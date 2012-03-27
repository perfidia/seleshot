# -*- coding: utf-8 -*-

from Xml2Json import Xml2Json
from selenium.webdriver.firefox import webdriver
import time
import Image
from selenium import selenium
import os
import argparse
import re
from xml.dom.minidom import parseString
from xml.dom.minidom import Document
import pickle

def parseCode(htmlCode,dir,id,set):
    #print set
    if set == "json":
        tojson(htmlCode,dir,id)
    else:
        parsing(htmlCode,dir,id)  
        
        
def parsing(html,dir,id):
    html = html.decode("utf-8", "replace")
    html = re.sub(r'(<img[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    html = re.sub(r'(<br[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    html = re.sub(r'(<hr[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    dom = parseString(html)
    pars(dom.firstChild)
    processedString = dom.toprettyxml(encoding="utf-8")
    #TODO: regexp to delete whitespace lines
    processedString = re.sub("^\n$", "", processedString)
    plik = open(dir + id + '.xml', 'w')
    plik.write(processedString)
    plik.close()
    print "xml saved"
    #print dom.toprettyxml()
    
def pars(dom):
    if dom.childNodes.length > 1:
        for node in dom.childNodes:
            if node.nodeType == node.TEXT_NODE:
                doc = Document()
                text = doc.createElement("text")
                textval = re.sub(r'[ \n\t]+', ' ', node.nodeValue)
                intext = doc.createTextNode(textval)
                text.appendChild(intext)
                dom.replaceChild(text, node)
            else:
                pars(node)


def tojson(html,dir,id):
    html = html.decode("utf-8", "replace")
    html = re.sub(r'(<img[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    html = re.sub(r'(<br[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    html = re.sub(r'(<hr[^>]+)(>)', lambda m: "%s/>" % m.group(1), html)
    dom = parseString(html)
    pars(dom.firstChild)
    json(dom.firstChild)
    x = str(dom.toxml())
    j = Xml2Json(x[22:]).result
    plik = open(dir + id + '.json', 'w')
    plik.write(str(j))
    plik.close()
    
    
def json(dom):
    if dom.nodeType is not dom.TEXT_NODE:
        if dom.hasAttributes():
            for i in range(dom.attributes.length):
                doc = Document()
                name = doc.createElement(dom.attributes.item(i).name)
                if dom.attributes.item(i).name != "href":
                    value = doc.createTextNode(dom.attributes.item(i).value)
                    name.appendChild(value)
                    dom.appendChild(name)
            for i in xrange(dom.attributes.length-1, -1, -1):
                dom.removeAttribute(dom.attributes.item(i).name)
            for node in dom.childNodes:
                json(node)

#ids- single string with one id or list of id of DOM element at page; url- ulr with protocol prefix to page(http://..); dir-directory to store tmp and results;
def get_screen(url, ids, path,set):
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
    #if isinstance(ids, str):#check against single id not int list 
    #    ids = [ids]
    for id in ids:#crop regions for all given id or do nothing if error ocured
    #try:
        print id
        matchObj = re.match(r'(.*)/(.*)', id, re.IGNORECASE)
        if matchObj:
            elem = browser.find_element_by_xpath(id)
            crop_screnshot(id, elem.location, elem.size, dir)
            
        else:
            elem = browser.find_element_by_id(id) 
            crop_screnshot(id, elem.location, elem.size, dir)
            htmlCode = browser.execute_script('return document.getElementById("'+id+'").outerHTML')
            parseCode(htmlCode,dir,id,set)

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
    matchObj = re.match(r'(.*)/(.*)', id, re.IGNORECASE)
    if matchObj:
        elem_filename = os.path.join(path + "xpath.png")
    else:
        elem_filename = os.path.join(path, id + ".png")
        
    region.save(elem_filename)
    print "image saved"
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url' , dest="url", help="url to web page with protocol like htpp://", required=True)
    parser.add_argument('-i', '--ids', dest="ids", help="list of id in page separated by space ", nargs='+', required=True)
    parser.add_argument('-d', '--path', dest="dir", help="path to save directory; default as run script", default=".")
    parser.add_argument('-s', '--sett', dest="set", help="choose a code's output [opt: xml, json]", default="xml")
    args = parser.parse_args()
    get_screen(args.url, args.ids, args.dir, args.set)
    #get_screen("http://kinyen.pl",["//div[@id='header']"], "C://", "json")

#beelow  are Linux system compatibility examples
#get_screen("http://kinyen.pl", ["header"], "C://", "xml") will save a header png image and header.json outerHtml code
#get_screen("http://kinyen.pl","//div[@id='header']", "C://", "json") will save a header png image and header.xml outerHtml code [element found by xpath]

#Debuging run arguments can be provide like:
#-u http://kinyen.pl -i header -d C:// -s json
