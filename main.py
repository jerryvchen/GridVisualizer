"""
main.py

Run this file to see things.

:author: Jerry Chen
"""

import sys
from PySide6.QtWidgets import QApplication
from GridVisualizer import GridVisualizer

def main() -> None:
    app = QApplication(sys.argv) 

    # change these maze parameters to whatever you want
    rows: int = 200
    cols: int = 200
    obstacle_density: float = 0.3

    # creates the grid visualizer
    grid_visualizer: GridVisualizer = GridVisualizer(rows, cols, obstacle_density)

    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
