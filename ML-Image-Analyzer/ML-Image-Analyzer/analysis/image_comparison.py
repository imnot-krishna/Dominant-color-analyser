import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt

def compare_images(image1, image2):
    """Compare two images using multiple metrics."""
    # Ensure images are the same size
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    # Convert to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    ssim_score = ssim(gray1, gray2)

    # Calculate histogram similarity
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    
    # Normalize histograms
    hist1 = hist1.ravel() / hist1.sum()
    hist2 = hist2.ravel() / hist2.sum()
    
    # Calculate Earth Mover's Distance (Wasserstein distance)
    emd = wasserstein_distance(np.arange(256), np.arange(256), hist1, hist2)

    # Calculate color histograms for each channel
    color_similarity = {}
    for i, color in enumerate(['blue', 'green', 'red']):
        hist1 = cv2.calcHist([image1], [i], None, [256], [0, 256])
        hist2 = cv2.calcHist([image2], [i], None, [256], [0, 256])
        hist1 = hist1.ravel() / hist1.sum()
        hist2 = hist2.ravel() / hist2.sum()
        color_similarity[color] = 1 - wasserstein_distance(np.arange(256), np.arange(256), hist1, hist2)

    # Create comparison visualization
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes[0, 0].imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Image 1')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 2')
    axes[0, 1].axis('off')
    
    # Show difference map
    diff = cv2.absdiff(gray1, gray2)
    axes[1, 0].imshow(diff, cmap='hot')
    axes[1, 0].set_title('Difference Map')
    axes[1, 0].axis('off')
    
    # Add text with similarity metrics
    axes[1, 1].text(0.1, 0.8, f'SSIM Score: {ssim_score:.3f}', fontsize=10)
    axes[1, 1].text(0.1, 0.6, f'Histogram EMD: {emd:.3f}', fontsize=10)
    for i, (color, score) in enumerate(color_similarity.items()):
        axes[1, 1].text(0.1, 0.4 - i*0.2, f'{color.capitalize()} Similarity: {score:.3f}', fontsize=10)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    return {
        'ssim_score': ssim_score,
        'histogram_emd': emd,
        'color_similarity': color_similarity,
        'comparison_figure': fig
    } 