# tests bb10/picks.py

import pytest
from picks import *


PICKS = {
    "1": [1, 24, 25, 48, 49, 72, 73, 96, 97, 120, 121, 144, 145, 168, 169, 192, 193, 216, 217, 240, 241, 264, 265, 288,
          289, 312, 313, 336, 337, 360, 361, 384],
    "2": [2, 23, 26, 47, 50, 71, 74, 95, 98, 119, 122, 143, 146, 167, 170, 191, 194, 215, 218, 239, 242, 263, 266, 287,
          290, 311, 314, 335, 338, 359, 362, 383],
    "3": [3, 22, 27, 46, 51, 70, 75, 94, 99, 118, 123, 142, 147, 166, 171, 190, 195, 214, 219, 238, 243, 262, 267, 286,
          291, 310, 315, 334, 339, 358, 363, 382],
    "4": [4, 21, 28, 45, 52, 69, 76, 93, 100, 117, 124, 141, 148, 165, 172, 189, 196, 213, 220, 237, 244, 261, 268, 285,
          292, 309, 316, 333, 340, 357, 364, 381],
    "5": [5, 20, 29, 44, 53, 68, 77, 92, 101, 116, 125, 140, 149, 164, 173, 188, 197, 212, 221, 236, 245, 260, 269, 284,
          293, 308, 317, 332, 341, 356, 365, 380],
    "6": [6, 19, 30, 43, 54, 67, 78, 91, 102, 115, 126, 139, 150, 163, 174, 187, 198, 211, 222, 235, 246, 259, 270, 283,
          294, 307, 318, 331, 342, 355, 366, 379],
    "7": [7, 18, 31, 42, 55, 66, 79, 90, 103, 114, 127, 138, 151, 162, 175, 186, 199, 210, 223, 234, 247, 258, 271, 282,
          295, 306, 319, 330, 343, 354, 367, 378],
    "8": [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161, 176, 185, 200, 209, 224, 233, 248, 257, 272, 281,
          296, 305, 320, 329, 344, 353, 368, 377],
    "9": [9, 16, 33, 40, 57, 64, 81, 88, 105, 112, 129, 136, 153, 160, 177, 184, 201, 208, 225, 232, 249, 256, 273, 280,
          297, 304, 321, 328, 345, 352, 369, 376],
    "10": [10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154, 159, 178, 183, 202, 207, 226, 231, 250, 255, 274,
           279, 298, 303, 322, 327, 346, 351, 370, 375],
    "11": [11, 14, 35, 38, 59, 62, 83, 86, 107, 110, 131, 134, 155, 158, 179, 182, 203, 206, 227, 230, 251, 254, 275,
           278, 299, 302, 323, 326, 347, 350, 371, 374],
    "12": [12, 13, 36, 37, 60, 61, 84, 85, 108, 109, 132, 133, 156, 157, 180, 181, 204, 205, 228, 229, 252, 253, 276,
           277, 300, 301, 324, 325, 348, 349, 372, 373],
}


@pytest.fixture
def n_teams():
    return 12


@pytest.fixture
def n_rounds():
    return 20


@pytest.fixture
def draft_slot():
    return 5


def test_generate_picks(draft_slot, n_teams, n_rounds):
    """Tests generate_picks"""
    picks = generate_picks(draft_slot, n_teams, n_rounds)
    assert picks == PICKS[str(draft_slot)][0:n_rounds]


def test_generate_all_picks(n_teams, n_rounds):
    """Tests generate_all_picks"""
    picks = generate_all_picks(n_teams, n_rounds)
    for i in range(1, n_teams + 1):
        assert picks[i] == PICKS[str(i)][0:n_rounds]


def test_generate_snake_order():
    """Tests generate_snake_order"""
    teams = ['A', 'B', 'C']
    n_rounds = 4
    order = generate_snake_order(teams, n_rounds)
    assert len(order) == len(teams) * n_rounds
    assert order == ['A', 'B', 'C', 'C', 'B', 'A', 'A', 'B', 'C', 'C', 'B', 'A']

    teams = ['A', 'B', 'C']
    n_rounds = 5
    order = generate_snake_order(teams, n_rounds)
    assert len(order) == len(teams) * n_rounds
    assert order == ['A', 'B', 'C', 'C', 'B', 'A', 'A', 'B', 'C', 'C', 'B', 'A', 'A', 'B', 'C']
