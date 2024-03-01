import xml.etree.ElementTree as ET
import json
from html import unescape

if __name__=="__main__":
    import sys
    xml_file = sys.argv[1]
    author_dir = sys.argv[2]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
          'wp': 'http://wordpress.org/export/1.2/',
          'dc': 'http://purl.org/dc/elements/1.1/'}
    for author_ns in root.findall('.//wp:author', ns):
        author_login = author_ns.find('.//wp:author_login', ns).text
        author_email = author_ns.find('.//wp:author_email', ns).text
        author_display_name = author_ns.find('.//wp:author_display_name', ns).text
        author_last_name = author_ns.find('.//wp:author_last_name', ns).text
        author_first_name = author_ns.find('.//wp:author_first_name', ns).text
        author = {"email": author_email,
                  "display_name": author_display_name,
                  "last_name": author_last_name,
                  "first_name": author_first_name}
        with open(f"{author_dir}/{author_login}.json", "w") as author_file:
            json.dump(author, author_file)
