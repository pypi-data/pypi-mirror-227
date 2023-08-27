import html
import requests

def request_html_page(url):
    r = requests.get(url)
    html_content = html.unescape(r.text)
    return html_content
# endDef


def read_html_file(path = "./index.html"):
    with open(path, 'r') as f:
        content = f.read()
    # endWith
    return html.unescape(content)
# endDef


