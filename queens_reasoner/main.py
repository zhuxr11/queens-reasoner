import numpy as np
from playwright.sync_api import sync_playwright
from queens_solver.browser import open_queens_game
from queens_solver.parser import parse_queens_game
from queens_solver.validator import validate_queens_game

from queens_reasoner.reasoner import (
    update_mask_multi_color,
    update_mask_other_row_col,
    update_mask_single_color,
    update_mask_whole_row_col,
)
from queens_reasoner.utils import print_queens_solution


def run(*args, **kwargs) -> None:
    """Run the complete Queens puzzle solving pipeline.

    This function:

    1. Parses a Queens puzzle board from the target source.
    2. Solves the puzzle using reasoner.
    3. Prints the formatted solution to the terminal.

    Positional and keyword arguments are forwarded directly to
    ``parse_queens_game``.

    Args:
        *args:
            Positional arguments passed to ``parse_queens_game``.

        **kwargs:
            Keyword arguments passed to ``parse_queens_game``.

    Returns:
        None
    """
    with sync_playwright() as p:
        page, mode = open_queens_game(p, *args, **kwargs)
        game_mat = parse_queens_game(page=page, mode=mode)
        game_solution = reason_queens_game(mat=game_mat.toarray())
        validation = validate_queens_game(
            solution=game_solution,
            page=page,
            mode=mode,
        )
        if not validation:
            raise RuntimeError("Validation failed")
    print_queens_solution(mat=game_mat.toarray(), mask=game_solution)


def reason_queens_game(
    mat: np.ndarray,
) -> np.ndarray:
    old_mask = np.zeros(shape=mat.shape, dtype=np.int64)
    new_mask = -np.ones(shape=mat.shape, dtype=np.int64)
    print_queens_solution(mat=mat, mask=new_mask)

    while not np.all(np.equal(old_mask, new_mask)):
        old_mask = new_mask.copy()
        new_mask = update_mask_whole_row_col(mat=mat, mask=new_mask)
        new_mask = update_mask_other_row_col(mat=mat, mask=new_mask)
        new_mask = update_mask_single_color(mat=mat, mask=new_mask)
        new_mask = update_mask_multi_color(mat=mat, mask=new_mask)

    return new_mask
