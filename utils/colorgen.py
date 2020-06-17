import random
import colorsys


def get_random_hue(saturation, value):
    hue = random.random()
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)
