import matplotlib.colors as mc
import colorsys


def lighten_color(rgb_color, factor=1):
    c = list(rgb_color)
    if len(c) == 4:
        alpha = c[-1]
        c = c[:3]
    else:
        alpha = None
    c = tuple(c)
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    c = colorsys.hls_to_rgb(c[0], 1 - factor * (1 - c[1]), c[2])
    c = list(c)
    if alpha is not None:
        c += [alpha]
    return tuple(c)


def set_transparency(rgb_color, alpha):
    rgb_color = list(rgb_color)
    if len(rgb_color) == 4:
        rgb_color[-1] = alpha
    else:
        rgb_color += [alpha]
    return tuple(rgb_color)
