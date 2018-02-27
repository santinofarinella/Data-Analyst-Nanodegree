"""
- we audit the OSMFILE and change the variable 'mapping' to reflect the changes 
  needed to fix unexpected street type to the appropriate one in the list expected. Mappings have been added 
  only for the actual problems found in this OSMFILE, not for a generalized solution, 
  since that may and will depend on the particular area being audited. 
- The update_name function fixes the street type. It takes a string with a street
  type as an argument and returns the fixed steet type. 

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# Use regular expression to find certain patterns in the value of "addr:steet", compile a pattern object  
street_type_re = re.compile(r'^\b\S+', re.IGNORECASE)


expected = ["Via","Viale","Corso","Vicolo","Piazza", "Piazzale", "Piazzetta", "Largo","Bastioni"]

mapping = {"via": "Via",
           "Andromeda": "Via Andromeda",           
           "viale": "Viale",
           "Saronnese": "Via Saronnese", 
           "vincenzo" : "Via Vincenzo",
           "piazza" : "Piazza", 
           "VIale": "Viale",
           "VIa" : "Via",
           "Torri": "Via Torri",
           "Stradia" : "Via",
           "San" : "Via San",
           "Gavazzi" : "Viale Riccardo Gavazzi",
           "Dante" : "Via Dante Alighieri",
           "Francesco" : "Via Francesco",
           "Giovanni": "Via Giovanni Verga",
           "Nazionale" : "Via Nazionale",
           "Alessandro" : "Via Alessandro",
           "C.na" : "Via Cascina",
           "Cascina" : "Via Cascina",
           "Circonvallazione" : "Via Circonvallazione",
           "Marzabotto" : "Via Marzabotto",
           "Mazzini" : "Via Mazzini",
           "Mohandas" : "Via Mohandas"
          }


def audit_street_type(street_types, street_name):
    """ add street name to defaultdict if the character pattern specified by the regular expression in the   
        pattern object is not in expected list 
   Args:
       street_types(defaultdict): key is the street type not in expected list and value is set 
       contains corrispondent value of the "addr:street" key    

       street_name(str): value of the "addr:street" key  
        
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
   """  defaultdict with possible problematic in the values of "addr:street" key  

   Args:
        osmfile(str): the path to the osm file,  e.g. "...\milan_italy.osm"  
        
   Returns:
        defaultdict: key is the street type no in the expected list and value is set 
        contains corrispondent value of the "addr:street" key     
      
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
     """ Fix string 'name' with the corrispondent value in the dictionary 
     'mapping' 
     Args:
        name(str): street name string   
        mapping (dict): key is the street type string not corrent and value is the corresponding correct string
     Returns:
        str: street name correct 
      
    """ 
    streetmatch = street_type_re.search(name)
    if streetmatch:
        streettype = streetmatch.group()
        if streettype not in expected and streettype in mapping:        
            name = street_type_re.sub( mapping[streettype], name)
    return name        

