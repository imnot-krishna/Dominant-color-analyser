import os
import sys

# Get the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from tkinter import Tk
from gui.gui import ColorAnalyzerApp

if __name__ == '__main__':
    root = Tk()
    app = ColorAnalyzerApp(root)
    root.mainloop() 