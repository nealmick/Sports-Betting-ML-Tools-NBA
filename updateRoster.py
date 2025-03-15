import pickle
import requests
import time
import random

LABELS = ['ast', 'blk', 'dreb', 'fg3_pct', 'fg3a', 'fg3m', 'fga', 'fgm', 'fta', 'ftm', 'oreb', 'pf', 'pts', 'reb', 'stl', 'turnover', 'min']


def save_obj(obj, name):
    with open('updatedObj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def req(url):
    r = requests.get(url)
    if r.status_code != 200:
        time.sleep(30)
        return req(url)
    time.sleep(1.5)
    return r.json()


def get_season_average(player_id, season):
    url = f'https://www.balldontlie.io/api/v1/season_averages?season={season}&player_ids[]={player_id}'
    r = req(url)
    if len(r['data']) == 0:
        return []
    return [r['data'][0][label] for label in LABELS]


def updateRoster():
    roster = {str(i): [] for i in range(0, 31)}
    player_id_by_team = load_obj('2022PlayerIdByTeamID')

    for team in player_id_by_team:
        for player_id in player_id_by_team[team]:
            url = f'https://www.balldontlie.io/api/v1/players/{player_id}'
            r = req(url)
            team_id = r['team']['id']
            roster[str(team_id)].append(player_id)
            save_obj(roster, 'roster')


if __name__ == '__main__':
    updateRoster()
