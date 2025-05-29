from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os
import cv2

from analysis.color_proportions import create_color_proportions_figure
from analysis.brightness import create_brightness_figures
from analysis.color_temperature import create_color_temperature_figure
from analysis.overlay import create_overlay_figure
from analysis.scatter_rgb import create_rgb_scatter_figure
from utils.color_utils import calculate_color_temperature

def analyze_image(image_path, cluster_count):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_img = cv2.resize(img_rgb, (200, 200))
    flat_img = resized_img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=cluster_count, random_state=0)
    labels = kmeans.fit_predict(flat_img)
    centers = np.array(kmeans.cluster_centers_, dtype='uint8')
    proportions = np.bincount(labels) / len(labels)

    info_data = []
    for i, (prop, color) in enumerate(zip(proportions, centers)):
        hex_val = '#%02x%02x%02x' % tuple(color)
        info_data.append({
            "Index": i + 1,
            "RGB": tuple(int(x) for x in color),
            "HEX": hex_val,
            "%": round(prop * 100, 2)
        })

    df = pd.DataFrame(info_data)
    csv_path = os.path.splitext(image_path)[0] + "_color_analysis.csv"
    df.to_csv(csv_path, index=False)

    figures = {
        "Proportions": create_color_proportions_figure(centers, proportions),
        "Brightness Distribution": create_brightness_figures(img)[0],
        "Smoothed Brightness": create_brightness_figures(img)[1],
        "Temperature (Hue)": create_color_temperature_figure(centers),
        "Overlay": create_overlay_figure(centers, labels, resized_img.shape),
        "3D RGB Scatter": create_rgb_scatter_figure(flat_img),
    }

    return {"csv_path": csv_path, "figures": figures}
