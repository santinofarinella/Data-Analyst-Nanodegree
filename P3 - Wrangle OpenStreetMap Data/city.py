"""
- we audit the OSMFILE and change the variable 'mapping' to reflect the changes 
  needed to fix the unexpected city to the appropriate ones. Mappings have been added 
  only for the actual problems found in this OSMFILE, not for a generalized solution, 
  since that may and will depend on the particular area being audited. 
- The update_name function fixes the city name. It takes a string with a city 
  name as an argument and returns the fixed city name. 

"""

import xml.etree.cElementTree as ET
import xlrd

def expected_city(xlsfile,col):
    """ extract from Excel file the city that is possible to find in the area map 
        subject to analysis, expected city    

    Args:
        xlsfile (str): the path to the Excel file, e.g. "...\ComuniCap.xlsx"  
        col(int): spreadsheet column number

    Returns:
        list: the values of the cells in the given column, expected city 

    """
    workbook = xlrd.open_workbook(xlsfile)
    sheet = workbook.sheet_by_index(0)
    city = sheet.col_values(col, start_rowx=1, end_rowx=None)
    return city


mapping = {'Cassina Savina' : 'Cesano Maderno', 
           'Rogorotto' : 'Arluno' , 
           'Sforzesca di Vigevano': 'Vigevano', 
           'Fizzonasco':' Pieve Emanuele', 
           'Valera': 'Arese', 
           'Villaggio Brollo': 'Solaro', 
           "Cassina De'Pecchi" : "Cassina de' Pecchi", 
           'Cantalupo' : 'Cerro Maggiore', 
           'Cavaione di Trucazzano' : 'Cavaione', 
           u'Beccalz\xf9' : 'Casaletto Lodigiano', 
           'Casterno' :  'Robecco sul Naviglio', 
           'Mantegazza': 'Vanzago', 
           'Gugnano' : 'Casaletto Lodigiano', 
           'Stazione' : 'Casaletto Lodigiano', 
           'Cernusco Sul Naviglio' : 'Cernusco sul Naviglio', 
           'Marcallo Con Casone': 'Marcallo con Casone', 
           'Conterico' : ' Paullo', 
           'Ponte Vecchio': 'Magenta' , 
           'Novegro' : 'Segrate', 
           'Pessano Con Bornago' : 'Pessano con Bornago', 
           "Cassina De'Pecchi" : "Cassina de' Pecchi", 
           'Giovenzano' : 'Vellezzo Bellini', 
           'Balbiano' : 'Colturano', 
           'Bovisio Masciago':'Bovisio-Masciago', 
           'Rozzano Vecchia' : "Rozzano"
           }

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")


def audit_city_name(osmfile):
    """get unexpected city
   Args:
        osmfile (str): the path to the osm file,  e.g. "...\milan_italy.osm"   
        
   Returns:
        set: problematic values of the "addr:city" key
      
    """
    osm_file = open(osmfile, "r")
    no_val_city_name = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    city_name = tag.attrib['v'] 
                    if city not in expected:   
                         no_val_city_name.add(city_name)
                    
    osm_file.close()
    return no_val_city_name

def update_name(name, mapping):
    """ Fix  string 'name' with the corrispondent value in the dictionary 
     'mapping' 
     Args:
        name(str): city name string   
        mapping (dict): key is the city name string not corrent and value is the corresponding correct string
     Returns:
        str: city name correct 
      
    """ 
    if mapping.has_key(name):
        name = mapping[name] 
    return name