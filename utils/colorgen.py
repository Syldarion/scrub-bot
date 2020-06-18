import random
import colorsys


def get_random_hue(saturation, value):
    hue = random.random()
    return discord_color_hsv(hue, saturation, value)


def discord_color_hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return discord_color_rgb(r, g, b)


def discord_color_rgb(r, g, b):
    return (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)
