import logging

import numpy as np


def create_logger(name: str) -> logging.Logger:
    """Create and configure a logger with a standard format.

    Args:
        name (str): Logger name, typically in ``"package::module"`` format.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger(name)


def print_queens_solution(
    mat: np.ndarray,
    mask: np.ndarray,
) -> None:
    """Print a formatted Queens puzzle solution to the terminal.

    The board layout is displayed as a colored NumPy array where queen
    positions are highlighted using terminal color formatting.

    Internally, queen cells are represented as negative values to allow
    conditional coloring during NumPy array formatting.

    Args:
        mat (np.ndarray): Sparse matrix of the puzzle layout. Each entry
            contains the integer color ID of a cell.
        mask (np.ndarray): Dense matrix indicating queen placements.
            ``1`` is a queen, ``0`` is a non-queen, ``-1`` is unknown.

    Returns:
        None
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

    Args:
        x (int): Integer value to format.
        marker (str): Character used as the queen marker.
        anti_marker (str): Character used as the non-queen marker.

    Returns:
        str: Formatted string.

    Example:
        >>> mark_ndarray(-3)
        '3*'
        >>> mark_ndarray(5)
        '5x'
        >>> mark_ndarray(10007)
        ' '
    """
    c = marker if x < 0 else (anti_marker if x < 10000 else " ")
    return f"{abs(x) if x <= 10000 else abs(x - 10000) // 3}{c}"
