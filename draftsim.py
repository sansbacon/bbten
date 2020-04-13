import random

import numpy as np
import pandas as pd
import requests
from scipy import stats

from picks import generate_all_picks, generate_picks


def get_adp(year=2019):
    """Gets ADP and generates some quasi-random projections"""
    url = f'https://fantasyfootballcalculator.com/api/v1/adp/standard?teams=12&year={year}'
    r = requests.get(url)
    data = r.json()
    players = data['players']
    df = pd.DataFrame(players)
    df['proj'] = [i * random.uniform(.75, .99) for i in sorted(np.random.normal(200, 50, len(df)), reverse=True)]
    return df.set_index(['player_id', 'name', 'position', 'team'])


def prob(row, pick_number):
    """Calculates probability that player available at a pick given mean, stdev"""
    return 1 - stats.norm(row.adp, row.stdev).cdf(pick_number)


def run():
    # setup draft
    df = get_adp()
    n_teams = 12
    n_rounds = 20
    my_draft_slot = random.randint(1, 12)

    my_picks = generate_picks(my_draft_slot, n_teams, n_rounds)

    # generate probabilities for each round
    # given your picks
    newdf = df.loc[:, ['adp', 'stdev', 'proj']]
    for idx, pick in enumerate(my_picks):
        newdf[f'Round{idx + 1}'] = newdf.apply(prob, args=(pick,), axis=1)

    with pd.option_context('display.float_format', "{:,.3f}".format), pd.option_context('expand_frame_repr', False):
        print(f'Results for draft slot: {my_draft_slot}')
        print(newdf.iloc[:, 0:7].head(my_draft_slot + 5))


if __name__ == '__main__':
    run()
