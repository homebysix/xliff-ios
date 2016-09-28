# # -*- coding: utf-8 -*-

import lxml.etree as Parser, os
from lxml import etree
import sys

try:
    filename = sys.argv[1]
except IndexError:
    print ("You must supply a file name.")
    sys.exit(2)

def createFullTagName(text):
    return "{urn:oasis:names:tc:xliff:document:1.2}" + text

def do_something_with_file(filename):
    nodes = Parser.parse(filename)
    root = nodes.getroot()
    with open("Localizable.strings", 'w') as out:
 
	    for f in root:
	    	if f.attrib['original'].endswith("Localizable.strings"):
		    	body = f.find(createFullTagName('body'))
		    	for trans in body.iter(createFullTagName('trans-unit')):
		    		note = trans.find(createFullTagName('note'))
		    		source = trans.find(createFullTagName('source'))

		    		note_text = ""
		    		if note != None and len(note.text) != 0:
		    			note_text = note.text
		    		else:
		    			note_text = "No comment provided by engineer."
		    		out.write ('/* ' + note_text + ' */' + '\n')
		    		out.write ('"' + source.text + '"' + "=" '"' + source.text + '";' + '\n')
		    		out.write ('\n')



do_something_with_file(filename)

