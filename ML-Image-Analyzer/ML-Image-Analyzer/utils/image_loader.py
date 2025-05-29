from PIL import Image, ImageTk

def load_image_thumbnail(path, size=(220, 220)):
    img = Image.open(path)
    img.thumbnail(size)
    return ImageTk.PhotoImage(img)
