import colorsys

def calculate_color_temperature(r, g, b):
    hsv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return hsv[0] * 360
