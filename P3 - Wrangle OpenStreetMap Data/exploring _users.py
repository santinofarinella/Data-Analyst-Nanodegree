"""
The function process_map return a set of unique user IDs ("uid"), so we find out how many unique users
have contributed to the map in particular area.
"""

import xml.etree.cElementTree as ET
import pprint
import re

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way" or element.tag == "relation":
            users.add(element.attrib['uid'])

    return users

