"""
- we audit the OSMFILE and change the variable 'mapping' to reflect the changes 
  needed to fix the street name includes a date to the correct one. Mappings have been added 
  only for the actual problems found in this OSMFILE, not for a generalized solution, 
  since that may and will depend on the particular area being audited. 
- The update_name function fixes the street name. It takes a string with a street
  name as an argument and returns the fixed steet name. 
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# Use regular expression to find if the value of "addr:steet" includes a date, compile a pattern object  
street_date_re = re.compile(r'gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre',
                            re.IGNORECASE)


mapping = { 'Piazza Ventiquattro Maggio':"Piazza 24 maggio",
            'Via 2 Giugno': 'Via 2 giugno', 
            'Via XX Settembre':'Via 20 settembre', 
            'Via 20 Settembre':'Via 20 settembre', 
            'Piazza otto novembre': 'Piazza 8 novembre',
            'Via 8 Ottobre 2001':'Via 8 ottobre', 
            'Piazza 4 Novembre':'Piazza 4 novembre', 
            'Corso Ventidue Marzo': 'Via 22 marzo',
            'Largo IV Novembre':'Largo 4 Novembre',
            'Piazza IV Novembre':'Piazza 4 novembre',  
            'Via IV Novembre':'Via 4 novembre', 
            'via IV Novembre' : 'Via 4 novembre' , 
            'Piazza Quattro Novembre' : 'Piazza 4 novembre', 
            'Via 4 Novembre': 'Via 4 novembre',    
            'Via 24 Maggio':'Via 24 maggio', 
            'Via XXIV Maggio':'Via 24 Maggio', 
            'Via privata 24 Maggio' : 'Via privata 24 maggio', 
            'Via 25 Aprile':'Via 25 aprile',
            'Largo XXV Aprile': 'Largo 25 aprile', 
            'Vicolo XXV Aprile':'Vicolo 25 aprile',
            'Piazza XXV Aprile': 'Via 25 aprile', 
            'Via VIII Aprile': 'Via 8 aprile', 
            'Via Venticinque Aprile' : 'Via 25 aprile', 
            'Via XXV Aprile':'Via 25 aprile', 
            'Via XXV Aprile angolo Via Tiziano': 'Via 25 aprile',
            'Piazza 25 Aprile': 'Piazza 25 aprile',  
            'Piazza Primo Maggio': u'Piazza 1\xb0 maggio',
            u'Via 1\xb0 Maggio' : u'Via 1\xb0 maggio' , 
            'Via I Maggio' :  u'Via 1\xb0 maggio', 
            'Via Primo Maggio': u'Via 1\xb0 maggio'        
           }



def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_date(osmfile):
    """get the values of "addr:steet" that matches the character patterns specified by the regular expression.
 
   Args:
        osmfile (str): the path to the osm file,  e.g. "...\milan_italy.osm"   
        
   Returns:
        set: values of the "addr:street" key that include a date 
      
    """   
    osm_file = open(path, "r")
    street_date_ = set()
    for event, element in ET.iterparse(osm_file, events=("start",)):
        if element.tag == "node" or element.tag == "way":
            for tag in element.iter("tag"):
                if is_street_name(tag):
                    date = tag.attrib['v']
                    street_date_match = street_date_re.search(date)
                    if street_date_match:
                        steret_date.add(date)
    
    return  street_date

def update_name(name_street, mapping):
    """ Fix name in string 'name_steet' with the corrispondent value in the dictionary 
     'mapping' 
     Args:
        name_street(str): name street string   
        mapping (dict): key is the street name string not corrent and value is the corresponding correct string
     Returns:
        str: street name correct 
      
    """ 
    if mapping.has_key(name_street):
        name_street = mapping[name_street]  
    return name_street