import xml.etree.ElementTree as ET
import json
from html import unescape

if __name__=="__main__":
    import sys
    xml_file = sys.argv[1]
    tag_dir = sys.argv[2]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
          'wp': 'http://wordpress.org/export/1.2/',
          'dc': 'http://purl.org/dc/elements/1.1/'}
    for tag_ns in root.findall('.//wp:tag', ns):
        tag_nicename = tag_ns.find('.//wp:tag_slug', ns).text
        tag_name = tag_ns.find('.//wp:tag_name', ns).text
        tag = {"name": tag_name}
        with open(f"{tag_dir}/{tag_nicename}.json", "w") as tag_file:
            json.dump(tag, tag_file)
