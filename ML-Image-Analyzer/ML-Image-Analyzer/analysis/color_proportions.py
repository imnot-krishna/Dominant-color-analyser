import matplotlib.pyplot as plt
import numpy as np

def create_color_proportions_figure(centers, proportions):
    fig, ax = plt.subplots(figsize=(5, 3))
    start = 0
    bar = np.zeros((50, 500, 3), dtype='uint8')
    for i, (prop, color) in enumerate(zip(proportions, centers)):
        end = start + int(prop * 500)
        bar[:, start:end] = color
        text_color = 'white' if np.mean(color) < 128 else 'black'
        ax.text(start + 5, 30, '#%02X%02X%02X' % tuple(color), rotation=90, fontsize=7,
                verticalalignment='center', color=text_color)
        start = end
    ax.imshow(bar)
    ax.axis('off')
    ax.set_title("Color Proportions with HEX")
    return fig
