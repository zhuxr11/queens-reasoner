import numpy as np

from queens_reasoner.main import reason_queens_game
from queens_reasoner.utils import print_queens_solution

# Color index legend:
# 0 = purple
# 1 = orange
# 2 = blue
# 3 = green
# 4 = gray
# 5 = coral
# 6 = yellow
# 7 = white

mat1 = np.array(
    [
        [0, 0, 0, 0, 1, 1, 1, 7, 7],
        [0, 2, 2, 0, 0, 1, 1, 7, 7],
        [0, 2, 2, 3, 0, 0, 1, 1, 7],
        [0, 0, 3, 3, 3, 0, 0, 1, 1],
        [6, 0, 0, 4, 4, 4, 0, 0, 1],
        [6, 6, 0, 0, 4, 5, 5, 0, 0],
        [6, 6, 6, 0, 0, 5, 5, 8, 0],
        [6, 6, 6, 6, 0, 0, 8, 8, 0],
        [6, 6, 6, 6, 6, 0, 0, 0, 0],
    ],
    dtype=int,
)

mat2 = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [2, 2, 3, 3, 0, 0, 0],
        [2, 2, 3, 3, 0, 0, 0],
        [4, 4, 4, 5, 5, 0, 0],
        [4, 4, 4, 5, 5, 0, 0],
        [4, 4, 4, 5, 5, 0, 6],
    ],
    dtype=int,
)


def test_reasoner_default():
    mask1 = reason_queens_game(mat=mat1)
    print_queens_solution(mat=mat1, mask=mask1)


def test_reasoner_entire_row_col():
    mask2 = reason_queens_game(mat=mat2)
    print_queens_solution(mat=mat2, mask=mask2)
