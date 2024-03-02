import xml.etree.ElementTree as ET
import json
from html import unescape
from datetime import datetime
import pathlib
import yaml

if __name__=="__main__":
    import sys
    xml_file = sys.argv[1]
    posts_dir = sys.argv[2]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
          'wp': 'http://wordpress.org/export/1.2/',
          'dc': 'http://purl.org/dc/elements/1.1/'}
    for post_ns in root.findall('.//item'):
        post = {'frontmatter':{}}
        status_ns = post_ns.find('.//wp:status', ns)
        status = status_ns.text if status_ns is not None else ''
        post['frontmatter']['isPublished'] = status != "draft"
        if not post['frontmatter']['isPublished']: continue
        post_type_ns = post_ns.find('.//wp:post_type', ns)
        post_type = post_type_ns.text if post_type_ns is not None else ''
        if post_type != 'post': continue
        post['frontmatter']['title'] = post_ns.find('title').text
        if post['frontmatter']['title'] is None: post['frontmatter']['title'] = 'Untitled'
        post_author = post_ns.find('.//dc:creator', ns).text
        postmeta_ns = post_ns.findall('.//wp:postmeta', ns)
        for postmeta in postmeta_ns:
            if postmeta.find('.//wp:meta_key', ns).text == 'blogger_author':
                post_author = postmeta.find('.//wp:meta_value', ns).text
        post['frontmatter']['author'] = post_author
        content_encoded = post_ns.find('.//content:encoded', ns)
        post['content'] = unescape(content_encoded.text) if content_encoded is not None and content_encoded.text is not None else ''
        post_pub_date_text = post_ns.find('pubDate').text
        post_pub_date_time = datetime.strptime(post_pub_date_text, "%a, %d %b %Y %H:%M:%S %z")
        post_pub_date = post_pub_date_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        post['frontmatter']['pubDate'] = post_pub_date_time
        post_link = post_ns.find('link').text
        post_link = post_link[post_link.find("/",8)+1:]
        post_link = post_link[:-1]
        post_path, post_nicename = post_link.rsplit("/", 1)

        post_categories = []
        for category in post_ns.findall('.//category[@domain="category"]'):
            post_categories.append(category.get('nicename'))
        post['frontmatter']['categories'] = post_categories
        post_tags = []
        for tag in post_ns.findall('.//category[@domain="post_tag"]'):
            post_tags.append(tag.get('nicename'))
        post['frontmatter']['tags'] = post_tags

        pathlib.Path(f"{posts_dir}/{post_path}").mkdir(parents=True, exist_ok=True)
        with open(f"{posts_dir}/{post_path}/{post_nicename}.md", "w", encoding="utf-8") as post_file:
            print("---", file=post_file)
            print(yaml.dump(post['frontmatter']), file=post_file)
            print("---", file=post_file)
            print(post['content'], file=post_file)
