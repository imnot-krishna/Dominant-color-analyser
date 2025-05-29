import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter1d
import numpy as np

def create_brightness_figures(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.hist(gray.ravel(), bins=256, range=[0, 256], color='gray')
    ax1.set_title("Brightness Distribution")
    ax1.set_xlabel("Brightness (0-255)")
    ax1.set_ylabel("Pixel Count")

    hist, bins = np.histogram(gray.ravel(), bins=256, range=[0, 256])
    smooth_hist = gaussian_filter1d(hist, sigma=2)

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.plot(bins[:-1], smooth_hist, color='blue')
    ax2.set_title("Smoothed Brightness Histogram")
    ax2.set_xlabel("Brightness (0-255)")
    ax2.set_ylabel("Smoothed Pixel Count")

    return fig1, fig2
