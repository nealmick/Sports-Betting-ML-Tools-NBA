import os
import requests


def req_spread(url):
    r = requests.get(url)
    return r.json()


def getSpread(abv_home, abv_visitor):
    api_key = os.environ.get('ODDS_API_KEY', '')
    CHOICES = {
    'ATL' :'Atlanta Hawks',
    'BKN':	'Brooklyn Nets',
    'BOS':	'Boston Celtics',
    'CHA':	'Charlotte Hornets',
    'CHI':	'Chicago Bulls',
    'CLE':	'Cleveland Cavaliers',
    'DAL':	'Dallas Mavericks',
    'DEN':	'Denver Nuggets',
    'DET':	'Detroit Pistons',
    'GSW':	'Golden State Warriors',
    'HOU':	'Houston Rockets',
    'IND':	'Indiana Pacers',
    'LAC':	'Los Angeles Clippers',
    'LAL':	'Los Angeles Lakers',
    'MEM':	'Memphis Grizzlies',
    'MIA':	'Miami Heat',
    'MIL':	'Milwaukee Bucks',
    'MIN':	'Minnesota Timberwolves',
    'NOP':	'New Orleans Pelicans',
    'NYK':	'New York Knicks',
    'OKC':	'Oklahoma City Thunder',
    'ORL':	'Orlando Magic',
    'PHI':	'Philadelphia 76ers',
    'PHX':	'Phoenix Suns',
    'POR':	'Portland Trail Blazers',
    'SAC':	'Sacramento Kings',
    'SAS':	'San Antonio Spurs',
    'TOR':	'Toronto Raptors',
    'UTA':	'Utah Jazz',
    'WAS':	'Washington Wizards',
    }
    TEAM_NAMES = CHOICES
    home_full = TEAM_NAMES[abv_home]
    visitor_full = TEAM_NAMES[abv_visitor]

    url = f'https://api.the-odds-api.com/v4/sports/basketball_nba/odds?markets=h2h,spreads,totals&regions=us&apiKey={api_key}'
    spread_data = req_spread(url)

    home_spread = 0
    visitor_spread = 0
    dk_home_spread = 0
    dk_visitor_spread = 0

    for provider in spread_data:
        for game in provider['bookmakers']:
            if game['title'] == 'FanDuel':
                outcomes = game['markets'][1]['outcomes']
                if outcomes[0]['name'] == visitor_full and outcomes[1]['name'] == home_full:
                    visitor_spread = outcomes[0]['point']
                    home_spread = outcomes[1]['point']
                    break
                if outcomes[0]['name'] == home_full and outcomes[1]['name'] == visitor_full:
                    home_spread = outcomes[0]['point']
                    visitor_spread = outcomes[1]['point']
                    break

    for provider in spread_data:
        for game in provider['bookmakers']:
            if game['title'] == 'DraftKings':
                outcomes = game['markets'][1]['outcomes']
                if outcomes[0]['name'] == visitor_full and outcomes[1]['name'] == home_full:
                    dk_visitor_spread = outcomes[0]['point']
                    dk_home_spread = outcomes[1]['point']
                    break
                if outcomes[0]['name'] == home_full and outcomes[1]['name'] == visitor_full:
                    dk_home_spread = outcomes[0]['point']
                    dk_visitor_spread = outcomes[1]['point']
                    break

    return [home_spread, visitor_spread, dk_home_spread, dk_visitor_spread]

