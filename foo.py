import pickle
import time
import requests
import random

from webData import load_obj, save_obj


def req(url, max_retries=500):
    retries = 0
    time.sleep(3)

    while retries < max_retries:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            print(f'Received status code {r.status_code}. Retrying...')
            time.sleep(30)
        except requests.exceptions.ConnectionError as e:
            print(f'Connection error: {e}')
            time.sleep(30)

        retries += 1
        print(f'Retry {retries}/{max_retries}')

    return None


def backfill_game_data(seasons):
    for season in seasons:
        games = load_obj(season + 'Games')
        for game in games:
            url = f'https://www.balldontlie.io/api/v1/stats?&game_ids[]={game}&per_page=100'
            response = req(url)
            if response:
                games[game]['data'] = response['data']
                save_obj(games, season + 'Games')


if __name__ == '__main__':
    seasons = ['2010', '2009', '2008', '2007', '2006']
    seasons.reverse()
    backfill_game_data(seasons)
