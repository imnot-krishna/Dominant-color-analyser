import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_rgb_scatter_figure(flat_img):
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(flat_img[:, 0], flat_img[:, 1], flat_img[:, 2], c=flat_img / 255.0, marker='.', s=2)
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('3D RGB Scatter Plot')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)
    return fig
