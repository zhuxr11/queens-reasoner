from collections.abc import Iterator
from itertools import combinations

import numpy as np

from queens_reasoner.utils import create_logger, print_queens_solution

# Experience 1: single color by row/column: queen must be in this row/column


def update_mask_whole_row_col(
    mat: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Eliminate queen candidates using whole-row/column color coverage.

    If a single color index occupies an entire row or column (excluding
    elements that are already ruled out), then all other cells with the
    same color index outside that row or column cannot contain queens.
    Such cells are set to 0 in the returned mask.

    Args:
        mat (np.ndarray): 2D integer matrix of color indices.
        mask (np.ndarray): 2D mask matrix. Cells that cannot contain queens
            are set to 0.

    Returns:
        np.ndarray: Updated mask matrix.
    """
    logger_row = create_logger("queens_reasoner::row_single_color")
    logger_col = create_logger("queens_reasoner::column_single_color")

    new_mask = mask.copy()

    n_rows, n_cols = mat.shape

    updated = True

    while updated:
        updated = False
        for color_idx in np.unique(mat):
            positions = np.argwhere((mat == color_idx) & (new_mask == -1))
            rows = positions[:, 0]
            # Count occurrences per row/column
            row_counts = np.bincount(rows, minlength=n_rows)

            # Whole-row coverage
            whole_rows = np.where(
                (row_counts == np.sum(new_mask == -1, axis=1))
                & (np.sum(new_mask == 1, axis=1) == 0)
            )[0]
            for r in whole_rows:
                # Same color outside this row cannot be queens
                outside = (mat == color_idx) & (new_mask == -1)
                outside[r, :] = False
                if np.any(outside):
                    logger_row.info(
                        f"Color {color_idx + 1} takes up entire undetermined "
                        f"element(s) in row {r + 1}; "
                        f"all other elements with color {color_idx + 1} "
                        f"({np.count_nonzero(outside)}) cannot be queens"
                    )
                    new_mask[outside] = 0
                    updated = True
                    print_queens_solution(mat=mat, mask=new_mask)

            positions = np.argwhere((mat == color_idx) & (new_mask == -1))
            cols = positions[:, 1]
            # Count occurrences per column
            col_counts = np.bincount(cols, minlength=n_cols)

            # Whole-column coverage
            whole_cols = np.where(
                (col_counts == np.sum(new_mask == -1, axis=0))
                & (np.sum(new_mask == 1, axis=0) == 0)
            )[0]
            for c in whole_cols:
                # Same color outside this column cannot be queens
                outside = (mat == color_idx) & (new_mask == -1)
                outside[:, c] = False
                if np.any(outside):
                    logger_col.info(
                        f"Color {color_idx + 1} takes up entire undetermined "
                        f"element(s) in column {c + 1}; "
                        f"all other elements with color {color_idx + 1} "
                        f"({np.count_nonzero(outside)}) cannot be queens"
                    )
                    new_mask[outside] = 0
                    updated = True
                    print_queens_solution(mat=mat, mask=new_mask)
    return new_mask


# Experience 2: If all other elements in a row/column are not queens,
# then the remaining element must be queen


def update_mask_other_row_col(
    mat: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Deduce queen positions from single-candidate rows or columns.

    If all other candidate positions in a row or column are ruled out
    except one remaining position, that position must be a queen. After
    marking a queen, conflicting positions are eliminated.

    Mask values:
        - ``-1``: candidate / unknown
        - ``0``: cannot be queen
        - ``1``: confirmed queen

    Args:
        mat (np.ndarray): 2D color matrix.
        mask (np.ndarray): 2D mask matrix.

    Returns:
        np.ndarray: Updated mask matrix.
    """
    logger_row = create_logger("queens_reasoner::row_one_candidate")
    logger_col = create_logger("queens_reasoner::column_one_candidate")
    mask = mask.copy()

    n_rows, n_cols = mask.shape

    updated = True

    while updated:
        updated = False

        #
        # Rows
        #
        for r in range(n_rows):
            candidate_cols = np.where(mask[r, :] == -1)[0]

            if len(candidate_cols) != 1:
                continue

            c = candidate_cols[0]

            if mask[r, c] == 1:
                continue

            logger_row.info(
                f"Row {r + 1} has only one remaining candidate "
                f"at ({r + 1}, {c + 1}); marking as queen"
            )

            mask[r, c] = 1

            # Propagate queen constraints
            mask = np.maximum(
                mask,
                gen_mask_single_queen(
                    shape=mask.shape,
                    row=r,
                    col=c,
                ),
            )
            print_queens_solution(mat=mat, mask=mask)

            updated = True

        #
        # Columns
        #
        for c in range(n_cols):
            candidate_rows = np.where(mask[:, c] == -1)[0]

            if len(candidate_rows) != 1:
                continue

            r = candidate_rows[0]

            if mask[r, c] == 1:
                continue

            logger_col.info(
                f"Column {c + 1} has only one remaining candidate "
                f"at ({r + 1}, {c + 1}); marking as queen"
            )

            mask[r, c] = 1

            # Propagate queen constraints
            mask = np.maximum(
                mask,
                gen_mask_single_queen(
                    shape=mask.shape,
                    row=r,
                    col=c,
                ),
            )
            print_queens_solution(mat=mat, mask=mask)

            updated = True

    return mask


# Experience 3: For all possible queens per color
# determine the elements that must/cannot be queens


def update_mask_single_color(
    mat: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Deduce queen positions from single-color constraints.

    For each color with no confirmed queen, considers all possible queen
    placements and identifies cells that must or cannot contain a queen.

    Args:
        mat (np.ndarray): 2D integer matrix of color indices.
        mask (np.ndarray): 2D mask matrix.

    Returns:
        np.ndarray: Updated mask matrix.
    """
    logger = create_logger("queens_reasoner::single_color_masking")
    new_mask = mask.copy()

    updated = True

    while updated:
        updated = False
        for color_idx in np.unique(mat):
            if np.any((mat == color_idx) & (new_mask == 1)):
                continue
            positions = np.argwhere((mat == color_idx) & (new_mask == -1))

            rows = positions[:, 0]
            cols = positions[:, 1]

            single_color_mask = []
            for row, col in zip(rows, cols, strict=True):
                single_color_mask.append(gen_mask_single_queen(mat.shape, row, col))
            single_color_mask = reduce_masks(masks=single_color_mask)

            cur_mask = new_mask.copy()
            new_mask = np.maximum(new_mask, single_color_mask)
            update_queens = (new_mask != cur_mask) & (single_color_mask == 1)
            update_nonqueens = (new_mask != cur_mask) & (single_color_mask == 0)
            logger_msg = f"Color {color_idx + 1} "
            if np.any(update_queens):
                logger_msg += "determines its queen"
                updated = True
            if np.any(update_nonqueens):
                if np.any(update_queens):
                    logger_msg += ", and "
                logger_msg += (
                    f"eliminates the possibility of queens "
                    f"on {np.count_nonzero(update_nonqueens)} elements"
                )
                updated = True
            if np.any(update_queens) or np.any(update_nonqueens):
                logger.info(logger_msg)
                print_queens_solution(mat=mat, mask=new_mask)

    return new_mask


def gen_mask_single_queen(
    shape: tuple[int, int],
    row: int,
    col: int,
) -> np.ndarray:
    """Generate a mask for a single queen placement.

    Marks the given position as a queen (1) and eliminates all
    conflicting positions in the same row, column, and diagonally
    adjacent cells.

    Args:
        shape (tuple[int, int]): Board shape as ``(rows, cols)``.
        row (int): Row index of the queen.
        col (int): Column index of the queen.

    Returns:
        np.ndarray: Mask matrix with queen and non-queen positions marked.

    Raises:
        AssertionError: If ``row`` or ``col`` is out of bounds.
    """
    assert row >= 0 and row < shape[0], (
        f"row index ({row + 1}) out of range; shape[0] = {shape[0]}"
    )
    assert col >= 0 and col < shape[1], (
        f"column index ({col + 1}) out of range; shape[1] = {shape[1]}"
    )
    res = -np.ones(shape=shape, dtype=np.int64)
    res[row, col] = 1
    # Set the other elements in the same column as 0 (non-queens)
    for other_row in range(shape[0]):
        if other_row != row:
            res[other_row, col] = 0
    # Set the other elements in the same row as 0 (non-queens)
    for other_col in range(shape[1]):
        if other_col != col:
            res[row, other_col] = 0
    # Set the diagonally adjacent elements as 0 (non-queens)
    left_exist = col > 0
    right_exist = col < shape[1] - 1
    top_exist = row > 0
    bottom_exist = row < shape[0] - 1
    if left_exist:
        if top_exist:
            res[row - 1, col - 1] = 0
        if bottom_exist:
            res[row + 1, col - 1] = 0
    if right_exist:
        if top_exist:
            res[row - 1, col + 1] = 0
        if bottom_exist:
            res[row + 1, col + 1] = 0
    return res


def reduce_masks(masks: list[np.ndarray]) -> np.ndarray:
    """Reduce a list of masks to their consensus.

    At each position, if all masks agree on the value, keep it;
    otherwise set to -1 (unknown).

    Args:
        masks (list[np.ndarray]): List of ndarrays with identical shapes.

    Returns:
        np.ndarray: Reduced mask.
    """
    res = masks[0].copy()

    for arr in masks[1:]:
        res[res != arr] = -1

    return res


# Experience 4: If k colors have all possible queen elements in k rows/columns,
# then other colors cannot have queens in these rows/columns


def update_mask_multi_color(
    mat: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Apply multi-color constraint reasoning.

    If k colors have all their possible queen positions confined to
    k rows or k columns, then other colors cannot place queens in
    those rows or columns.

    Args:
        mat (np.ndarray): 2D integer matrix of color indices.
        mask (np.ndarray): 2D mask matrix.

    Returns:
        np.ndarray: Updated mask matrix.
    """
    logger = create_logger("queens_reasoner::multi_color_masking")

    mask = mask.copy()
    new_mask = mask.copy()

    orientation = "row"
    updated = True

    while orientation is not None and updated:
        updated = False
        unknown_positions = []
        for color_idx in np.unique(mat):
            if np.any((mat == color_idx) & (mask == 1)):
                unknown_positions.append(np.empty((0, mat.ndim)))
            else:
                positions = np.argwhere((mat == color_idx) & (mask == -1))
                unknown_positions.append(positions)
        for orientation, mat_idx, list_idx in iter_min_subset(unknown_positions):
            outside = -np.ones(shape=mask.shape, dtype=np.int64)
            if orientation == "row":
                outside[mat_idx, :] = mask[mat_idx, :] * np.isin(
                    mat[mat_idx, :], list_idx
                )
            elif orientation == "column":
                outside[:, mat_idx] = mask[:, mat_idx] * np.isin(
                    mat[:, mat_idx], list_idx
                )
            else:
                raise ValueError(f"Invalid orientation: {orientation}")

            update_nonqueens = (outside != -1) & (mask == -1)
            if np.any(update_nonqueens):
                logger.info(
                    f"Color(s) {', '.join([str(x + 1) for x in list_idx])} eliminate "
                    f"the possibility of queens on all other elements "
                    f"in {orientation}(s) {', '.join([str(x + 1) for x in mat_idx])}"
                )
                updated = True

            new_mask = np.maximum(mask, outside)
            if updated:
                print_queens_solution(mat=mat, mask=new_mask)
                mask = new_mask
                break
    return new_mask


# def find_min_subset(lst: list[np.ndarray]) -> tuple[str, tuple[int], tuple[int]]:
#     """
#     Given a list of ndarrays (rows are [row, col] positions),
#     find a small subset where union of rows or columns <= number of arrays selected.

#     Returns:
#         orientation: "row" or "column"
#         unique_values: list of unique row/column numbers
#         selected_indices: tuple of indices of arrays selected
#     """
#     valid = [
#         (idx, arr)
#         for idx, arr in enumerate(lst)
#         if arr.shape[0] > 0
#     ]

#     if len(valid) == 0:
#         return None, [], ()

#     original_indices = [idx for idx, _ in valid]

#     row_sets = [
#         set(arr[:, 0])
#         for _, arr in valid
#     ]

#     col_sets = [
#         set(arr[:, 1])
#         for _, arr in valid
#     ]

#     n = len(valid)

#     def greedy(sets: list[set]):
#         selected = []
#         union_set = set()
#         remaining = set(range(n))

#         while remaining:
#             # Pick array adding fewest new values
#             best_idx = min(
#                 remaining,
#                 key=lambda i: len(sets[i] - union_set),
#             )

#             selected.append(best_idx)
#             union_set |= sets[best_idx]
#             remaining.remove(best_idx)

#             if len(union_set) <= len(selected):
#                 return (
#                     union_set,
#                     tuple(original_indices[i] for i in selected),
#                 )

#         return None, ()

#     # Try rows
#     row_union, row_indices = greedy(row_sets)

#     # Try columns
#     col_union, col_indices = greedy(col_sets)

#     # Choose smaller solution
#     if (
#         row_indices
#         and (
#             not col_indices
#             or len(row_indices) <= len(col_indices)
#         )
#     ):
#         return "row", tuple(sorted(row_union)), row_indices

#     if col_indices:
#         return "column", tuple(sorted(col_union)), col_indices

#     return None, (), ()


def iter_min_subset(
    lst: list[np.ndarray],
) -> Iterator[tuple[str, tuple[int], tuple[int]]]:
    """Yield subsets where the union of rows or columns is minimal.

    For each k from 1 to n, examines all k-combinations of arrays and
    yields those where the number of unique rows or unique columns
    is at most k.

    Args:
        lst (list[np.ndarray]): List of 2D position arrays, each with
            shape ``(N, 2)`` where columns are ``[row, col]``.

    Yields:
        tuple[str, tuple[int], tuple[int]]: A tuple of
        ``(orientation, unique_indices, selected_array_indices)``
        where orientation is ``"row"`` or ``"column"``.
    """
    valid = [(idx, arr) for idx, arr in enumerate(lst) if arr.shape[0] > 0]
    if not valid:
        return

    original_indices = [idx for idx, _ in valid]
    n = len(valid)

    row_sets = [set(arr[:, 0]) for _, arr in valid]
    col_sets = [set(arr[:, 1]) for _, arr in valid]

    for k in range(1, n + 1):
        for idxs in combinations(range(n), k):
            combined_rows = set().union(*(row_sets[i] for i in idxs))
            combined_cols = set().union(*(col_sets[i] for i in idxs))

            if len(combined_rows) <= k:
                yield (
                    "row",
                    tuple(sorted(combined_rows)),
                    tuple(original_indices[i] for i in idxs),
                )
            elif len(combined_cols) <= k:
                yield (
                    "column",
                    tuple(sorted(combined_cols)),
                    tuple(original_indices[i] for i in idxs),
                )
