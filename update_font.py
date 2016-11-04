# # -*- coding: utf-8 -*-

import lxml.etree as os
from lxml import etree
import sys
import glob, os


try:
    filename = sys.argv[1]
except IndexError:
    print ("You must supply a file or directory name.")
    sys.exit(2)

def addCustomFonts(customFonts,fontFileName,fontName):

    array = etree.SubElement(customFonts, "array",  attrib={"key": fontFileName})

    string = etree.SubElement(array, "string")

    string.text = fontName


def updateFile(filename):

    parser = etree.XMLParser(remove_blank_text=True)
    nodes = etree.parse(filename, parser)
    root = nodes.getroot()


    customFont = root.find("customFonts")
    if customFont == None:
        customFont = etree.Element("customFonts")
        root.insert(1, customFont)


    existFonts = []

    for family in customFont.iter("array"):
        print ("GOING THRO {}".format(family.attrib["key"]))
        fontName = family.find("string").text
        if "Gibson" not in fontName:
            customFont.remove(family)
        else:
            existFonts.append(fontName)

    elementFonts = root.findall(".//fontDescription")


    systemFontChangesCount = 0
    customFontChangesCount = 0

    for fontSetting in elementFonts:

        print ("WAS: {}".format(fontSetting.attrib))

        isSystemFont = (fontSetting.attrib.get("type") == "system")

        if isSystemFont:
            systemFontWeight = fontSetting.attrib.get("weight")  
            fontSetting.attrib.pop('type', None)
            fontSetting.attrib.pop('weight', None)
            systemFontChangesCount += 1
        elif fontSetting.attrib.get("family") == "Gibson":
            continue
        else:
            customFontChangesCount += 1

        pointSize = fontSetting.attrib.get("pointSize")

        family = "Gibson"
        oldFontName = fontSetting.attrib.get("name")


        if oldFontName != None:
            oldFontName = oldFontName.lower()
            if "light" in oldFontName:
                name = "Gibson-Light"
            elif "bold" in oldFontName or "bd" in oldFontName:
                name = "Gibson-Bold"
            else:
                name = "Gibson-Regular"
        elif systemFontWeight!=None:
            if "light" in systemFontWeight:
                name = "Gibson-Light"
            elif "bold" in systemFontWeight:
                name = "Gibson-Bold"
            else:
                name = "Gibson-Regular"
        else:
            name = "Gibson-Regular"

        fontSetting.attrib["pointSize"] = pointSize 
        fontSetting.attrib["family"] = family 
        fontSetting.attrib["name"] = name 

        if name not in existFonts:
            addCustomFonts(customFont,"Canada Type - {}".format(name),name)
            existFonts.append(name)

        print ("Changed to ---------->: {}".format(fontSetting.attrib))


    updateAttributeFont(root,existFonts)
 
    print ("---------------------------\n Font replace finished, {} ststem font changes, {} custom font changes \n-------------------------------------".format(systemFontChangesCount,customFontChangesCount))

    print ("Now using fonts{}".format(existFonts))

    nodes.write(filename,pretty_print=True)


def updateAttributeFont(root,existFonts):

    attibutes = 0
    attributeFonts = root.findall(".//font[@key='NSFont']")

    for atributeFont in attributeFonts:
        oldFontName = atributeFont.attrib.get("name")
        print ("attribute {}".format(oldFontName))
        if atributeFont.attrib["key"] == "NSFont" and oldFontName != None :

            if  "gibson"  in oldFontName.lower():
                continue

            attibutes += 1

            if "light" in oldFontName:
                atributeFont.attrib["name"] = "Gibson-Light"
            elif "bold" in oldFontName or "bd" in oldFontName:
                atributeFont.attrib["name"] = "Gibson-Bold"
            else:
                atributeFont.attrib["name"] = "Gibson-Regular"


            name = atributeFont.attrib["name"] 
            if name not in existFonts:
                addCustomFonts(customFont,"Canada Type - {}.otf".format(name),name)
                existFonts.append(name)
        else:
            print ("not changing unknown font{}".format(atributeFont.attrib))


    print ("Replaced {} attibutes".format(attibutes))


if os.path.isfile(filename):
    updateFile(filename)
else:
    os.chdir(filename)
    for file in glob.glob("*.storyboard"):
        print ("---------------------------FILE:{}---------------------------".format(file))
        updateFile(file)

