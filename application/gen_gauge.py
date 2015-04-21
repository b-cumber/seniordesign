from application.gauges import *
from PIL import Image
from PIL import ImageFilter


def gauge_maker(diags):
    ticks = {'Altitude': 10000, 'Time': None, 'Latitude': None, 'Satellites': None, 'Longitude': None}
    anti_alias = 3
    thickness = 1.4*anti_alias
    width = 160*anti_alias
    height = 160*anti_alias
    for name in diags:
        if ticks[name]:
            im = Image.new("RGB", (width, height), (255, 255, 255))
            g = GaugeDraw(im, 0, 100000)
            g.add_needle(diags[name], needle_fill_color="#FF0000", needle_outline_color="#FF0000")
            g.add_dial(major_ticks=ticks[name], minor_ticks=ticks[name]/2, 
                        dial_format = "%d", dial_thickness=thickness)
            g.render()
            gauge_name = "application/static/" + name + "_gauge.png"
            im.thumbnail((200,200), Image.ANTIALIAS)
            im.save(gauge_name, "PNG")        