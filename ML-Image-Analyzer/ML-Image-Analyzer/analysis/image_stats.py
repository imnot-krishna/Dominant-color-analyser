import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy

def calculate_image_statistics(image):
    """Calculate advanced image statistics including texture analysis."""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Basic statistics
    mean = np.mean(gray)
    std = np.std(gray)
    entropy = shannon_entropy(gray)

    # Texture analysis using GLCM
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(gray, distances, angles, 256, symmetric=True, normed=True)
    
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]

    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

    return {
        "mean_intensity": mean,
        "std_deviation": std,
        "entropy": entropy,
        "contrast": contrast,
        "homogeneity": homogeneity,
        "correlation": correlation,
        "energy": energy,
        "edge_density": edge_density
    } 