import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from tkinter import Tk
from gui.gui import ColorAnalyzerApp

if __name__ == '__main__':
    root = Tk()
    app = ColorAnalyzerApp(root)
    root.mainloop()