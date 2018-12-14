# Escaping special characters in XML files.
# for the list of special characters see
# https://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references#Predefined_entities_in_XML

import xml.etree.ElementTree as etree
from xml.etree.ElementTree import _escape_cdata, _raise_serialization_error
from mock import patch


def _escape_cdata(text):
    # escape character data
    try:
        # it's worth avoiding do-nothing calls for strings that are
        # shorter than 500 character, or so.  assume that's, by far,
        # the most common case in most applications.
        if "&" in text:
            text = text.replace("&", "&amp;")
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        if "'" in text:
            text = text.replace("'", "&apos;")
        if '"' in text:
            text = text.replace('"', "&quot;")
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


tree = etree.parse('input.xml')
root = tree.getroot()

s = ''
with patch('xml.etree.ElementTree._escape_cdata', new=_escape_cdata):
    s = etree.tostring(root, encoding="UTF-8", method="xml")

with open('output.xml', 'wb') as o:
    o.write('<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'))
    o.write(s)
