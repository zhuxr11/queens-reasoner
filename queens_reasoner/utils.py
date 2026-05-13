import logging

import numpy as np


def create_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger(name)


def print_queens_solution(
    mat: np.ndarray,
    mask: np.ndarray,
):
    """Print a formatted Queens puzzle solution to the terminal.

    The board layout is displayed as a colored NumPy array where queen
    positions are highlighted using terminal color formatting.

    Internally, queen cells are represented as negative values to allow
    conditional coloring during NumPy array formatting.

    Args:
        layout:
            Sparse matrix representing the puzzle layout. Each entry
            contains the integer color ID of a cell.

        solution:
            Dense binary NumPy array indicating queen placements.

            - ``1`` indicates a queen.
            - ``0`` indicates an empty cell.
            - ``-1`` indicates an empty cell.

    Returns:
        None

    Notes:
        Terminal coloring is implemented using ``colorama`` and
        ``numpy.printoptions`` with a custom integer formatter.
    """
    mat_marked = (mat + 1) * (1 - mask * 2) + (mask < 0) * 10000
    with np.printoptions(
        formatter={"int": lambda x: mark_ndarray(x)},
    ):
        print(mat_marked)


def mark_ndarray(x: int, marker: str = "*", anti_marker: str = "x") -> str:
    """Format an integer value with optional terminal coloring.

    Negative values are highlighted using designated markers.
    Positive values are printed normally.

    The displayed value is converted to its absolute value before applying
    the optional offset.

    Args:
        x:
            Integer value to format.

        marker:
            Character as marker of queens.

        anti_marker:
            Character as marker of non-queens.

    Returns:
        Formatted string.

    Example:
        ```python
        mark_ndarray(-3)
        mark_ndarray(5)
        mark_ndarray(10007)
        ```
    """
    c = marker if x < 0 else (anti_marker if x < 10000 else " ")
    return f"{abs(x) if x <= 10000 else abs(x - 10000) // 3}{c}"
