# # -*- coding: utf-8 -*-

import lxml.etree as Parser, os
from lxml import etree
import sys
import subprocess


try:
    filename = sys.argv[1]
except IndexError:
    print ("You must supply the xcode project path.")
    sys.exit(2)


NO_COMMENT_TEXT = "(No Comment)"


def createFullTagName(text):
    return "{urn:oasis:names:tc:xliff:document:1.2}" + text

def start(filename):

	subprocess.run(["xcodebuild", "-exportLocalizations","-localizationPath",".","-project",filename, "-exportLanguage", "en"])

	nodes = Parser.parse("en.xliff")

	root = nodes.getroot() # switch to xliff node

	with open("Localizable.strings", 'w') as out:

		for f in root:

			if f.attrib['original'].endswith("Localizable.strings"):

				body = f.find(createFullTagName('body'))

				translation_list = []

				for trans in body.iter(createFullTagName('trans-unit')):

					unit_id = trans.attrib['id']

					note = trans.find(createFullTagName('note'))

					en_target = trans.find(createFullTagName('target'))

					note_text = None

					if note != None and len(note.text) != 0:
						note_text = note.text
					else:
						note_text = NO_COMMENT_TEXT

					translation_list.append((note_text,unit_id,en_target.text))

				print("--------------------Localizable has {} trans-units--------------------".format(len(translation_list)))
				
				translation_list.sort()

				for unit in translation_list:
					out.write ('/* ' + unit[0] + ' */' + '\n')
					out.write ('"' + unit[1] + '"' + "=" '"' + unit[2] + '";' + '\n')
					out.write ('\n')

				break



start(filename)

