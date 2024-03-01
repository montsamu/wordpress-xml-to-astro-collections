import xml.etree.ElementTree as ET
import json
from html import unescape

if __name__=="__main__":
    import sys
    xml_file = sys.argv[1]
    category_dir = sys.argv[2]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
          'wp': 'http://wordpress.org/export/1.2/',
          'dc': 'http://purl.org/dc/elements/1.1/'}
    for category_ns in root.findall('.//wp:category', ns):
        category_nicename = category_ns.find('.//wp:category_nicename', ns).text
        category_name = category_ns.find('.//wp:category_name', ns).text
        category = {"name": category_name}
        with open(f"{category_dir}/{category_nicename}.json", "w") as category_file:
            json.dump(category, category_file)
