"""
- we audit the OSMFILE and change the variable 'mapping' to reflect the changes 
  needed to fix the unexpected postcode to the appropriate ones. Mappings have been added 
  only for the actual problems found in this OSMFILE, not for a generalized solution, 
  since that may and will depend on the particular area being audited. 
- The update_postcode function fixes postcode. It takes a string with a postocode as 
  an argument and returns the fixed postcode. 

"""

import xml.etree.cElementTree as ET
import xlrd

def expected_cap(xlsfile,col):
    """ extract from Excel file the postcode that is possible to find in the area map 
        subject to analysis, expected postcode    

    Args:
        xlsfile (str): the path to the Excel file, e.g. "...\ComuniCap.xlsx" 
        col(int): spreadsheet column number

    Returns:
        list: the values of the cells in the given column, expected postcode 

    """
    workbook = xlrd.open_workbook(xlsfile)
    sheet = workbook.sheet_by_index(0)
    cap = sheet.col_values(col, start_rowx=1, end_rowx=None)
    return cap

mapping = {"2'122":20144, 
           20033 :20832 , 
           20660 :20060, 
           20036 :20063, 
           20038 :20831, 
           20041 :20864, 
           2090 :20092, 
           20043 :20862, 
           20172 : 20127, 
           20048 :20841, 
           20050 :20843, 
           2003 : 20030, 
           20916 : 20861, 
           27070 : 27010, 
           20054 : 20834, 
           2009 : 20092, 
           20052 : 20025 , 
           20059 :20871, 
           22974 : 22074
          }


def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    """get unexpected postcode
   Args:
        osmfile (str): the path to the osm file, e.g. "...\milan_italy.osm"  
        
   Returns:
        set: problematic values of the "addr:postcode" key
      
    """
    osm_file = open(osmfile, "r")
    no_val_addr_postcode = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    postcode = tag.attrib['v'] 
                    try:
                        #convert postcode-like strings to integer value, given that
                        #expected postcode are integer value  
                        postcode = int(postcode)
                        if postcode not in expected:   
                            no_val_addr_postcode.add(postcode)
                    except:
                        #Handle the exception, bad values of "addr:postcode" Key, 
                        #e.g. "2'122" 
                        no_val_addr_postcode.add(postcode)
                        pass

                        
    osm_file.close()
    return no_val_addr_postcode

def update_name(code, mapping):
    """ Fix postcode in string 'code' with the corrispondent value in the dictionary 
     'mapping' 
     Args:
        name(str): postcode string   
        mapping (dict): key is the postcode string not corrent and value is the corresponding correct string
     Returns:
        str: city name correct 
      
    """ 
    if mapping.has_key(code):
        code = mapping[code] 
    return code