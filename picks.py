# picks.py
# generates list of pick numbers for a snake draft


def generate_all_picks(n_teams, n_rounds):
    return dict([(i, generate_picks(i, n_teams, n_rounds))
                 for i in range(1, n_teams + 1)])


def generate_picks(slot, n_teams, n_rounds):
    return [((r - 1) * n_teams + slot) if r % 2 == 1 else (r * n_teams) - slot + 1
            for r in range(1, n_rounds + 1)]


def generate_snake_order(teams, n_rounds):
    """Create a snake draft order

    Args:
        teams (iterable): e.g. ('Team1', 'Team2', 'Team3')
        n_rounds (int): number of rounds in draft

    Returns:
        list

    Examples:
        >>>generate_snake_order(teams=['A', 'B', 'C'], n_rounds=4)
        ['A', 'B', 'C', 'C', 'B', 'A', 'A', 'B', 'C', 'C', 'B', 'A']
    """
    if n_rounds % 2 == 0:
        return (teams + teams[::-1]) * int(n_rounds / 2)
    else:
        return generate_snake_order(teams, int(n_rounds -1)) + teams


if __name__ == '__main__':
    pass
