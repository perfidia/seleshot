#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Marcin Gumkowski, Wojciech Zamozniewicz
'''

import seleshot

if __name__ == '__main__':
    s = seleshot.create()
    url = 'http://www.python.org'

    ##########################################################################
    # Simple screen capture
    ##########################################################################

    i = s.get_screen(url)
    i.save("page.png")

    ##########################################################################
    # Capture element by id or xpath
    ##########################################################################

    i.cut_element(id = 'submit').save('cut1.png')
    i.cut_element(xpath = ".//*[@id='mainnav']/ul/li").save('cut2.png')

    ##########################################################################
    # Capture selected area
    ##########################################################################

    i.cut_area(height = 100).save('area1.png')
    i.cut_area(200, 300, 250, 350).save('area2.png')
    i.cut_area(200, 300, 250, 350).cut_area(70, 120, 50, 100).save('area3.png')

    ##########################################################################
    # Draw a frame by id or xpath
    ##########################################################################

    i.draw_frame(id = 'submit').save('frame1.png')
    i.draw_frame(xpath = ".//*[@id='mainnav']/ul/li", color = 'yellow').save('frame2.png')

    ##########################################################################
    # Draw a frame by coordinates
    ##########################################################################

    i.draw_frame(coordinates = (500, 500, 40, 50), padding = 10, color = 'green', size = 9).save('frame3.png')

    ##########################################################################
    # Draw some dots
    ##########################################################################
    # ... by id

    i.draw_dot(id = 'submit').save("dot1.png")
    i.draw_dot(id = 'submit', size = 10).save("dot2.png")
    i.draw_dot(id = 'submit', size = 10, position = i.OUTSIDE | i.TOP).save("dot3.png")
    i.draw_dot(id = 'submit', size = 10, position = i.BORDER | i.BOTTOM).save("dot4.png")
    i.draw_dot(id = 'submit', size = 10, position = i.BORDER | i.BOTTOM, padding = (10, -10)).save("dot5.png")

    # ... by xpath
    i.draw_dot(xpath = '/html/body/div/div[2]/div/section/div/div[2]/p[2]/a[2]',
             padding = (10, -10), size = 3, position = i.MIDDLE).save("dot6.png")

    # ... by coordinates

    i.draw_dot(coordinates = (500, 500, 40, 50), size = 100, position = i.MIDDLE).save("dot7.png")

    ##########################################################################
    # Combo: cut area and draw some dots
    ##########################################################################

    i.cut_area(200, 300, 250, 350).\
             draw_dot(coordinates = (50, 50), size = 10).\
             draw_dot(coordinates = (60, 20), color = 'pink', size = 17).\
             save('combo1.png')

    ##########################################################################
    # Draw image
    ##########################################################################
    # ... by id

    i.draw_image(id = 'community', filename = 'cut1.png').save("image1.png")
    i.draw_image(id = 'community', filename = 'cut1.png', position = i.OUTSIDE | i.BOTTOM).save("image2.png")
    i.draw_image(id = 'community', filename = 'cut2.png', position = i.OUTSIDE | i.LEFT, padding = (15, 10)).save("image3.png")

    i.draw_image(id = 'touchnav-wrapper', filename = 'cut1.png').save("image4.png")
    i.draw_image(id = 'touchnav-wrapper', filename = 'cut1.png', position = i.OUTSIDE | i.BOTTOM).save("image5-OB.png")
    i.draw_image(id = 'touchnav-wrapper', filename = 'cut2.png', position = i.OUTSIDE | i.LEFT, padding = (15, 10)).save("image6-OL.png")

    # ... by xpath

    i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", filename = 'cut2.png', padding = (15, 10), position = i.OUTSIDE | i.TOP).save("image7-OT.png")

    # ... by coordinates

    i.draw_image(coordinates = (100, 200), padding = (0, 0), position = i.OUTSIDE | i.RIGHT, filename = 'cut1.png').save("image8-OR.png")

    ##########################################################################
    # Draw blur by id or xpath
    ##########################################################################

    i.draw_blur(id = 'submit').save('blur1.png')
    i.draw_blur(xpath = ".//*[@id='mainnav']/ul/li").save('blur2.png')

    ##########################################################################
    # Zoom
    ##########################################################################
    # ... by id

    i.draw_zoom(id = 'submit', zoom = 0.5).save("zoom1.png")
    i.draw_zoom(id = 'submit', zoom = 2).save("zoom2.png")


    i.draw_zoom(id = 'submit', zoom = 0.5, padding = (0, 5), position = i.OUTSIDE | i.BOTTOM).save("zoom3-OB.png")
    i.draw_zoom(id = 'submit', zoom = 2, padding = (0, 5), position = i.OUTSIDE | i.BOTTOM).save("zoom4-OB.png")

    i.draw_zoom(id = 'touchnav-wrapper', zoom = 0.5, padding = (15, 10), position = i.OUTSIDE | i.LEFT).save("zoom5-OL.png")
    i.draw_zoom(id = 'touchnav-wrapper', zoom = 1.5, padding = (15, 10), position = i.OUTSIDE | i.LEFT).save("zoom6-OL.png")

    # ... by xpath

    i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 0.5, padding = (15, 10), position = i.OUTSIDE | i.TOP).save("zoom7-OT.png")
    i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 2.0, padding = (15, 10), position = i.OUTSIDE | i.TOP).save("zoom8-OT.png")

    ##########################################################################
    # end, closing driver
    ##########################################################################

    s.close()

    print "done"
