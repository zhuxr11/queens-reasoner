# Queens Reasoner

Queens Reasoner solves "Queens" game hosted on [linkedin](https://linkedin.com/games/queens) with linear programming, with step-by-step reasoning as humans.

## Installation

To install Queens Reasoner, first run one of the following:

``` {bash}
# Using pip
pip install queens-reasoner

# Using uv
uv pip install queens-reasoner
```

Then, run this to install browsers for playwright:

``` {bash}
install-playwright-browsers
```

## Usage

The Queens Reasoner automatically loads the "Queens" game hosted daily. To call the reasoner, run:

``` {bash}
queens-reasoner
```

The reasoner first loads the game, then solves it, and finally validates the solution on the hosted webpage. Positions of queens are marked by asterisks to the right of color index, while others are marked by "x". In contrast to Queens Solver ("queens-slvr", which solves the game with linear programming), you may see the step-by-step reasoning process with Queens Reasoner. An example output looks like:

```
2026-05-13 09:43:01,303 [INFO] queens_browser: Page loaded from: https://linkedin.com/games/view/queens/desktop
2026-05-13 09:43:01,515 [INFO] queens_browser: [Play game] button clicked
2026-05-13 09:43:01,548 [INFO] queens_browser: Tutorial screen escaped
2026-05-13 09:43:01,733 [INFO] queens_parser: [queens-board] section found
2026-05-13 09:43:01,739 [INFO] queens_parser: Queens game board parsed
[[1  1  1  4  5  5  5 ]
 [6  6  1  5  5  5  5 ]
 [1  1  1  5  5  5  5 ]
 [2  2  1  5  5  3  5 ]
 [1  1  1  5  3  3  3 ]
 [5  5  5  5  5  3  7 ]
 [5  5  5  5  3  3  3 ]]
2026-05-13 09:43:01,750 [INFO] queens_reasoner::single_color_masking: Color 2 eliminates the possibility of queens on 9 elements
[[1  1  1  4  5  5  5 ]
 [6  6  1  5  5  5  5 ]
 [1x 1x 1  5  5  5  5 ]
 [2  2  1x 5x 5x 3x 5x]
 [1x 1x 1  5  3  3  3 ]
 [5  5  5  5  5  3  7 ]
 [5  5  5  5  3  3  3 ]]
2026-05-13 09:43:01,751 [INFO] queens_reasoner::single_color_masking: Color 4 determines its queen, and eliminates the possibility of queens on 13 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6  6  1x 5x 5x 5  5 ]
 [1x 1x 1  5x 5  5  5 ]
 [2  2  1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3  3 ]
 [5  5  5  5x 5  3  7 ]
 [5  5  5  5x 3  3  3 ]]
2026-05-13 09:43:01,755 [INFO] queens_reasoner::single_color_masking: Color 6 eliminates the possibility of queens on 2 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6  6  1x 5x 5x 5x 5x]
 [1x 1x 1  5x 5  5  5 ]
 [2  2  1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3  3 ]
 [5  5  5  5x 5  3  7 ]
 [5  5  5  5x 3  3  3 ]]
2026-05-13 09:43:01,757 [INFO] queens_reasoner::single_color_masking: Color 7 determines its queen, and eliminates the possibility of queens on 10 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6  6  1x 5x 5x 5x 5x]
 [1x 1x 1  5x 5  5  5x]
 [2  2  1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5  5  5  5x 3  3x 3x]]
2026-05-13 09:43:01,758 [INFO] queens_reasoner::single_color_masking: Color 1 eliminates the possibility of queens on 2 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6  6  1x 5x 5x 5x 5x]
 [1x 1x 1  5x 5  5  5x]
 [2  2x 1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5  5  5x 5x 3  3x 3x]]
2026-05-13 09:43:01,760 [INFO] queens_reasoner::single_color_masking: Color 2 determines its queen, and eliminates the possibility of queens on 2 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6  1x 5x 5x 5x 5x]
 [1x 1x 1  5x 5  5  5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5  5x 5x 3  3x 3x]]
2026-05-13 09:43:01,761 [INFO] queens_reasoner::single_color_masking: Color 3 eliminates the possibility of queens on 1 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6  1x 5x 5x 5x 5x]
 [1x 1x 1  5x 5x 5  5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5  5x 5x 3  3x 3x]]
2026-05-13 09:43:01,762 [INFO] queens_reasoner::single_color_masking: Color 6 determines its queen, and eliminates the possibility of queens on 2 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6* 1x 5x 5x 5x 5x]
 [1x 1x 1x 5x 5x 5  5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1  5x 3  3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5x 5x 5x 3  3x 3x]]
2026-05-13 09:43:01,765 [INFO] queens_reasoner::single_color_masking: Color 1 determines its queen, and eliminates the possibility of queens on 1 elements
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6* 1x 5x 5x 5x 5x]
 [1x 1x 1x 5x 5x 5  5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1* 5x 3x 3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5x 5x 5x 3  3x 3x]]
2026-05-13 09:43:01,766 [INFO] queens_reasoner::single_color_masking: Color 3 determines its queen
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6* 1x 5x 5x 5x 5x]
 [1x 1x 1x 5x 5x 5  5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1* 5x 3x 3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5x 5x 5x 3* 3x 3x]]
2026-05-13 09:43:01,767 [INFO] queens_reasoner::single_color_masking: Color 5 determines its queen
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6* 1x 5x 5x 5x 5x]
 [1x 1x 1x 5x 5x 5* 5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1* 5x 3x 3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5x 5x 5x 3* 3x 3x]]
2026-05-13 09:43:02,000 [INFO] queens_validator: Setting [queen] on row 1, column 4
2026-05-13 09:43:02,031 [WARNING] queens_validator: Skip setting [queen] on row 2, column 2, since the tile is not enabled
2026-05-13 09:43:02,084 [WARNING] queens_validator: Skip setting [queen] on row 3, column 6, since the tile is not enabled
2026-05-13 09:43:02,710 [INFO] queens_validator: Setting [queen] on row 4, column 1
2026-05-13 09:43:02,798 [INFO] queens_validator: Setting [queen] on row 5, column 3
2026-05-13 09:43:02,858 [INFO] queens_validator: Setting [queen] on row 6, column 7
2026-05-13 09:43:02,947 [INFO] queens_validator: Setting [queen] on row 7, column 5
2026-05-13 09:43:07,042 [INFO] queens_validator: Validation result: SUCCESS
[[1x 1x 1x 4* 5x 5x 5x]
 [6x 6* 1x 5x 5x 5x 5x]
 [1x 1x 1x 5x 5x 5* 5x]
 [2* 2x 1x 5x 5x 3x 5x]
 [1x 1x 1* 5x 3x 3x 3x]
 [5x 5x 5x 5x 5x 3x 7*]
 [5x 5x 5x 5x 3* 3x 3x]]
```

Apart from "single_color_masking", there are other reasoners. To see all of them, please run `pytest -rP --log-cli-level=INFO` for more comprehensive tests on the reasoners.
