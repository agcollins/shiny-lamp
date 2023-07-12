import re
import xml.etree.ElementTree as ET
import argparse

def pretty_format(element, indent='    ', level=0):
    s = '\n' + indent * level + '<' + element.tag
    if element.attrib:
        s += ' ' + ' '.join(f'{k}="{v}"' for k, v in sorted(element.attrib.items()))
    if len(element) or element.text.strip():
        s += '>' + element.text.lstrip()
        for child in element:
            s += pretty_format(child, indent, level + 1)
        if len(element):
            s += '\n' + indent * level
        s += '</' + element.tag + '>'
    else:
        s += ' />'
    return s

def sort_xml_file(file_path):
    with open(file_path, 'r') as file:
        root = ET.ElementTree(ET.fromstring(re.sub(r'<!--.*?-->', '', file.read(), flags=re.DOTALL))).getroot()
        root[:] = sorted(root, key=lambda e: (e.tag, e.get('name') if e.get('name') else ''))
        return pretty_format(root).lstrip()

def sort_xml_string(xml_string):
    root = ET.ElementTree(ET.fromstring(re.sub(r'<!--.*?-->', '', xml_string, flags=re.DOTALL))).getroot()
    root[:] = sorted(root, key=lambda e: (e.tag, e.get('name') if e.get('name') else ''))
    return pretty_format(root).lstrip()

parser = argparse.ArgumentParser(description='Sort an Android strings XML file.')
parser.add_argument('file', help='The XML file to sort.')
args = parser.parse_args()

print(sort_xml_file(args.file))
