"""
We use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The count_tags function returns a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event, element in ET.iterparse(filename):
        if element.tag not in tags:
            tags[element.tag] = 1
        else:
            tags[element.tag] += 1
    return tags

