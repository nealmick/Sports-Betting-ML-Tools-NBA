import time
import requests
from itertools import chain

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda *args, **kwargs: args[0]


BASE_URL = "api.the-odds-api.com/v4"
PROTOCOL = "https://"

BOOKMAKER_MAPPING = {
    'DraftKings': 'draftkings',
    'FanDuel': 'fanduel',
    'Unibet': 'unibet_us',
    'MyBookie.ag': 'mybookieag',
    'BetMGM': 'betmgm',
    'Caesars': 'williamhill_us',
    'Bovada': 'bovada',
    'PointsBet (US)': 'pointsbetus',
    'WynnBET': 'wynnbet',
    'BetRivers': 'betrivers',
    'BetUS': 'betus',
    'SuperBook': 'superbook',
    'BetOnline.ag': 'betonlineag',
    'LowVig.ag': 'lowvig',
    '888sport': 'sport888',
    'Betfair Exchange': 'betfair_ex_uk',
    'Betfair Sportsbook': 'betfair_sb_uk',
    'Bet Victor': 'betvictor',
    'Betway': 'betway',
    'BoyleSports': 'boylesports',
    'Casumo': 'casumo',
    'Coral': 'coral',
    'Grosvenor': 'grosvenor',
    'Ladbrokes': 'ladbrokes_uk',
    'LeoVegas': 'leovegas',
    'LiveScore Bet': 'livescorebet',
    'Matchbook': 'matchbook',
    'Mr Green': 'mrgreen',
    'Paddy Power': 'paddypower',
    'Sky Bet': 'skybet',
    'Unibet': 'unibet_uk',
    'Virgin Bet': 'virginbet',
    'William Hill (UK)': 'williamhill',
    '1xBet': 'onexbet',
    'Betclic': 'betclic',
    'Betsson': 'betsson',
    'Coolbet': 'coolbet',
    'Everygame': 'everygame',
    'Livescorebet (EU)': 'livescorebet_eu',
    'Marathon Bet': 'marathonbet',
    'NordicBet': 'nordicbet',
    'Pinnacle': 'pinnacle',
    'Suprabets': 'suprabets',
    'William Hill': 'williamhill',
    'Betr': 'betr_au',
    'BlueBet': 'bluebet',
    'Ladbrokes': 'ladbrokes_au',
    'Neds': 'neds',
    'PlayUp': 'playup',
    'PointsBet (AU)': 'pointsbetau',
    'SportsBet': 'sportsbet',
    'TAB': 'tab',
    'TopSport': 'topsport',
}


class APIException(RuntimeError):
    def __str__(self):
        return f"('{self.args[0]}', '{self.args[1].json()['message']}')"


class AuthenticationException(APIException):
    pass


class RateLimitException(APIException):
    pass


def handle_faulty_response(response: requests.Response):
    if response.status_code == 401:
        raise AuthenticationException("Failed to authenticate with the API. is the API key valid?", response)
    elif response.status_code == 429:
        raise RateLimitException("Encountered API rate limit.", response)
    else:
        raise APIException("Unknown issue arose while trying to access the API.", response)


def get_sports(key):
    url = f"{BASE_URL}/sports/"
    escaped_url = PROTOCOL + requests.utils.quote(url)
    querystring = {"apiKey": key}

    response = requests.get(escaped_url, params=querystring)
    if not response:
        handle_faulty_response(response)

    return {item["key"] for item in response.json()}


def get_data(key,sport, region):
    url = f"{BASE_URL}/sports/{sport}/odds/"
    escaped_url = PROTOCOL + requests.utils.quote(url)
    querystring = {
        "apiKey": key,
        "regions": region,
        "oddsFormat": "decimal",
        "dateFormat": "unix"
    }

    response = requests.get(escaped_url, params=querystring)
    if not response:
        handle_faulty_response(response)

    return response.json()


def process_data(matches, include_started_matches = True):
    """Extracts all matches that are available and calculates some things about them, such as the time to start and
    the best available implied odds."""
    matches = tqdm(matches, desc="Checking all matches", leave=False, unit=" matches")
    for match in matches:
        start_time = int(match["commence_time"])
        if not include_started_matches and start_time < time.time():
            continue

        best_odd_per_outcome = {}
        for bookmaker in match["bookmakers"]:
            bookie_name = bookmaker["title"]
            for outcome in bookmaker["markets"][0]["outcomes"]:
                outcome_name = outcome["name"]
                odd = outcome["price"]
                if outcome_name not in best_odd_per_outcome.keys() or \
                    odd > best_odd_per_outcome[outcome_name][1]:
                    best_odd_per_outcome[outcome_name] = (bookie_name, odd)

        total_implied_odds = sum(1/i[1] for i in best_odd_per_outcome.values())
        match_name = f"{match['home_team']} v. {match['away_team']}"
        time_to_start = (start_time - time.time())/3600
        league = match["sport_key"]
        event_id = match.get('id', '')

        yield {
            "match_name": match_name,
            "match_start_time": start_time,
            "hours_to_start": time_to_start,
            "league": league,
            "best_outcome_odds": best_odd_per_outcome,
            "total_implied_odds": total_implied_odds,
            "id": event_id,
        }


def get_arbitrage_opportunities(key, region, cutoff):
    sports = get_sports(key)
    data = chain.from_iterable(get_data(key, sport, region=region) for sport in sports)
    data = filter(lambda x: x != "message", data)
    results = process_data(data)
    arbitrage_opportunities = list(filter(lambda x: 0 < x["total_implied_odds"] < 1-cutoff, results))

    arbitrage_opportunities = [arb for arb in arbitrage_opportunities if len(arb['best_outcome_odds']) <= 3]

    return arbitrage_opportunities

def get_updated_odds(event_id, bookmaker_titles, key):
    bookmaker_keys = [BOOKMAKER_MAPPING.get(title) for title in bookmaker_titles if title in BOOKMAKER_MAPPING]

    url = f"{PROTOCOL}{BASE_URL}/sports/upcoming/odds/"
    querystring = {
        "apiKey": key,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "eventIds": event_id,
        "bookmakers": ','.join(bookmaker_keys)
    }

    response = requests.get(url, params=querystring)

    if response.status_code != 200:
        handle_faulty_response(response)

    odds_data = response.json()
    return process_event_odds_data(odds_data, event_id, bookmaker_keys)



def process_event_odds_data(odds_data, event_id, bookmakers):
    structured_odds = {}

    for game in odds_data:
        if game["id"] == event_id:
            game_odds = {}

            for bookmaker in game["bookmakers"]:
                if bookmaker["key"] in bookmakers:
                    game_odds[bookmaker["key"]] = bookmaker["markets"]

            if game_odds:
                structured_odds[game["id"]] = {
                    "home_team": game["home_team"],
                    "away_team": game["away_team"],
                    "odds": game_odds
                }
                break

    return structured_odds