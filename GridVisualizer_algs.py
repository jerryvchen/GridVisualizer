"""
GridVisualizer_algs.py

Ok ur brother is at it again. I'm not the best at building programs yet so you'll have to do without autocomplete, whoops.
The start of a maze will always be at (0, 0), and the ending will always be at (rows - 1, cols - 1).
Your job is to create a dfs AND bfs algorithm which marks the grid, stopping when it reaches the end. 

Relevent functions for grid: 
- Properties (call it using grid.rows, NOT grid.rows())
    - rows
        - returns the number of rows on the grid
    - cols
        - returns the number of columns on the grid 
    - grid
        - returns a 2D List of integers. See the TileTypes class for what each number means. 
- Functions
    - mark(self, row: int, col: int) -> None:
        - marks the grid at the given coordinate
        - appears in YELLOW
        - can mark anything EXCEPT obstacles

    - mark_path(self, path: List[Tuple])
        - given a list of coordinates, marks those points (points should be a tuple of two, as (row, col))
        - appears in BLUE
        - can mark anything EXCEPT obstacles

Good Luck!
"""

from collections import deque
from typing import Dict, List, Set, Tuple

class TileType:
    """
    When you use grid.grid to check if a tile is blocked, check if grid[row][col] == TileType.OBSTACLE
    """
    EMPTY: int = 0      # white
    OBSTACLE: int = 1   # black
    START: int = 2      # green
    END: int = 3        # red
    MARK: int = 4       # yellow
    PATH_MARK: int = 5  # blue


def dfs(grid):
    """
    Performs a DFS on the grid. 

    You should mark each tile that you've visited.
    When you find the end, override the necessary marked tiles that form a path.
    """
    # stack: List[Tuple[int, int]] = []
    # dfs_util(grid, (0, 0), stack)

    call_stack: List[Tuple[int, int]] = [(0, 0)]
    path_stack = []
    
    while call_stack:
        dfs_util_iter(grid, call_stack.pop(), call_stack, path_stack)

def dfs_util_iter(grid, coord, call_stack, path_stack):
    row, col = coord
    if row < 0 or col < 0 or row >= grid.rows or col >= grid.cols:
        return # out of bounds
    if grid.grid[row][col] == TileType.MARK or grid.grid[row][col] == TileType.PATH_MARK:
        return # already visited
    if grid.grid[row][col] == TileType.OBSTACLE:
        return # obstacle
    
    # mark current cell as visited
    grid.mark(row, col)
    path_stack.append(coord)

    if coord == (grid.rows - 1, grid.cols - 1): 
        # reached the end, so recreate path
        grid.mark_path(path_stack)
        call_stack.clear()
        return # reached the end

    # explore neighbors
    call_stack.append((row - 1, col))
    call_stack.append((row + 1, col))
    call_stack.append((row, col - 1))
    call_stack.append((row, col + 1))


def dfs_util(grid, coord, stack) -> None:
    row, col = coord
    if row < 0 or col < 0 or row >= grid.rows or col >= grid.cols:
        return # out of bounds
    if grid.grid[row][col] == TileType.MARK or grid.grid[row][col] == TileType.PATH_MARK:
        return # already visited
    if grid.grid[row][col] == TileType.OBSTACLE:
        return # obstacle
    
    # mark current cell as visited
    grid.mark(row, col)
    stack.append(coord)

    if coord == (grid.rows - 1, grid.cols - 1): 
        # reached the end, so recreate path
        grid.mark_path(stack)
        return # reached the end

    # explore neighbors
    dfs_util(grid, (row - 1, col), stack)
    dfs_util(grid, (row + 1, col), stack)
    dfs_util(grid, (row, col - 1), stack)
    dfs_util(grid, (row, col + 1), stack)

    stack.pop()

def bfs(grid):
    """
    Performs a BFS on the grid. 

    You should mark each tile that you've visited.
    When you find the end, override the necessary marked tiles that form a path.
    """
    backtrack = dict()
    backtrack[(0,0)] = None

    q = deque([(0, 0)])

    while q:
        row, col = q.popleft()

        if row < 0 or col < 0 or row >= grid.rows or col >= grid.cols:
            continue # out of bounds
        if grid.grid[row][col] == TileType.MARK or grid.grid[row][col] == TileType.PATH_MARK:
            continue # already visited 
        if grid.grid[row][col] == TileType.OBSTACLE:
            continue # obstacle

        grid.mark(row, col)
        
        if (row, col) == (grid.rows - 1, grid.cols - 1):
            path = []
            curr = (row, col)
            while curr:
                path.append(curr)
                curr = backtrack[curr]
            grid.mark_path(path)
            return 
        
        # add neighbors
        q.append((row - 1, col))
        q.append((row + 1, col))
        q.append((row, col - 1))
        q.append((row, col + 1))

        if (row - 1, col) not in backtrack:
            backtrack[row - 1, col] = (row, col)
        if (row + 1, col) not in backtrack:
            backtrack[row + 1, col] = (row, col)
        if (row, col - 1) not in backtrack:
            backtrack[row, col - 1] = (row, col)
        if (row, col + 1) not in backtrack:
            backtrack[row, col + 1] = (row, col)

    # backtrack: Dict[Tuple[int, int], Tuple[int, int] | None] = dict() # to reconstruct path, holds as (coord, parent_coord)

    # seen: Set[Tuple[int, int]] = set()
    # q: deque[Tuple[int, int]] = deque([])
    # q.append((0, 0))

    # while q:
    #     curr_len: int = len(q)
    #     for _ in range(curr_len):
    #         curr_row: int
    #         curr_col: int
    #         curr_row, curr_col = q.popleft()

    #         seen.add((curr_row, curr_col))
    #         grid.mark(curr_row, curr_col)

    #         if curr_row == grid.rows - 1 and curr_col == grid.cols - 1: # last one
    #             q.clear()
    #             break

    #         if curr_row - 1 >= 0 and grid.grid[curr_row - 1][curr_col] != TileType.OBSTACLE and (curr_row - 1, curr_col) not in seen:
    #             q.append((curr_row - 1, curr_col))
    #             backtrack[(curr_row - 1, curr_col)] = (curr_row, curr_col)

    #         if curr_row + 1 < grid.rows and grid.grid[curr_row + 1][curr_col] != TileType.OBSTACLE and (curr_row + 1, curr_col) not in seen:
    #             q.append((curr_row + 1, curr_col))
    #             backtrack[(curr_row + 1, curr_col)] = (curr_row, curr_col)

    #         if curr_col - 1 >= 0 and grid.grid[curr_row][curr_col - 1] != TileType.OBSTACLE and (curr_row, curr_col - 1) not in seen:
    #             q.append((curr_row, curr_col - 1))
    #             backtrack[(curr_row, curr_col - 1)] = (curr_row, curr_col)

    #         if curr_col + 1 < grid.cols and grid.grid[curr_row][curr_col + 1] != TileType.OBSTACLE and (curr_row, curr_col + 1) not in seen:
    #             q.append((curr_row, curr_col + 1))
    #             backtrack[(curr_row, curr_col + 1)] = (curr_row, curr_col)

    
    # backtrack[(0, 0)] = None
    # # mark path if it exists
    # if (grid.rows - 1, grid.cols - 1) in backtrack:
    #     # reconstruct path from backtrack
    #     path: List[Tuple[int, int]] = []
    #     curr: Tuple[int, int] = (grid.rows - 1, grid.cols - 1)
    #     while curr is not None:
    #         path.append(curr)
    #         curr = backtrack[curr]
    #     grid.mark_path(path)

    