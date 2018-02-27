import xml.etree.cElementTree as ET
import xlrd
import pprint
from bs4 import BeautifulSoup



def extract_tag_value(html_page,key_string):
    """ extract from html file the listing of values provides by OSM Map Features page for particular key, 
        thematic attributes for real geographic object.
        A tag consists of two items, a key and a value, e.g. <tag k="highway" v="motorway_junction"/>, key = "highway" 
        value = "motorway_junction".
    
    Args:
        html_page (str): path to the html file, e.g. "...\Key_building - OpenStreetMap Wiki.html" 
        key_string(str): key tag choice   
    
    Returns:
        set: expected values of the key tag choice 
    """
    value = set()
    with open(html_page, "r") as html:
        soup = BeautifulSoup(html,'lxml')
        table = soup.find('table',{'class':'wikitable'})
        for key_tag in table.find_all('a'):
            title = key_tag.get('title')
            # Handling Exceptions "TypeError: argument of type 'NoneType' is not iterable"
            try:
                if 'Tag:' + key_string in title:
                    text = key_tag.string.strip() # eliminate all the whitespace from string
                    value.add(text)
            except:
                   pass 
        # key is not extract by web scraping techniques
        if key_string == 'building':
           value.add('yes') 
    
    return value
    

def is_tag_key(elem,key_string):
    return (elem.attrib['k'] == key_string)


def audit(osmfile):
    """get values of key does not provide by OSM Map Features page
   Args:
        osmfile (str): the path to the osm file,  e.g. "...\milan_italy.osm"   
        
   Returns:
        set: unexpected values of the key tag choice
      
    """
    osm_file = open(osmfile, "r")
    value = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_tag_key(tag,key_string):
                    tag_value = tag.attrib['v'] 
                    if tag_value not in expected:   
                        value.add(tag_value)
                    
    osm_file.close()
    return value

