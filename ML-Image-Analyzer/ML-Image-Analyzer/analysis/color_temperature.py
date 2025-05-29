import matplotlib.pyplot as plt
import numpy as np
from utils.color_utils import calculate_color_temperature

def create_color_temperature_figure(centers):
    temperatures = [calculate_color_temperature(*color) for color in centers]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(range(len(temperatures)), temperatures, color=np.array(centers) / 255)
    ax.set_title("Color Temperature (Hue)")
    ax.set_xlabel("Dominant Colors (HEX)")
    ax.set_ylabel("Hue (°)")
    ax.set_xticks(range(len(centers)))
    hex_labels = ['#%02X%02X%02X' % tuple(color) for color in centers]
    ax.set_xticklabels(hex_labels, rotation=45, fontsize=8)
    return fig
