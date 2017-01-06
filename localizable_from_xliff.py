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


NO_COMMENT_TEXT = "(No Commment)"


def createFullTagName(text):
    return "{urn:oasis:names:tc:xliff:document:1.2}" + text

def start(filename):

	subprocess.run(["xcodebuild", "-exportLocalizations","-localizationPath",".","-project",filename, "-exportLanguage", "en"])

	nodes = Parser.parse("en.xliff")

	root = nodes.getroot()

	with open("Localizable.strings", 'w') as out:

		for f in root:

			if f.attrib['original'].endswith("Localizable.strings"):

				body = f.find(createFullTagName('body'))

				print("--------------------Localizable has {} trans-units--------------------".format(len(body)))

				trans_unit_iter = body.iter(createFullTagName('trans-unit'))

				for trans in trans_unit_iter:
					unit_id = trans.attrib['id']

					note = trans.find(createFullTagName('note'))

					en_target = trans.find(createFullTagName('target'))

					note_text = None

					if len(note.text) != 0:
						note_text = note.text
					else:
						note_text = NO_COMMENT_TEXT

					out.write ('/* ' + note_text + ' */' + '\n')
					out.write ('"' + unit_id + '"' + "=" '"' + en_target.text + '";' + '\n')
					out.write ('\n')

				break



start(filename)

