import xml.etree.ElementTree as ET
import json
from html import unescape
from datetime import datetime
import pathlib
import yaml

if __name__=="__main__":
    import sys
    xml_file = sys.argv[1]
    pages_dir = sys.argv[2]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
          'wp': 'http://wordpress.org/export/1.2/',
          'dc': 'http://purl.org/dc/elements/1.1/'}
    for item_ns in root.findall('.//item'):
        page = {'frontmatter':{}}
        status_ns = item_ns.find('.//wp:status', ns)
        status = status_ns.text if status_ns is not None else ''
        page['frontmatter']['isPublished'] = status != "draft"
        if not page['frontmatter']['isPublished']: continue
        post_type_ns = item_ns.find('.//wp:post_type', ns)
        post_type = post_type_ns.text if post_type_ns is not None else ''
        if post_type != 'page': continue
        page['frontmatter']['title'] = item_ns.find('title').text
        if page['frontmatter']['title'] is None: page['frontmatter']['title'] = 'Untitled'
        page_author = item_ns.find('.//dc:creator', ns).text
        page['frontmatter']['author'] = page_author
        content_encoded = item_ns.find('.//content:encoded', ns)
        page['content'] = unescape(content_encoded.text) if content_encoded is not None and content_encoded.text is not None else ''
        page_pub_date_text = item_ns.find('pubDate').text
        page_pub_date_time = datetime.strptime(page_pub_date_text, "%a, %d %b %Y %H:%M:%S %z")
        page_pub_date = page_pub_date_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        page['frontmatter']['pubDate'] = page_pub_date_time
        page['frontmatter']['sortOrder'] = int(item_ns.find('.//wp:menu_order', ns).text)
        page_link = item_ns.find('link').text
        page_link = page_link[page_link.find("/",8):]
        page_link = page_link[:-1]
        page_path, page_nicename = page_link.rsplit("/", 1)

        pathlib.Path(f"{pages_dir}/{page_path}").mkdir(parents=True, exist_ok=True)
        with open(f"{pages_dir}/{page_path}/{page_nicename}.md", "w", encoding="utf-8") as page_file:
            print("---", file=page_file)
            print(yaml.dump(page['frontmatter']), file=page_file)
            print("---", file=page_file)
            print(page['content'], file=page_file)
