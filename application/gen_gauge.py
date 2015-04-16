from application.gauges import *
from PIL import Image


def gauge_maker(diags):
    im = Image.new("RGB", (200, 200), (255, 255, 255))
    g = GaugeDraw(im, 0, 100000)
    g.render_simple_gauge(value=float(diags["Altitude"]), major_ticks=10000, 
                                minor_ticks=5000, label=diags["Altitude"])
    im.save("altitude_gauge.png", "PNG")