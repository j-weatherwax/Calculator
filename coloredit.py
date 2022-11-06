import matplotlib.colors as plt
import colorsys

#Makes color of buttons darker when hovered over or pressed
def make_darker(color, percent):
    #convert hexcode to rgb
    r,g,b = plt.to_rgb(color)
    # convert the color hexcode to hsl
    h, l, s = colorsys.rgb_to_hls(r,g,b)
    #increase lightness and convt back to rgb
    rgb = colorsys.hls_to_rgb(h, min(1, l * percent), s = s)
    #return as hex
    return plt.to_hex(rgb)