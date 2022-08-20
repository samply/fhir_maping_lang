import collections
import re

from lxml import etree


def loadMetaData(file_path):
    """Dynamically generates file structure of an XML file"""
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    for elem in root.getiterator():
        if not (
                isinstance(elem, etree._Comment)
                or isinstance(elem, etree._ProcessingInstruction)
        ):
            elem.tag = etree.QName(elem).localname
    etree.cleanup_namespaces(root)
    raw_tree = etree.ElementTree(root)
    nice_tree = collections.OrderedDict()

    for tag in root.iter():
        path = re.sub('\[[0-9]+\]', '', raw_tree.getpath(tag))
        if path not in nice_tree:
            nice_tree[path] = []
        if len(tag.keys()) > 0:
            nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])
    for path, attribs in nice_tree.items():
        indent = int(path.count('/') - 1)
        print('{0}{1}: {2} [{3}]'.format('    ' * indent, indent, path.split('/')[-1],
                                         ', '.join(attribs) if len(attribs) > 0 else '-'))
    return nice_tree
