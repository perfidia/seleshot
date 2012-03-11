from selenium.webdriver.firefox import webdriver
import time
import Image
from selenium import selenium
import os
import argparse

#ids- single string with one id or list of id of DOM element at page; url- ulr with protocol prefix to page(http://..); dir-directory to store tmp and results;
def get_screen(url, ids, path):
    '''
    Get screen shots of ids
    @param url: web page address
    @param ids: list of identifiers (for which a screen shot ought to be taken)
    @param path: place where to store images
    @return: status, a boolen value or list of ids of taken screen shots
    '''

    dir = os.path.abspath(path)
    if not os.path.exists(dir): #create directory if not exsist
        os.makedirs(dir)
    browser = webdriver.WebDriver() # Get local session of firefox
    browser.get(url) # Load page
    tmp_filename = os.path.join(dir , "tmp.png")
    browser.save_screenshot(tmp_filename)
    if isinstance(ids, str):#check against single id not int list 
        ids = [ids]
    for id in ids:#crop regions for all given id or do nothing if error ocured
        try:
            elem = browser.find_element_by_id(id) 
            crop_screnshot(id, elem.location, elem.size, dir)
        except:#do nothing if error ocured during croping or finding id 
            ids.remove(id)
    browser.close()
    if not ids:
        return false
    return ids

#crop_screnshot crop region from temporary file stored in dir at tmp.png 
def crop_screnshot(id, position, size, path):
    '''
    Crop a region for given id and position from image
    @param id: id of element - for naming a output file
    @param position: position on page/screenshot of full page  of given id
    @param size: size of  element of given id
    @param path: place where to store images
    '''
    left = position['x']
    top = position['y']
    right = left + size['width']
    down = top + size['height']
    box = (left, top, right, down) #box of croping region
    tmp_filename = os.path.join(path, "tmp.png")
    img = Image.open(tmp_filename)
    region = img.crop(box)
    elem_filename = os.path.join(path, id + ".png")
    region.save(elem_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url' , dest="url", help="url to web page with protocol like htpp://", required=True)
    parser.add_argument('-i', '--ids', dest="ids", help="list of id in page separated by space ", nargs='+', required=True)
    parser.add_argument('-d', '--path', dest="dir", help="path to save directory; default as run script", default=".")
    args = parser.parse_args()
    get_screen(args.url,args.ids,  args.dir)

#beelow  are Linux system compatibility examples
#get_screen("http://wp.pl",["bxSerwisy","bxWiadomosci","wpCenter"],  "./tmp")
#get_screen("http://onet.pl",["belka_gl","osgs_sidebar_l","bottomContent"],  "./tmp")
#get_screen("http://o2.pl",["sidebar","footer"],  ".")
