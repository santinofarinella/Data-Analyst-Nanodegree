"""
We wrangle the data and transform the shape of the data. The output is a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

The function parses the map file, and call the function with the element
as an argument. The function returns a dictionary, containing the shaped data for that element.
We provide a way to save the data in a file, so that we could use
mongoimport later on to import the shaped data into MongoDB. 

In particular the following things are done:
- we process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" are turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it are ignored
- if the second level tag "k" value starts with "addr:", it are added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", we
  process it without making changes. 
- if there is a second ":" that separates the type/direction of a street,
  the tag are ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  are turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

are turned into
"node_refs": ["305896090", "1719825889"]
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['created'] = {}
        node['type_element'] = element.tag 
        tag_nd_ref = []
        tag_k_address = {}
        for tag_attr in element.attrib:
            if tag_attr in CREATED:
                if tag_attr == "version":
                    node['created'] [tag_attr] = int(element.attrib["version"])   
                else:
                    node['created'] [tag_attr] = element.attrib[tag_attr]        
            elif tag_attr == 'lat' or tag_attr == 'lon':
                 node['pos'] = [float(element.attrib['lat']),float(element.attrib['lon'])]
            else:
                node[tag_attr] = element.attrib[tag_attr]   
        
        for tag in element.iter('tag'):
            tag_k = problemchars.search(tag.attrib['k'])
            if tag_k:
                continue
            elif 'addr:' in tag.attrib['k']:
                if ":" in tag.attrib['k'][5:]:
                    continue
                else:
                    tag_k_address[tag.attrib['k'][5:]] = tag.attrib['v']
                    node['address'] = tag_k_address

            else:
                node[tag.attrib['k']] = tag.attrib['v']
               
        for tag_nd in element.iter('nd'):
            tag_nd_ref.append(tag_nd.attrib['ref'])
            node['node_refs'] = tag_nd_ref
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data



