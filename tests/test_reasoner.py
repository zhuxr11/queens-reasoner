import numpy as np

from queens_reasoner.main import reason_queens_game
from queens_reasoner.utils import print_queens_solution

# Queens No. 747: Dome, published on May 17, 2026
mat = np.array(
    [
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 7, 7, 7, 2, 2, 2],
        [2, 2, 6, 6, 6, 6, 6, 2, 2],
        [2, 4, 4, 4, 4, 4, 4, 5, 2],
        [2, 4, 1, 1, 1, 8, 8, 5, 2],
        [2, 4, 1, 0, 0, 0, 8, 5, 2],
        [2, 4, 1, 1, 0, 3, 8, 5, 2],
        [1, 1, 1, 1, 0, 3, 3, 5, 5],
        [1, 1, 1, 0, 0, 0, 3, 3, 5],
    ],
    dtype=np.int64,
)


def test_reasoner():
    mask = reason_queens_game(mat=mat)
    print_queens_solution(mat=mat, mask=mask)
