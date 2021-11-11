from lxml import etree


def parse_xml(content):
    raw = {}
    root = etree.fromstring(content, parser=etree.XMLParser(resolve_entities=False))
    for child in root:
        raw[child.tag] = child.text
    return raw
