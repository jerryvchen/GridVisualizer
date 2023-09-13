import sys
from PySide6.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, 
                               QGraphicsRectItem, QMainWindow, QVBoxLayout, 
                               QWidget, QPushButton)
from PySide6.QtCore import Qt
import random
from typing import List, Tuple

from GridVisualizer_algs import dfs, bfs

class TileType:
    EMPTY: int = 0
    OBSTACLE: int = 1
    START: int = 2
    END: int = 3
    MARK: int = 4
    PATH_MARK: int = 5

class GridVisualizer(QMainWindow):
    def __init__(self, rows: int, cols: int, obstacle_density: float) -> None:
        super().__init__()
        self.__rows: int = rows
        self.__cols: int = cols
        self.__obstacle_density: float = obstacle_density
        self.__grid_vals: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
        self.__grid: List[List[QGraphicsRectItem | None]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.initUI()
        self.show()
        
    def initUI(self) -> None:
        self.setWindowTitle("Grid Visualizer")
        self.central_widget: QWidget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout: QVBoxLayout = QVBoxLayout(self.central_widget)
        self.view: QGraphicsView = QGraphicsView(self.central_widget)
        self.scene: QGraphicsScene = QGraphicsScene()
        self.view.setScene(self.scene)

        # scene size
        self.scene_size: int = 500
        scene_margin: int = 5
        self.view.setMinimumWidth(self.scene_size + scene_margin)
        self.view.setMaximumWidth(self.scene_size + scene_margin)
        self.view.setMinimumHeight(self.scene_size + scene_margin)
        self.view.setMaximumHeight(self.scene_size + scene_margin)
        self.layout.addWidget(self.view)

        # maze stuff
        self.init_maze()

        self.generate_maze_button: QPushButton = QPushButton("Generate New Maze")
        self.generate_maze_button.clicked.connect(self.generate_maze)
        self.layout.addWidget(self.generate_maze_button)

        self.clear_marks_button: QPushButton = QPushButton("Clear Marks")
        self.clear_marks_button.clicked.connect(self.clear_marks)
        self.layout.addWidget(self.clear_marks_button)

        self.dfs_button: QPushButton = QPushButton("Start DFS")
        self.dfs_button.clicked.connect(self.call_DFS_func)
        self.layout.addWidget(self.dfs_button)

        self.bfs_button: QPushButton = QPushButton("Start BFS")
        self.bfs_button.clicked.connect(self.call_BFS_func)
        self.layout.addWidget(self.bfs_button)


    def init_maze(self) -> None:
        """
        Initialize an empty maze.
        """
        cell_size: int = self.scene_size // max(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                rect_item: QGraphicsRectItem = QGraphicsRectItem(col * cell_size, row * cell_size, cell_size, cell_size)
                rect_item.setBrush(Qt.white)
                self.__grid[row][col] = rect_item
                self.scene.addItem(rect_item)
        
        # set START
        self.__grid_vals[0][0] = TileType.START
        self.__grid[0][0].setBrush(Qt.green)

        # set END
        self.__grid_vals[self.rows - 1][self.cols - 1] = TileType.END
        self.__grid[self.rows - 1][self.cols - 1].setBrush(Qt.red)

    def clear_maze(self) -> None:
        """
        Clears the maze.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.__grid_vals[row][col] = TileType.EMPTY
                self.__grid[row][col].setBrush(Qt.white)

        # set START
        self.__grid_vals[0][0] = TileType.START
        self.__grid[0][0].setBrush(Qt.green)

        # set END
        self.__grid_vals[self.rows - 1][self.cols - 1] = TileType.END
        self.__grid[self.rows - 1][self.cols - 1].setBrush(Qt.red)

    def generate_maze(self) -> None:
        """
        Generates a new maze. 
        """
        self.clear_maze()

        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < self.__obstacle_density:
                    self.__grid_vals[row][col] = TileType.OBSTACLE
                    self.__grid[row][col].setBrush(Qt.black)

        # set START
        self.__grid_vals[0][0] = TileType.START
        self.__grid[0][0].setBrush(Qt.green)

        # set END
        self.__grid_vals[self.rows - 1][self.cols - 1] = TileType.END
        self.__grid[self.rows - 1][self.cols - 1].setBrush(Qt.red)

    def clear_marks(self) -> None:
        """
        Clear all marks from the current maze.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__grid_vals[row][col] == TileType.MARK or self.__grid_vals[row][col] == TileType.PATH_MARK:
                    self.__grid_vals[row][col] = TileType.EMPTY
                    self.__grid[row][col].setBrush(Qt.white)
        # set START
        self.__grid_vals[0][0] = TileType.START
        self.__grid[0][0].setBrush(Qt.green)

        # set END
        self.__grid_vals[self.rows - 1][self.cols - 1] = TileType.END
        self.__grid[self.rows - 1][self.cols - 1].setBrush(Qt.red)
        

    def mark(self, row: int, col: int) -> None:
        """
        Marks the maze at the given coordinate.
        
        Should appear yellow. 
        """
        curr_tile_type: int = self.__grid_vals[row][col]
        if curr_tile_type != TileType.OBSTACLE:
            self.__grid_vals[row][col] = TileType.MARK
            self.__grid[row][col].setBrush(Qt.yellow)
        else:
            raise ValueError
        
    def mark_path(self, path: List[Tuple[int, int]]) -> None:
        for coord in path:
            row: int = coord[0]
            col: int = coord[1]
            curr_tile_type: int = self.__grid_vals[row][col]
            if curr_tile_type != TileType.OBSTACLE:
                self.__grid_vals[row][col] = TileType.PATH_MARK
                self.__grid[row][col].setBrush(Qt.blue)
            else:
                raise ValueError
                

    def call_DFS_func(self):
        dfs(self)

    def call_BFS_func(self):
        bfs(self)

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def cols(self) -> int:
        return self.__cols
    
    @property
    def grid(self) -> List[List[int]]:
        return self.__grid_vals
