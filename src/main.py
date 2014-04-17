#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Marcin Gumkowski, Wojciech Zamozniewicz
'''

import seleshot

if __name__ == '__main__':
    s = seleshot.create()
    url = 'http://www.python.org'

    i = s.get_screen(url)
    i.cut_element(id = 'submit').save('cut1.png')
    i.cut_element(xpath = ".//*[@id='mainnav']/ul/li").save('cut2.png')

    i.cut_area(height = 100).save('area1.png')
    i.cut_area(200, 300, 250, 350).save('area2.png')
    i.cut_area(200, 300, 250, 350).cut_area(60, 60, 50, 50).save('area3.png')

    i.draw_frame(id = 'submit', padding = 10, color = 'yellow', size = 5).save('frame1.png')
    i.draw_frame(coordinates = (500, 500, 40, 50), color = 'green').save('frame2.png')

    i.cut_area(200, 300, 250, 350).draw_dot(coordinates = (50, 50), padding = (10, 4), color = 'yellow', size = 5).draw_dot(coordinates = (60, 20), padding = (10, 4), color = 'red', size = 10).save(
        'dot1.png')

    i.draw_blur(id = 'submit').save('blur1.png')
    i.draw_blur(xpath = ".//*[@id='mainnav']/ul/li").save('blur2.png')

    i.draw_dot(id = 'touchnav-wrapper', padding = (100, 200), size = 100, position = i.MIDDLE).save("dot2M.png")
    i.draw_dot(id = 'submit', padding = (10, -10), size = 3, position = i.MIDDLE).save("dot3M.png")

    i.draw_image(id = 'submit', padding = (0, 0), position = i.OUTSIDE | i.BOTTOM, filename = 'cut1.png').save("image1OB.png")
    i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", padding = (15, 10), position = i.OUTSIDE | i.TOP, filename = 'cut2.png').save("image2OT.png")
    i.draw_image(id = 'touchnav-wrapper', padding = (15, 10), position = i.OUTSIDE | i.LEFT, filename = 'cut2.png').save("image3OL.png")
    i.draw_image(coordinates = (100, 200), padding = (0, 0), position = i.OUTSIDE | i.RIGHT, filename = 'cut1.png').save("image4Cor.png")

    i.draw_zoom(id = 'submit', padding = (0, 5), position = i.OUTSIDE | i.BOTTOM, zoom = 0.5).save("zoom1OB.png")
    i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", padding = (15, 10), position = i.OUTSIDE | i.TOP, zoom = 0.5).save("zoom2OT.png")
    i.draw_zoom(id = 'touchnav-wrapper', padding = (15, 10), position = i.OUTSIDE | i.LEFT, zoom = 0.5).save("zoom3OL.png")

    i.draw_zoom(id = 'submit', padding = (0, 5), position = i.OUTSIDE | i.BOTTOM, zoom = 2).save("zoom4OB.png")
    i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", padding = (15, 10), position = i.OUTSIDE | i.TOP, zoom = 2).save("zoom5OT.png")
    i.draw_zoom(id = 'touchnav-wrapper', padding = (15, 10), position = i.OUTSIDE | i.LEFT, zoom = 1.5).save("zoom6OL.png")
    i.close()
s.close()

