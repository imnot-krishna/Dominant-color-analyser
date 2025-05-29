import matplotlib.pyplot as plt

def create_overlay_figure(centers, labels, shape):
    segmented_img = centers[labels].reshape(shape)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.imshow(segmented_img.astype('uint8'))
    ax.axis('off')
    ax.set_title("Color Map Overlay")
    return fig
