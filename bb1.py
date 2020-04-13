import pandas as pd
import numpy as np

import requests

from picks import generate_snake_order

stat_headers = [
    'pass_yards',
    'pass_tds',
    'pass_twopt',
    'pass_int',
    'rush_yards',
    'rush_tds',
    'rush_twopt',
    'rec',
    'rec_yds',
    'rec_tds',
    'rec_twopt',
    'fumbles',
    'off_fumbrec_td',
    'def_sacks',
    'def_int',
    'def_fumble_rec',
    'def_safety',
    'def_int_tds',
    'def_fumbble_rec_tds',
    'def_kickret_tds',
    'def_puntret_tds',
    'def_block_kick_tds',
    'def_shutout',
    'def_PNTS1_6',
    'def_PNTS7_20',
    'def_PNTS21_29',
    'def_PNTS30_99'
]


headers = {
    'Referer': 'https://bestball10s.shgn.com/historical/league/football/22182',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'DNT': '1',
}

params = (
    ('v', '2.71'),
)

# STEP 1: get basic data
# BB10_PLAYERS
# is a dict of player_id(str): player_name(str)
# {'1905': 'Kansas City Chiefs'}
url = 'https://assets.shgn.com/highstakes/historical/players/football.json?v=2.71'
response = requests.get(url, headers=headers, params=params)
players = response.json()

# OWNERS
# Is a dict of owner_id, owner_name
# {"22653": "@BTXJ", ...}
url = 'https://assets.shgn.com/highstakes/historical/owners/_owners.json?v=2.71'
response = requests.get(url, headers=headers, params=params)
owners = response.json()

# OWNER_TEAMS
# Is a list of 3-element lists [team_id, owner_name, owner_id]
# Example: [191980,"@BTXJ",22653]
# team_id is unique; reuse user_name and user_id for every team user has
url = 'https://assets.shgn.com/highstakes/historical/teams/football/mfl.2019.json?v=2.71'
response = requests.get(url, headers=headers, params=params)
owner_teams = response.json()
owner_teams_d = {item[0]: (item[1], item[2]) for item in owner_teams}


def get_team_owner(team_id):
    """Returns tuple of owner_handle, owner_id given team_id

    Args:
        team_id (int): the numeric team ID

    Example:
        owner_handle, owner_id = get_team_owner(owner_team)
    """
    return owner_teams_d.get(team_id)


# STEP 2: get 2019 leagues

# league_2019 is a 3 element list
# [0] is a list of player ids
# [1] are stat headers
# [2] is a list of list of leagues
url = 'https://assets.shgn.com/highstakes/historical/leagues/football/mfl.2019.json?v=2.71'
response = requests.get(url, headers=headers, params=params)
league_2019 = response.json()

# create an intermediate dictionary
# key is the index of league_2019[0] (the list of player_ids)
# value is the player name
# this makes parsing draft easier, as it uses indexes rather than player ids
player_ids = league_2019[0]
idx_player_lookup = {idx: players.get(str(item)) for idx, item
                     in enumerate(player_ids)}

# drafts is a list of dicts
# keys are league_id, team_id, pick_number, player_id, player_name
leagues = league_2019[2]
n_rounds = 20
drafts = []


def process_league_draft(lg, pids, pids_lookup, rnd):
    """Processes league draft"""
    pks = []
    league_id = lg[0]
    league_draft = lg[3][1]
    all_teams = generate_snake_order([item[0] for item in lg[2]], rnd)
    for idx, item in enumerate(league_draft):
        pick = {'league_id': league_id,
                'team_id': all_teams[idx],
                'pick': idx + 1,
                'player_id': pids[item],
                'player_name': pids_lookup.get(item)
                }
        pks.append(pick)
    return pks


def process_league_results(lg):
    """Processes league results"""
    results = []
    for item in lg[2]:
        result = {
            'league_id': lg[0],
            'team_id': item[0],
            'points': item[1]
        }
        for h, v in zip(stat_headers, item[2][0]):
            result[h] = v
        for h, v in zip(stat_headers, item[2][1]):
            result[f'{h}_fpts'] = v
        results.append(result)
    return results


for league in leagues:
    draft_picks = process_league_draft(league, player_ids, idx_player_lookup, n_rounds)
    league_results = process_league_results(league)


# print out results
summ = (
    pd.DataFrame(draft_picks)
    .join(pd.DataFrame(league_results).set_index('team_id')['points'], on='team_id', how='left')
    .groupby(['player_id', 'player_name'])
    .agg({'pick': ['mean', 'median'], 'points': ['count', 'mean']})
    .sort_values(by=('points', 'mean'), ascending=False)
)

summ.columns = [f'{a}_{b}' for a, b in summ.columns]
summ.query('points_count > 500').head(50)