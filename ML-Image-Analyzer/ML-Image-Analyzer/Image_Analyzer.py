import os
import sys

# Get the absolute path to the ML-Image-Analyzer directory
ml_analyzer_dir = os.path.dirname(os.path.abspath(__file__))

# Add the ML-Image-Analyzer directory to Python path
if ml_analyzer_dir not in sys.path:
    sys.path.append(ml_analyzer_dir)

from tkinter import Tk
from gui.gui import ColorAnalyzerApp

def main():
    root = Tk()
    app = ColorAnalyzerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 