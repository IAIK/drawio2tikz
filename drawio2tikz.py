#TODO check slh.drawio.cml if time
import configparser
import os
import re
import string
import sys
import xml.etree.ElementTree as ET

import webcolors


# ------------------------------------------------------
class Coordinates:
    def __init__(self, x, y):
        self.X = float(x)
        self.Y = float(y)


# ------------------------------------------------------
class childValues:
    def __init__(self, mxPoint, style, relatives):
        self.mxPoint = mxPoint
        self.style = style
        self.relative = relatives


# Fonts
# Helvetica = texttt, Verdana = , Times New Roman = , Garamond = , Comic Sans MS = , Courier New = none, Georgia = ,
# Lucida Console = , Tahoma = ,

# [texttt]
# [textbf]
# [textit]
# [none]
# ------------------------------------------------------
# ------------------------------------------------------
def readConfig(configurationFile):
    config = configparser.ConfigParser()
    dir = os.getcwd()
    configurationFile = configurationFile[configurationFile.find(dir) + len(dir) + 1:]
    if (dir.endswith("code") == False):
        configurationFile = "code/" + configurationFile
    config.read(configurationFile)
    return config


# ------------------------------------------------------
def splitStringBeforeComaOrSpace(stringToSplit):
    x = stringToSplit.find(',')
    space = stringToSplit.find(' ')
    splittedString = string
    if (x != -1):
        splittedString = stringToSplit[0:x]
    elif (space != -1):
        splittedString = stringToSplit[0:space]
    return splittedString


# ------------------------------------------------------
def splitStringAfterComaOrSpace(stringToSplit):
    x = stringToSplit.find(',')
    space = stringToSplit.find(' ')
    splittedString = string
    if (x != -1):
        splittedString = stringToSplit[x + 1:]
    elif (space != -1):
        splittedString = stringToSplit[space + 1:]
    return splittedString


# ------------------------------------------------------
def printColour(color, alreadyDefinedColours):
    # print(color)
    if (color == None or color == 'default'):
        return alreadyDefinedColours
    if (color == 'none'):
        color = '#' + white
    if(color.find("#") == -1):
        return alreadyDefinedColours
    colour = color[-6:]
    if (config.has_option("Colours", colour) == True and colour not in alreadyDefinedColours):
        colorRGB = webcolors.hex_to_rgb(color)
        alreadyDefinedColours.append(colour)
        print("\definecolor{%s}{RGB}{%d,%d,%d}" % (
            config["Colours"][colour], colorRGB.red, colorRGB.green, colorRGB.blue))
    elif (colour not in alreadyDefinedColours):
        # print(colour)
        colorRGB = webcolors.hex_to_rgb(color)
        alreadyDefinedColours.append(colour)
        print("\definecolor{%s}{RGB}{%d,%d,%d}" % (colour, colorRGB.red, colorRGB.green, colorRGB.blue))
    return alreadyDefinedColours


# ------------------------------------------------------
def getFillColour(style):
    fill = ''
    fillColour = findAndReturnInSplitted(style, "fillColor=")
    opacity = findAndReturnInSplitted(style, "opacity=")
    if(fillColour == "default" and style[0] == 'text'):
        fill = ",fill=white"
        if(opacity != None):
            fill = fill + ",opacity={0:}".format(float(opacity) / 100) + ",text opacity=1"
        return fill
    if (fillColour != None and fillColour != "none" and fillColour != "default"):
        color = fillColour[-6:]  # it has to be 6 digits no matter what
        if (config.has_option("Colours", color) == True):
            fill = ',fill=' + config["Colours"][color]
        else:
            fill = ',fill=' + color
        if (opacity != None):
            fill = fill + ",opacity={0:}".format(float(opacity) / 100) + ",text opacity=1"
        return fill
    else:
        # TODO use fill color white here -> need to refactor every single test with that
        return fill  # makes me use fewer ifs


# ------------------------------------------------------
def getStrokeColour(style):
    strokeColour = findAndReturnInSplitted(style, r"strokeColor=")
    if (strokeColour == "none"):
        return "white"
    elif (strokeColour != None and strokeColour != "default"):
        color = strokeColour[-6:]
        if (config.has_option("Colours", color) == True):
            return config["Colours"][color]
        return color
    else:
        return ''


# # #TODO if time is still there adapt every single word with the corresponding colour not whole text in one
# # # probably like makeWordBold but not so sure might be something different
# # ------------------------------------------------------
# def prepareTextColors(text,style):
#     if(text.find("font color=\"") == -1 and style.find("fontColor") != -1):
#         fontColour = getFontColourText(text, style)
#         if(fontColour != ''):
#             text = "\\textcolor{" + fontColour + "}{" + text + "}"
#         return text
#     elif(text.find("font color=") == -1 and style.find("fontColor") != -1):
#         currentText = text
#         while(currentText.find("font color=\"") != -1):
#             #TODO somehow find out which part belongs to which word
#             fontColour = currentText[currentText.find("font color=\"") + len("font color=\""):].split('"')[0]
#             text = "\\textcolor{" + fontColour + "}{" + text + "}"
#             currentText = currentText[currentText.find("font color=\"") + len("font color=\""):]
#         return text
#     else:
#         return text
#
# # ------------------------------------------------------
# def getFontColourText(text, style):
#     fontColour = ''
#     if (text != replaceCircledUnicode(text)):
#         return ''
#
#     elif text.find("font color=\"") != -1:
#         fontColour = text[text.find("font color=\"") + len("font color=\""):].split('"')[0]
#     elif style.find("fontColor") != -1:
#         fontColour = style[style.find("fontColor=") + len("fontColor="):].split(';')[0]
#
#     if (fontColour == "none"):
#         return white
#     elif (fontColour != None and fontColour != "default"):
#         color = fontColour[-6:]
#         if (config.has_option("Colours", color) == True):
#             return config["Colours"][color]
#         return color
#     else:
#         return ''


# ------------------------------------------------------
def getFontColour(text, style):
    fontColour = ''
    if (text != replaceCircledUnicode(text)):
        return ''

    if (text.find("font color=") == -1 and style.find("fontColor") == -1 and text.find('color="') == -1):
        return ''
    elif text.find("font color=\"") != -1:
        fontColour = text[text.find("font color=\"") + len("font color=\""):].split('"')[0]
    elif style.find("fontColor") != -1:
        fontColour = style[style.find("fontColor=") + len("fontColor="):].split(';')[0]
    elif(text.find('color="') != -1):
        fontColour = text[text.find('color="') + len('color="'):].split('"')[0]

    if (fontColour == "none"):
        return white
    elif (fontColour != None and fontColour != "default"):
        color = fontColour[-6:]
        if (config.has_option("Colours", color) == True):
            return ',text=' + config["Colours"][color]
        return ',text=' + color
    else:
        return ''


# ------------------------------------------------------
def splitAfterEqualSign(stringToSplit):
    splitted = str(stringToSplit).split('=')
    value = splitted[1]
    value = value[:len(value) - 2]
    return value


# ------------------------------------------------------
def findAndReturnInSplitted(stringToSplit, toBeFound):
    res = [x for x in stringToSplit if toBeFound in x]
    if (str(res).find('=') != -1):
        foundElement = splitAfterEqualSign(res)
        return foundElement
    else:
        return None


# ------------------------------------------------------
def indexContainingSubstring(theList, substring):
    for index, s in enumerate(theList):
        if substring in s:
            return index
    return -1


# ------------------------------------------------------
def splitAfterAndBeforeSign(text, splitAfter, splitBefore):
    if (text.find(splitAfter) != -1 and text.find(splitBefore) != -1):
        if (text.find("font face=") != -1):
            text = text[text.find("font face="):]
            text = text[text.find(splitAfter) + 1:]
            text = text[:text.find(splitBefore)]
            return text
        else:
            before, separator, text = text.partition(splitAfter)
            text, separator, after = str(text).partition(splitBefore)
            return text
    else:
        return text


# ------------------------------------------------------
def getMiddle(startX, startY, endX, endY):
    mid = Coordinates(0, 0)
    mid.X = float((startX + endX) / 2)
    mid.Y = float((startY + endY) / 2)
    return mid


# ------------------------------------------------------
def getFont(text, style):
    if (text.find("font face") != -1):
        font = splitAfterEqualSign(text)
    elif (style.find("fontFamily=") != -1):
        font = style[style.find("fontFamily=") + len("fontFamily="):]
        font = font.split(';')[0]
    else:
        font = ''

    if (font.find("Comic Sans MS") != -1 or font.find("Georgia") != -1 or font.find(
            "Lucida Console") != -1):
        font = r"\textbf"
    elif (font.find("Courier New") != -1 or font.find("Verdana") != -1 or font.find("Tahoma") != -1):
        font = r"\texttt"
    elif (font.find("Helvetica") != -1 or font.find("Times New Roman") != -1 or font.find(
            "Garamond") != -1):
        font = ''
    else:
        font = ''
    if(text.find("</h1>") != -1 and font == ''):
        font = r"\textbf"

    if(text.find("/strike") != -1):
        if(font != ''):
            font = r"\st{" + font + "}"
        else:
            font = r"\st"

    return font


# ------------------------------------------------------
def getFontSize(text, style):
    if (text.find("font-size:") != -1):
        size = int(float(text[text.find("font-size: ") + len("font-size: "):].split('px')[0]))
    elif (style.find("fontSize=") != -1):
        size = int(float(style[style.find("fontSize=") + len("fontSize="):].split(';')[0]))
    else:
        size = 12
    if (size != ""):
        if (size < 7):
            size = r'\small'
        elif (size >= 7 and size < 22):
            size = ''
        elif (size >= 22):
            size = r"\Large"
    else:
        size = ''
    return size


# ------------------------------------------------------
def replaceCircledUnicode(text):
    for letter in text:
        if (config.has_option("circled Unicode", letter) == True):
            text = text.replace(letter, config["circled Unicode"][letter])

    return text


# ------------------------------------------------------
def replaceUnicode(text):
    text = replaceCircledUnicode(text)
    for letter in text:
        if (config.has_option("Unicode", letter) == True):
            text = text.replace(letter, config["Unicode"][letter])

    return text


# ------------------------------------------------------
def getFontStyle(style):
    type = ''
    if (style.find("fontStyle=\"") != -1):
        type = style[style.find("fontStyle=\"") + len("fontStyle=\""):].split('"')[0]
    elif (style.find("fontStyle=") != -1):
        type = style[style.find("fontStyle=") + len("fontStyle="):].split(';')[0]

    if (type == '1'):
        type = r"\textbf"
    else:
        type = ''

    return type


# ------------------------------linebreaks----------------------
def replaceLinebreaksAndFilterText(text):
    text = text.replace(" ", "~")
    text = text.replace("nbsp;", "~")
    text = text.replace("<sup>", "$^")
    text = text.replace("</sup>", "$")

    if(not(text.find("<sub>") < text.find("span style=") and text.find("</sub>") > text.find("span style=")) and
            text.find("</sub>") != -1):
        text = text.replace("<sub>", "$_")
        text = text.replace("</sub>", "$")
    elif(text.find("</sub>") != -1):
        text = text.replace("<sub>", "", 1)
        text = text[:text.find("</sub>") + len("</sub>")]
        text = text.replace("<sub>", "$_")
        text = text.replace("</sub>", "$")

    text = text.replace("&", "")

    if (text.find("<br>") != -1):
        text = text.replace("<br>", r"\\[-2pt]")
        text = re.sub("<br([^>]*)>", r"\\\\[-2pt]", text)

    if (text.find("<br") != -1):
        text = re.sub("<br([^>]*)>", r"\\\\[-2pt]", text)

    if (text.find("<") != -1):
        text = re.sub(r"<.*?>", r"", text)

    # print(text + " stop")
    while (text.endswith(r"\\[-2pt]") == True or text.endswith(r"\\[-2pt]}") == True):
        if(text.endswith(r"\\[-2pt]") == True):
            text = text[:-len(r"\\[-2pt]")]
        elif(text.endswith(r"\\[-2pt]}") == True):
            text = text[:-len(r"\\[-2pt]}")] + "}"

    while (text.startswith(r"\\[-2pt]") == True):
        text = text[len(r"\\[-2pt]"):]

    if (text.find(r"\\") != -1):
        text = text + r"\\"

    text = text.replace(r"\\[-2pt]\\[-2pt]", r"\\[4pt]")
    return text


# ------------------------------------------------------
def makeWordBold(filtertext):
    textbold = re.sub(r"<b(?:\s[^>]*)?>", r"\\textbf{", filtertext)
    textbold = re.sub(r"</b>", r"}", textbold)
    return textbold


# ------------------------------------------------------
def findAmountofCharacter(text, character):
    amount = 0
    for letter in text:
        if(letter == character):
            amount += 1

    return amount


# ------------------------------------------------------
def replaceSpecialCharacters(text):
    text = text.replace("~", r"$\sim$")
    replaceTextPostion = text.find(r"\text{")
    nextBrace = text.find("}", replaceTextPostion)
    for i in range(replaceTextPostion, nextBrace):
        if(text[i] == ' '):
            text = text[:i] + text[i].replace(' ', '~') + text[i+1:]

    if(nextBrace != -1 and replaceTextPostion != -1):
        text = text[:nextBrace] + text[nextBrace + 1:]

    text = text.replace(r"\text{", r"")
    # text = text.replace(r"$$", r"$")
    text = text.replace(r"%", r"\%")
    #only replace the backslash somehow -> DONT might replace unwanted characters just use the backslash n etc
    text = text.replace(r'\n' , r"\textbackslash n")
    text = text.replace(r"{", r"\{")
    text = text.replace(r"}", r"\}")
    text = text.replace(r"#", r"\#")
    # text = text.replace("<<", "$<<$")

    return text


# ------------------------------------------------------
def replaceFirstAndLastDoubleDollar(text):
    if(text != '' and text != None):
        rangeOfDollar = int(len(text)/(len(text)/4))
        while(text[:rangeOfDollar].find("$$") != -1):
            text = text.replace("$$", "$", 1)

        reversedString = text[::-1]
        while(reversedString[:rangeOfDollar].find("$$") != -1):
            reversedString = reversedString.replace("$$", "$", 1)

        text = reversedString[::-1]

    return text


# ------------------------------------------------------
def replaceSignificantCharacters(text):
    text = text.replace(r"lt;", r"$<$")
    text = text.replace(r"gt;", r"$>$")
    text = text.replace(r"\\[-2pt]$", r"$")
    text = replaceFirstAndLastDoubleDollar(text)
    #this part needs some serious rethinking -> already much better
    amount = findAmountofCharacter(text, '$')
    text_reversed = text[::-1]
    if(amount == 1):
        text = text.replace(r"$", r"\$")
    elif(amount % 2 != 0):
        #how do we know which $ to replace if it's not even and how do we know we don't have to replace it anyway
        text_reversed = text_reversed.replace(r"$", '$\\', 1)
        text = text_reversed[::-1]
    text = text.replace("amp;", "\&")
    return text


# ------------------------------------------------------
def prepareText(text, style, height=float('0'), pureText = False):
    if (text != ""):
        curtext = text
        text = replaceSpecialCharacters(text)
        text = makeWordBold(text)
        text = replaceLinebreaksAndFilterText(text)
        fontsize = getFontSize(curtext, style)

        if(pureText == True):
            return text

        # text = prepareTextColors(text,style)
        if (text != replaceCircledUnicode(text)):
            fontface = r"\textbf"
        else:
            fontface = getFont(curtext, style)

        if (fontsize != '' and text != ''):
            text = fontsize + "{" + text + "}"

        if (fontface != "" and text != ''):
            text = fontface + "{" + text + "}"

        fontStyle = getFontStyle(style)
        if (fontStyle != "" and text != ''):
            text = fontStyle + "{" + text + "}"
        text = replaceUnicode(text)
        if (style.find("verticalAlign=top") != -1):
            if(text.find(" ") != -1):
                text = text.replace(" ", r" \vspace{" + str(round(height - 1, 2)) + "cm}", 1)
            elif(text.find(r"\\[-2pt]") != -1):
                text = text.replace(r"\\[-2pt]", r" \vspace{" + str(round(height - 1, 2)) + "cm}", 1)
            else:
                text = r"\vspace{" + str(round(height - 1, 2)) + "cm}" + "{" + text + "}"

        horizontal = getHorizontal(style)
        if(horizontal != ''):
            text = horizontal + "{" + text + "}"

    text = replaceSignificantCharacters(text)
    return text


# ------------------------------------------------------
def replaceOffset(offset, top):
    #TODO this needs much more thought -> might already be enough most of the times

    newOffset = ''
    offset = offset.split(',')
    for i, item in enumerate(offset):
        if (str(item).find("left") != -1 or str(item).find("right") != -1 or str(item).find("above") != -1
                or str(item).find("left") != -1 or item == None):
            continue
        newOffset += item + ','
        if(i == 0 and top):
            newOffset += 'above,'
        elif(i == 0 and not top):
            newOffset += 'below,'

    offset = newOffset[:-1]
    return offset


# ------------------------------------------------------
def prepareLabelText(text, offset):
    currentText = text
    if (text != "" and text.find(r"\\") == -1):
        text = "node{0}".format(offset) + "{" + text + "}"
    elif(text != "" and text.find(r"\\[-2pt]") != -1):
        topOffset = replaceOffset(offset, True)
        botOffset = replaceOffset(offset, False)
        text = "node{0}".format(topOffset) + "{" + currentText.split(r"\\[-2pt]")[0] + "}"
        text += "node{0}".format(botOffset) + "{" + currentText.split(r"\\[-2pt]")[1] + "}"
        text = text.replace(r"\\","")# for replacing trailing newlines which aren't necessary anymore

    return text


# ------------------------------------------------------
def getVerticalOffset(offset, offset_y, offset_relative_y_diff):
    if (offset_y != None and offset_y < 0 and offset_relative_y_diff < 0):
        if (offset != ''):
            offset = offset + ",above={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
        else:
            offset = offset + "above={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
    elif (offset_y != None and offset_y > 0 and offset_relative_y_diff > 0):
        if (offset != ''):
            offset = offset + ",below={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
        else:
            offset = offset + "below={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
    elif (offset_y != None and offset_y < 0 and offset_relative_y_diff == 0):
        if (offset != ''):
            offset = offset + ",above={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
        else:
            offset = "above={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
    elif (offset_y != None and offset_y > 0 and offset_relative_y_diff == 0):
        if (offset != ''):
            offset = offset + ",below={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
        else:
            offset = "below={0:.2f}".format(offset_y / (divisorfactor.Y * 10))
    return offset


# ------------------------------------------------------
def getoffset(mxPoint, style, relative):
    splittedStyle = style.split(';')
    rotate = getRotation(splittedStyle)
    offset = ''
    offset_relative_x_diff = 0
    offset_relative_y_diff = 0
    relative_x = relative.get('x')
    relative_y = relative.get('y')
    offset_x = mxPoint.get('x')
    offset_y = mxPoint.get('y')

    # ------------------------------------------------------
    if (relative_x != None):
        relative_x = float(relative_x)
        if (offset_x != None):
            offset_relative_x_diff = relative_x + (float(offset_x) / divisorfactor.Y)
        if (offset_relative_x_diff < -5.5 or offset_relative_x_diff > 5.5):
            relative_x = -relative_x * 3

    if (relative_y != None):
        relative_y = float(relative_y)
        if (offset_y != None):
            offset_y = float(offset_y)
            offset_relative_y_diff = int(relative_y + (offset_y / divisorfactor.Y))
        if (offset_relative_y_diff < -10 or offset_relative_y_diff > 10):
            offset_y = -offset_y
            offset_relative_y_diff = int(-offset_relative_y_diff)
    if (offset_y != None):
        offset_y = float(offset_y)

    # ------------------------------------------------------
    if (relative_y == None or (style.find("align=center") != -1 and relative_y < 0)):
            offset = "pos=0.50"
    else:
        if (relative_y == 0):
            relative_y = 1
        relative_y = abs(relative_y)
        position = 1 / relative_y
        if (offset != ''):
            offset = offset + ",pos={0:.2f}".format(position)
        else:
            offset = "pos={0:.2f}".format(position)

    if (relative_x != None and relative_x < 0 and offset_relative_x_diff < 0 and style.find("verticalAlign=middle") != -1 and style.find("spacingLeft") != -1):
        if (offset != ''):
            offset = offset + ",left={0:.2f}cm".format(abs(relative_x))
        else:
            offset = offset + "left={0:.2f}cm".format(abs(relative_x))
    if (relative_x != None and relative_x > 0 and offset_relative_x_diff > 0 and style.find("verticalAlign=middle") != -1 and style.find("spacingRight") != -1):
        if (offset != ''):
            offset = offset + ",right={0:.2f}cm".format(relative_x)
        else:
            offset = offset + "right={0:.2f}cm".format(relative_x)

    # ------------------------------------------------------
    if(relative_y != None and relative_y < 0):
        offset_relative_y_diff = offset_y
    offset = getVerticalOffset(offset, offset_y, offset_relative_y_diff)

    # ------------------------------------------------------
    if (rotate != None and rotate != 0):
        if (offset != ''):
            offset = offset + ",rotate={0}".format(rotate)
        else:
            offset = offset + "rotate={0}".format(rotate)
    if (offset != ''):
        offset = "[" + offset + "]"
    return offset


# ------------------------------------------------------
def getID(sourceOrTargetOrID, child):
    ID = ''
    if (sourceOrTargetOrID == "id"):
        ID = child.attrib.get("id")
    elif (sourceOrTargetOrID == "source"):
        ID = child.attrib.get("source")
    elif (sourceOrTargetOrID == "target"):
        ID = child.attrib.get("target")
    return getIDNumber(ID)


# ------------------------------------------------------
def getIDNumber(ID):
    if (ID == None):
        return ''
    position = ID.find("_")
    if (len(ID) - position > 8 or len(ID) - position < 5):
        position = len(ID) - 6
    return 'ID' + ID[position:]


# ------------------------------------------------------
def calculateCoordinateForAnchor(coordinate):
    # -------------------------------------------------------
    if coordinate <= 0.1:
        return 0
    elif coordinate > 0.1 and coordinate < 0.4:
        return 0.25
    elif coordinate >= 0.4 and coordinate < 0.6:
        return 0.5
    elif coordinate >= 0.6 and coordinate < 0.9:
        return 0.75
    else:
        return 1


# ------------------------------------------------------
def getEntryAnchor(style, objectStyle):
    anchor = ''
    entryCoor = Coordinates(0, 0)
    entryCoor.X = findAndReturnInSplitted(style, "entryX")
    entryCoor.Y = findAndReturnInSplitted(style, "entryY")
    if (entryCoor.X == None):
        return anchor
    entryCoor.X = float(entryCoor.X)
    entryCoor.Y = float(entryCoor.Y)

    entryCoor.X = calculateCoordinateForAnchor(entryCoor.X)
    entryCoor.Y = calculateCoordinateForAnchor(entryCoor.Y)

    # -------------------------------------------------------
    if (entryCoor.X == 0 and entryCoor.Y == 0):
        anchor = '.north west'
    elif (entryCoor.X == 0 and entryCoor.Y == 0.25):
        anchor = '.west north west'
    elif (entryCoor.X == 0 and entryCoor.Y == 0.5):
        anchor = '.west'
    elif (entryCoor.X == 0 and entryCoor.Y == 0.75):
        anchor = '.west south west'
    elif (entryCoor.X == 0 and entryCoor.Y == 1):
        anchor = '.south west'
    elif (entryCoor.X == 0.25 and entryCoor.Y == 1):
        anchor = '.south south west'
    elif (entryCoor.X == 0.5 and entryCoor.Y == 1):
        anchor = '.south'
    elif (entryCoor.X == 0.75 and entryCoor.Y == 1):
        anchor = '.south south east'
    elif (entryCoor.X == 1 and entryCoor.Y == 1):
        anchor = '.south east'
    elif (entryCoor.X == 1 and entryCoor.Y == 0.75):
        anchor = '.east south east'
    elif (entryCoor.X == 1 and entryCoor.Y == 0.5):
        anchor = '.east'
    elif (entryCoor.X == 0 and entryCoor.Y == 1):
        anchor = '.east north east'
    elif (entryCoor.X == 1 and entryCoor.Y == 0):
        anchor = '.north east'
    elif (entryCoor.X == 0.75 and entryCoor.Y == 0):
        anchor = '.north north east'
    elif (entryCoor.X == 0.5 and entryCoor.Y == 0):
        anchor = '.north'
    elif (entryCoor.X == 0.25 and entryCoor.Y == 0):
        anchor = '.north north west'

    if(objectStyle.find("shape=mxgraph.electrical.logic_gates.logic_gate") != -1):
        anchor = anchor.replace(".west north west", ".in 1")
        anchor = anchor.replace(".west south west", ".in 2")
        anchor = anchor.replace(".east", ".out")

    if(objectStyle.find("shape=mxgraph.electrical.electro-mechanical") != -1):
        anchor = anchor.replace(".east north east", ".out 1")
        anchor = anchor.replace(".east south east", ".out 2")
        anchor = anchor.replace(".west", ".in")

    return anchor


# ------------------------------------------------------
def getExitAnchor(style, objectStyle):
    anchor = ''
    exitCoor = Coordinates(0, 0)
    exitCoor.X = findAndReturnInSplitted(style, "exitX")
    exitCoor.Y = findAndReturnInSplitted(style, "exitY")
    if (exitCoor.X == None):
        return anchor
    exitCoor.X = float(exitCoor.X)
    exitCoor.Y = float(exitCoor.Y)

    exitCoor.X = calculateCoordinateForAnchor(exitCoor.X)
    exitCoor.Y = calculateCoordinateForAnchor(exitCoor.Y)

    # -------------------------------------------------------
    if (exitCoor.X == 0 and exitCoor.Y == 0):
        anchor = '.north west'
    elif (exitCoor.X == 0. and exitCoor.Y == 0.25):
        anchor = '.west north west'
    elif (exitCoor.X == 0 and exitCoor.Y == 0.5):
        anchor = '.west'
    elif (exitCoor.X == 0 and exitCoor.Y == 0.75):
        anchor = '.west south west'
    elif (exitCoor.X == 0 and exitCoor.Y == 1):
        anchor = '.south west'
    elif (exitCoor.X == 0.25 and exitCoor.Y == 1):
        anchor = '.south south west'
    elif (exitCoor.X == 0.5 and exitCoor.Y == 1):
        anchor = '.south'
    elif (exitCoor.X == 0.75 and exitCoor.Y == 1):
        anchor = '.south south east'
    elif (exitCoor.X == 1 and exitCoor.Y == 1):
        anchor = '.south east'
    elif (exitCoor.X == 1 and exitCoor.Y == 0.75):
        anchor = '.east south east'
    elif (exitCoor.X == 1 and exitCoor.Y == 0.5):
        anchor = '.east'
    elif (exitCoor.X == 1 and exitCoor.Y == 0.25):
        anchor = '.east north east'
    elif (exitCoor.X == 1 and exitCoor.Y == 0):
        anchor = '.north east'
    elif (exitCoor.X == 0.75 and exitCoor.Y == 0):
        anchor = '.north north east'
    elif (exitCoor.X == 0.5 and exitCoor.Y == 0):
        anchor = '.north'
    elif (exitCoor.X == 0.25 and exitCoor.Y == 0):
        anchor = '.north north west'

    if(objectStyle.find("shape=mxgraph.electrical.logic_gates.logic_gate") != -1):
        anchor = anchor.replace(".west north west", ".in 1")
        anchor = anchor.replace(".west south west", ".in 2")
        anchor = anchor.replace(".east", ".out")

    if(objectStyle.find("shape=mxgraph.electrical.electro-mechanical") != -1):
        anchor = anchor.replace(".east north east", ".out 1")
        anchor = anchor.replace(".east south east", ".out 2")
        anchor = anchor.replace(".west south west", ".in")

    return anchor


# ------------------------------------------------------
def getAnchor(exitOrEntry, style, objectStyle=''):
    anchor = ''
    if (exitOrEntry == "exit"):
        anchor = getExitAnchor(style, objectStyle)
    elif (exitOrEntry == "entry"):
        anchor = getEntryAnchor(style, objectStyle)
    else:
        print("something went wrong while acquiring the anchor")
    return anchor


# ------------------------------------------------------
def findEntryAnchor(target, style):
    if (target != None and mapObjects.get(target) != None and mapObjects.get(target).find("rotation") != -1):
        entryAnchor = ''
    elif (mapObjects.get(target) != None):
        entryAnchor = getAnchor("entry", style, mapObjects.get(target))
    else:
        entryAnchor = getAnchor("entry", style)
    return entryAnchor


# ------------------------------------------------------
def findExitAnchor(source, style):
    if (mapObjects.get(source) != None and mapObjects.get(source).find("rotation") != -1):
        entryAnchor = ''
    elif (mapObjects.get(source) != None):
        entryAnchor = getAnchor("exit", style, mapObjects.get(source))
    else:
        entryAnchor = getAnchor("exit", style)
    return entryAnchor


# ------------------------------------------------------
def getLineStyle(style):
    line = ',solid'
    if (findAndReturnInSplitted(style, "dashed") != None and findAndReturnInSplitted(style, "dashPattern=1 3") != None):
        line = ',dashed'
    elif (findAndReturnInSplitted(style, "dashed") != None and findAndReturnInSplitted(style,
                                                                                       "dashPattern=1 4") != None):
        line = ',dotted'
    elif (findAndReturnInSplitted(style, "dashed") != None and findAndReturnInSplitted(style,
                                                                                       "dashPattern=8 8") != None):
        line = ',loosely dashed'
    elif (findAndReturnInSplitted(style, "dashed") != None):
        line = ',dashed'  # my default case to have it somewhat dashed and didn't handle pattern yet
    return line


# ------------------------------------------------------
def getLineWidth(style):
    lineWidth = ''
    if(findAndReturnInSplitted(style, "strokeWidth=") != None):
        width = findAndReturnInSplitted(style, "strokeWidth=")
        if(divisorfactor.Y > 2):
            width = float(width) / (divisorfactor.Y - 2)
        lineWidth = ",line width={0:.1f}pt".format(width)
    return lineWidth


# ------------------------------------------------------
def getSpacing(style , divisor=None):
    spacing = ',inner sep=0'
    if (findAndReturnInSplitted(style, 'spacingLeft') != None and findAndReturnInSplitted(style, 'spacingRight') != None):
        right = float(findAndReturnInSplitted(style, 'spacingRight'))
        left = float(findAndReturnInSplitted(style, 'spacingLeft'))
        if(divisor != None):
            return ',inner sep=' + str((right + left) / (2 * divisor))
        spacing = ',inner sep=' + str((right + left) / 2)
    return spacing


# ------------------------------------------------------
def getControls(arrayWithPoints, targetPoint):
    controlPoints = "--"
    cPoint = Coordinates(0,0)
    for point in arrayWithPoints:
        cPoint = Coordinates(0, 0)
        if point.get("x") != None and point.get("y") != None:
            cPoint.X = "{0:.1f}".format(float(point.get("x")) / divisorfactor.X)
            cPoint.Y = "{0:.1f}".format(-float(point.get("y")) / divisorfactor.X)
        elif (point.get("x") == None) and (point.get("y") == None):
            continue
        elif point.get("x") == None:
            cPoint.Y = "{0:.1f}".format(-float(point.get("y")) / divisorfactor.X)
            cPoint.X = 0.0
        elif point.get("y") == None:
            cPoint.X = "{0:.1f}".format(float(point.get("x")) / divisorfactor.X)
            cPoint.Y = 0.0
        controlPoints += ('(' + str(cPoint.X) + ',' + str(cPoint.Y) + ')')
        if (point != arrayWithPoints[-1]):
            controlPoints += ("--")
        else:
            controlPoints += ("--")
    if(float(cPoint.X) == round(targetPoint.X, 1) and float(cPoint.Y) == round(targetPoint.Y, 1)):
        controlPoints = controlPoints.replace(("({0:},{1:})--".format(cPoint.X, cPoint.Y)), "")
    return controlPoints


# ------------------------------------------------------
def getCurvedControls(arrayWithPoints, arc):
    controlPoints = "..controls"
    first_coordinate = True
    for point in range(len(arrayWithPoints)):
        cPoint = Coordinates(0, 0)
        cPoint.X = "{0:.1f}".format((float(arrayWithPoints[point].get("x")) / divisorfactor.X))
        cPoint.Y = "{0:.1f}".format((-float(arrayWithPoints[point].get("y")) / divisorfactor.X))
        if (arc != None):
            cPoint.Y = float(cPoint.Y) - arc
        controlPoints += ('(' + str(cPoint.X) + ',' + str(cPoint.Y) + ')')
        if (first_coordinate == False and point != len(arrayWithPoints) - 1):
            nextPoint = Coordinates(0, 0)
            nextPoint.X = "{0:.1f}".format((float(arrayWithPoints[point + 1].get("x")) / divisorfactor.X))
            nextPoint.Y = "{0:.1f}".format((-float(arrayWithPoints[point + 1].get("y")) / divisorfactor.X))
            if (arc != None):
                nextPoint.Y = float(nextPoint.Y) - arc

            controlPoints += ".." + '(' + "{0:.1f}".format((float(cPoint.X) + float(nextPoint.X)) / 2) + ',' + \
                             "{0:.1f}".format((float(cPoint.Y) + float(nextPoint.Y)) / 2) + ')' + "..controls"
            first_coordinate = True
            continue
        elif (point != len(arrayWithPoints) - 1):
            controlPoints += ("and")
            first_coordinate = False
        else:
            controlPoints += ("..")
    if(controlPoints == "..controls"):
        controlPoints = "to"
    return controlPoints


# ------------------------------------------------------
def getText(child):
    text = child.attrib.get("value")
    if (text != None):
        text = text.replace('_', '\_')
    else:
        text = ''
    return text


# ------------------------------------------------------
def getArc(style):
    arc = findAndReturnInSplitted(style, "arcSize")
    if (arc != None):
        arc = float(arc) / 20
    else:
        arc = 0
    # print(arc)
    return arc


# ------------------------------------------------------
def getHorizontal(style):
    horizontal = ''
    if(style.find("horizontal=0;") != -1):
        horizontal = r"\rotatebox{90}"
    return horizontal


# ------------------------------------------------------
def getNextId(ID):
    IDNumber = int(ID[-2:]) + 1
    ID = ID[:-2] + str(IDNumber)
    # print(ID)
    return ID


# ------------------------------------------------------
def getTarget(child):
    if (child.attrib.get("target") != None):
        target = getID('target', child)
        if (mapObjects.get(target) != None and (mapObjects.get(target).find("shape=curlyBracket") != -1 and
              mapObjects.get(target).find("shape=mxgraph.flowchart.annotation_2") != -1)):
            target = None
    else:
        target = None
    while(mapObjects.get(target) != None and
          (mapObjects.get(target).find("shape=table") != -1 or mapObjects.get(target).find("shape=tableRow") != -1)):
        target = getNextId(target)
    return target


# ------------------------------------------------------
def getSource(child):
    if (child.attrib.get("source") != None):
        source = getID('source', child)
        if (mapObjects.get(source) != None and (mapObjects.get(source).find("shape=curlyBracket") != -1
                and mapObjects.get(source).find("shape=mxgraph.flowchart.annotation_2") != -1)):
            source = None
    else:
        source = None
    while(mapObjects.get(source) != None and
          (mapObjects.get(source).find("shape=table") != -1 or mapObjects.get(source).find("shape=tableRow") != -1)):
        source = getNextId(source)
    return source

def getSourcePoint(element, sourcePoint):
    if (element.get("as") == "sourcePoint"):
        if (element.attrib.get("x") != None):
            sourcePoint.X = float(element.attrib.get("x")) / divisorfactor.X

        if (element.attrib.get("y") != None):
            sourcePoint.Y = -float(element.attrib.get("y")) / divisorfactor.X
    return sourcePoint


def getTargetPoint(element, targetPoint):
    if (element.get("as") == "targetPoint"):
        if (element.attrib.get("x") != None):
            targetPoint.X = float(element.attrib.get("x")) / divisorfactor.X

        if (element.attrib.get("y") != None):
            targetPoint.Y = -float(element.attrib.get("y")) / divisorfactor.X
    return targetPoint

# ------------------------------------------------------
def getOrthogonalControls(child, entry, exit, previousChild, objectCoordinates, source, target, targetPoint):
    #TODO somehow make corners at the right points without coordinates from points -> still not done really
    if (list(child) and str(list(child)).find('Array') != -1):
        control = getControls(list(child)[-1], targetPoint)

    elif (len(list(child)) < 1 and str(child).find('Array') == -1 and
          (objectCoordinates.get(source).Y != objectCoordinates.get(target).Y)):
        if (entry == '' and previousChild != ''):
            entry = previousChild.entry
        if (exit == '' and previousChild != ''):
            exit = previousChild.exit
        if (entry.find('north') != -1 and exit.find('south') != -1):
            coordinates = '0,-1'
        elif (entry.find('west') != -1 and exit.find('east') != -1):
            coordinates = '1,0'
        elif (entry.find('south') != -1 and exit.find('north') != -1):
            coordinates = '0,1'
        elif (entry.find('east') != -1 and exit.find('west') != -1):
            coordinates = '-1,0'
        else:
            coordinates = ''
        if (coordinates != ''):
            control = "|-++(" + coordinates + ")-|"
        else:
            control = "--"

    else:
        control = "--"
    return control


# ------------------------------------------------------
def parseArguments(argv):
    if len(argv) != 2:
        print("amount of arguments was incorrect: expected: 2 received:", len(argv))
        for argument in argv:
            print(" argument = " + argument)
        sys.exit(111)
    argument = argv[1]
    if argument[-(len(drawioEnding)):] == drawioEnding:
        eltree = ET.parse(argument)
    elif argument[-(len(XMLEnding)):] == XMLEnding:
        eltree = ET.parse(argument)
    else:
        print("not supported file type, please use an XML or drawio" + argv[1])
        sys.exit(111)
    return eltree


# ------------------------------------------------------
def printFontColour(text, style, alreadyDefined):
    while(text.find("font color=\"") != -1 or text.find('color="') != -1 or style.find("fontColor") != -1):
        fontColour = ''
        if text.find("font color=\"") != -1:
            fontColour = text[text.find("font color=\"") + len("font color=\""):].split('"')[0]
            text = text[text.find("font color=\"") + len("font color=\""):]
        elif style.find("fontColor") != -1:
            fontColour = style[style.find("fontColor=") + len("fontColor="):].split(';')[0]
            style = style[style.find("fontColor") + len("fontColor"):]
        elif(text.find('color="') != -1):
            fontColour = text[text.find('color="') + len('color="'):].split('"')[0]
            text = text[text.find('color="') + len('color="'):]

        if (fontColour != ''):
            alreadyDefined = printColour(fontColour, alreadyDefined)

    return alreadyDefined


# ------------------------------------------------------
def printStrokeColour(style, alreadyDefined):
    strokeColor = ''
    if style.find("strokeColor=") != -1:
        strokeColor = style[style.find("strokeColor=") + len("strokeColor="):].split(';')[0]
    if (strokeColor != ''):
        alreadyDefined = printColour(strokeColor, alreadyDefined)
    return alreadyDefined


# ------------------------------------------------------
def printFillColour(style, alreadyDefined):
    fillColor = ''
    if style.find("fillColor=") != -1:
        fillColor = style[style.find("fillColor=") + len("fillColor="):].split(';')[0]
    if (fillColor != ''):
        alreadyDefined = printColour(fillColor, alreadyDefined)
    return alreadyDefined


# ------------------------------------------------------
def calculateDivisorFactor(mytree, inSetup=None):
    maxYCoordinate = 0
    maxXCoordinate = 0
    minYCoordinate = 1000
    minXCoordinate = 1000
    maxWidth = 0
    for child in mytree.iter():
        if (child.tag == "mxGeometry"):
            y = child.attrib.get("y")
            x = child.attrib.get("x")
            width = child.attrib.get("width")
            if (x != None and float(x) > maxXCoordinate):
                maxXCoordinate = float(x)

            if (y != None and float(y) > maxYCoordinate):
                maxYCoordinate = float(y)

            if (x != None and float(x) < minXCoordinate):
                minXCoordinate = float(x)

            if (y != None and float(y) < minYCoordinate):
                minYCoordinate = float(y)

            if (width != None and float(width) > maxWidth):
                maxWidth = float(width)
    # not sure if this is the correct dimension for everything -> seems to be working out fine
    if (maxXCoordinate > maxYCoordinate * 2):
        maxYCoordinate = maxXCoordinate / 2
    if (maxYCoordinate <= 50):
        factor = 1
    elif (maxYCoordinate <= 150):
        factor = 2
    elif (maxYCoordinate <= 250):
        factor = 3
    elif (maxYCoordinate <= 350):
        factor = 4
    else:
        factor = 5

    # TODO might need fine tuning
    if (((maxXCoordinate > 1000 or maxWidth > 1000) and inSetup == True and maxXCoordinate - minXCoordinate > 500) or
            (inSetup == True and maxWidth/factor > 200)):
        print(r"\resizebox{\hsize}{!}{")
    elif (((maxXCoordinate > 1000 or maxWidth > 1000) and inSetup == False and maxXCoordinate - minXCoordinate > 500) or
            (inSetup == False and maxWidth/factor > 200)):
        print("}")

    return factor


# ------------------------------------------------------
def defineLabelDict(tree):
    labels = {}
    for child in tree.iter():
        if (child.attrib.get('parent') != '1' and child.attrib.get('parent') != None and child.attrib.get(
                'parent') != '0'):
            labels[getIDNumber(child.attrib.get('parent'))] = child
    return labels


# ------------------------------------------------------
def defineLabelPointDict(tree):
    labels = {}
    for i, child in enumerate(tree.iter()):
        if (child.attrib.get('parent') != '1' and child.attrib.get('parent') != None and child.attrib.get(
                'parent') != '0' and len(list(tree.iter())) > i + 2 and list(tree.iter())[i + 2].find('mxPoint') != -1):
            labels[getIDNumber(child.attrib.get('id'))] = childValues(list(tree.iter())[i + 2],
                                                                      child.attrib.get('style'), list(tree.iter())[
                                                                          i + 1])  # mxPoint, style, relative
    return labels

# ------------------------------------------------------
def defineBracesPositions(tree):
    positions = {}
    objectID = 0
    startPoint = Coordinates(0,0)
    endPoint = Coordinates(0, 0)
    style = ''
    for child in tree.iter():
        if (child.tag == "mxCell"):
            objectID = getID('id', child)
            style = child.attrib.get("style")
            if (style == None):
                continue
        if (child.tag == "mxGeometry" and (style.find("shape=curlyBracket") != -1
                or style.find("shape=mxgraph.flowchart.annotation_2") != -1)):
            if (child.attrib.get("x") != None):
                startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
            else:
                startPoint.X = 0
            if (child.attrib.get("y") != None):
                startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
            else:
                startPoint.Y = 0

            if (child.attrib.get("x") != None):
                startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
            else:
                startPoint.X = 0
            if (child.attrib.get("y") != None):
                startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
            else:
                startPoint.Y = 0
            if (child.attrib.get("height") != None and child.attrib.get("width") != None):
                endPoint.Y = startPoint.Y - float(child.attrib.get("height")) / divisorfactor.X
                endPoint.X = startPoint.X + float(child.attrib.get("width")) / divisorfactor.X
                middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)
                middle.X = float("{:.1f}".format(middle.X))
                middle.Y = float("{:.1f}".format(middle.Y))
                positions[objectID] = middle

    return positions


# ------------------------------------------------------
def defineObjectCoordinates(tree):
    positions = {}
    objectID = 0
    startPoint = Coordinates(0,0)
    endPoint = Coordinates(0, 0)
    for child in tree.iter():
        if (child.tag == "mxCell"):
            objectID = getID('id', child)
            style = child.attrib.get("style")
            if (style == None):
                continue
        if (child.tag == "mxGeometry"):
            if (child.attrib.get("x") != None):
                startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
            else:
                startPoint.X = 0
            if (child.attrib.get("y") != None):
                startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
            else:
                startPoint.Y = 0

            if (child.attrib.get("x") != None):
                startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
            else:
                startPoint.X = 0
            if (child.attrib.get("y") != None):
                startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
            else:
                startPoint.Y = 0
            if (child.attrib.get("height") != None and child.attrib.get("width") != None):
                endPoint.Y = startPoint.Y - float(child.attrib.get("height")) / divisorfactor.X
                endPoint.X = startPoint.X + float(child.attrib.get("width")) / divisorfactor.X
                middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)
                middle.X = float("{:.1f}".format(middle.X))
                middle.Y = float("{:.1f}".format(middle.Y))
                positions[objectID] = Coordinates(middle.X, middle.Y)

    return positions


# ------------------------------------------------------
def getRotation(style, raw=False):
    rotation = findAndReturnInSplitted(style, "rotation")
    if (rotation != None):
        if(raw == True):
            return int(rotation)
        rotation = -int(rotation)
        if (rotation < 0):
            rotation = 360 + rotation
    return rotation


# ------------------------------------------------------
def getArrowStyle(style):
    arrow = "-stealth"

    if (style.find('shape=flexArrow') != -1):
        arrow = "line width=2mm, -{Stealth[line width=1mm,inset=0pt, width=8mm, length=7mm, open]}"
    elif(style.find('shape=mxgraph.arrows2.arrow;') != -1):
        arrow = "line width=1mm, double distance=3pt, -{Stealth[line width=1mm,inset=0pt, width=8mm, length=7mm, open]}"
    elif (style.find("endArrow=cross") != -1):
        arrow = "-Rays"
    elif (style.find("endArrow=openThin;") != -1 or style.find("endArrow=block;") != -1 and style.find("endFill=1;") != -1):
        arrow = "-Latex"
    elif ((style.find("endArrow=openThin;") != -1 or style.find("endArrow=block;") != -1) and style.find("endFill=0;") != -1):
        arrow = "-{Latex[open]}"
    elif (style.find("endArrow=oval;") != -1):
        arrow = "-Circle"
    elif (style.find("endArrow=circle;") != -1):
        arrow = "-{Circle[open]}"
    elif (style.find("endArrow=diamondThin;") != -1 and style.find("endFill=1;") != -1):
        arrow = "-Diamond"
    elif (style.find("endArrow=diamondThin;") != -1 and style.find("endFill=0;") != -1):
        arrow = "-{Diamond[open]}"
    elif (style.find("endArrow=doubleBlock;") != -1 and style.find("endFill=0;") != -1):
        arrow = "-{Latex[open] Latex[open]}"
    elif (style.find("endArrow=doubleBlock;") != -1 and style.find("endFill=1;") != -1):
        arrow = "-{Latex[] Latex[]}"
    elif (style.find("endArrow=open;") != -1):
        arrow = "->"
    elif (style.find("endArrow=none;") != -1):
        arrow = arrow.replace("-stealth", "-")

    if(style.find("startArrow=classic;") != -1):
        arrow = "stealth" + arrow
    elif (style.find("startArrow=cross") != -1):
        arrow = "Rays" + arrow
    elif (style.find("startArrow=openThin;") != -1 or style.find("startArrow=block;") != -1 and style.find("startFill=1;") != -1):
        arrow = "Latex" + arrow
    elif ((style.find("startArrow=openThin;") != -1 or style.find("startArrow=block;") != -1) and style.find("startFill=0;") != -1):
        arrow = "{Latex[open]}" + arrow
    elif (style.find("startArrow=oval;") != -1):
        arrow = "Circle" + arrow
    elif (style.find("startArrow=circle;") != -1):
        arrow = "{Circle[open]}" + arrow
    elif (style.find("startArrow=diamondThin;") != -1 and style.find("startFill=1;") != -1):
        arrow = "Diamond" + arrow
    elif (style.find("startArrow=diamondThin;") != -1 and style.find("startFill=0;") != -1):
        arrow = "{Diamond[open]}" + arrow
    elif (style.find("startArrow=doubleBlock;") != -1 and style.find("startFill=0;") != -1):
        arrow = "{Latex[open] Latex[open]}" + arrow
    elif (style.find("startArrow=doubleBlock;") != -1 and style.find("startFill=1;") != -1):
        arrow = "{Latex[] Latex[]}" + arrow
    elif (style.find("endArrow=open;") != -1):
        arrow = "->"

    #TODO i need a better solution here probably -> need to rethink this whole if -> very complicated concept

    if(((style.find("endArrow=none") != -1 or style.find("endArrow") == -1)
            and (style.find("startArrow=none") != -1 or style.find("startArrow") == -1)
            and ((style.find("startArrow") != -1 and style.find("endArrow=none") != -1)
             or (style.find("endArrow") != -1 and style.find("startArrow=none") != -1))) and arrow == '-'):
        arrow = None

    return arrow


# ------------------------------------------------------
def getAmplitude(turnedUpOrDown, width, height):
    if(turnedUpOrDown):
        amplitude = height * divisorfactor.X
    else:
        amplitude = width * divisorfactor.X
    amplitude = ', amplitude={0:.1f}mm'.format(amplitude)
    return amplitude


# ------------------------------------------------------
def getAlign(text, splittedStyle, style):
    if(style.find("verticalAlign=top") != -1 and getHorizontal(style) != ''):
        return "NoAlign"
    align = findAndReturnInSplitted(splittedStyle, "align")
    if((align == None or align == 'None') and text.find("text-align:") != -1):
        alignment = text[text.find("text-align:") + len("text-align: "):]
        alignment = alignment[:alignment.find(";")]
        align = alignment
    return align


# ------------------------------------------------------
def getEllipseForm(currentStyle):
    ellipse = ''
    if(currentStyle.find("shape=orEllipse") != -1):
        ellipse = ',or'
    elif(currentStyle.find("shape=sumEllipse") != -1):
        ellipse = ',sum'
    return ellipse


# ------------------------------------------------------
def getStyleEllipse(ellipse, tree):
    for child in tree.iter():
        if (child.tag == "mxCell"):
            style = child.attrib.get("style")
            if (style == None):
                continue
            ellipseSum = r"""\tikzset{sum/.style={path picture={\draw[black](path picture bounding box.south east) -- (path picture bounding box.north west)
                (path picture bounding box.south west) -- (path picture bounding box.north east);}}}"""
            ellipseOr = r"""\tikzset{or/.style={path picture={\draw[black](path picture bounding box.south) -- (path picture bounding box.north)
                (path picture bounding box.west) -- (path picture bounding box.east);}}}"""
            if(style.find("shape=orEllipse") != -1 and ellipse.find(ellipseSum) == -1):
                ellipse += ellipseSum
                print(ellipseOr)
            elif(style.find("shape=sumEllipse") != -1 and ellipse.find(ellipseOr) == -1):
                ellipse += ellipseOr
                print(ellipseSum)

    return ellipse


# ------------------------------------------------------
def getLogicType(style):
    logicType = "and port"
    if(style.find("operation=and;") != -1):
        logicType = "and port"
    elif(style.find("operation=xor;") != -1):
        logicType = "xor port"
    elif(style.find("operation=or;") != -1):
        logicType = "or port"
    elif(style.find("operation=xnor;") != -1):
        logicType = "xnor port"
    elif(style.find("operation=nor;") != -1):
        logicType = "nor port"
    elif(style.find("operation=nand;") != -1):
        logicType = "nand port"
    elif(style.find(".nmos;") != -1):
        logicType = "nmos"
    elif(style.find(".pmos;") != -1):
        logicType = "pmos"
    elif(style.find("singleSwitch;") != -1):
        logicType = "spdt"
    elif(style.find("mxgraph.electrical.diodes.") != -1):
        logicType = "put"

    return logicType

# ------------------------------------------------------
def getTransistorRotation(style):
    rotate = ''
    if(style.find("direction=south;") != -1):
        rotate = ",rotate=270"
    elif(style.find("direction=north;") != -1):
        rotate = ",rotate=90"
    elif(style.find("direction=east;") != -1):
        rotate = ",rotate=180"
    elif(style.find("direction=west;") != -1):
        rotate = ""
    return rotate


# ------------------------------------------------------
def getTransistorScale(style):
    scale = ''
    if(style.find("nmos") != -1 or style.find("pmos") != -1):
        scale = ",scale={0:}".format(divisorfactor.Y)

    return scale


# ------------------------------------------------------
def getTransistorCoordinates(rotate, startPoint, endPoint, middle):
    coordinates = Coordinates(middle.X, middle.Y)
    if(rotate == ",rotate=270"):
        coordinates.Y = endPoint.Y
    elif(rotate == ",rotate=180"):
        coordinates.X = startPoint.X
    elif(rotate == ",rotate=90"):
        coordinates.Y = startPoint.Y
    elif(rotate == ''):
        coordinates.X = endPoint.X
    return coordinates


# ------------------------------------------------------
def getInOut(mapObjectCoordinates, source, target, sourcePoint, targetPoint, entry, exit, bracePositions):
    inOut = 'in=180,out=90,'
    if(source != None and mapObjectCoordinates.get(source) != None):
        sourcePoint = Coordinates(mapObjectCoordinates.get(source).X,mapObjectCoordinates.get(source).Y)
    if(target != None and mapObjectCoordinates.get(target) != None):
        targetPoint = Coordinates(mapObjectCoordinates.get(target).X,mapObjectCoordinates.get(target).Y)

#TODO this might need more fine tuning -> is fine i think
    if(sourcePoint.X < targetPoint.X and sourcePoint.Y < targetPoint.Y):
        inOut = 'in=270,out=0,'
    elif(sourcePoint.X > targetPoint.X and sourcePoint.Y < targetPoint.Y):
        inOut = 'in=270,out=180,'
    elif (sourcePoint.X > targetPoint.X and sourcePoint.Y > targetPoint.Y):
        inOut = 'in=90,out=180,'
    elif (sourcePoint.X < targetPoint.X and sourcePoint.Y > targetPoint.Y):
        inOut = 'in=90,out=0,'
    elif(sourcePoint.X == targetPoint.X and sourcePoint.Y < targetPoint.Y):
        inOut = 'in=90,out=270,'
    elif(sourcePoint.X > targetPoint.X and sourcePoint.Y == targetPoint.Y):
        inOut = 'in=0,out=180,'
    elif (sourcePoint.X == targetPoint.X and sourcePoint.Y > targetPoint.Y):
        inOut = 'in=90,out=270,'
    elif (sourcePoint.X < targetPoint.X and sourcePoint.Y == targetPoint.Y):
        inOut = 'in=180,out=0,'

    if(entry.find("north") != -1):
        inOut = "in=90" + inOut[inOut.find(','):]
    elif(entry.find("south") != -1):
        inOut = "in=270" + inOut[inOut.find(','):]
    elif(entry.find("west") != -1):
        inOut = "in=180" + inOut[inOut.find(','):]
    elif(entry.find("east") != -1):
        inOut = "in=0" + inOut[inOut.find(','):]

    if(exit.find("north") != -1):
        inOut = inOut[:inOut.find(',')] + ",out=90,"
    elif (exit.find("south") != -1):
        inOut = inOut[:inOut.find(',')] + ",out=270,"
    elif (exit.find("west") != -1):
        inOut = inOut[:inOut.find(',')] + ",out=180,"
    elif (exit.find("east") != -1):
        inOut = inOut[:inOut.find(',')] + ",out=0,"

    if (bracePositions.get(source) != None):
        inOut = inOut[:inOut.find(',')] + ",out=90,"
    if (bracePositions.get(target) != None):
        inOut = "in=90" + inOut[inOut.find(','):]

    return inOut


# ------------------------------------------------------
def getChildrenMxPoint(i, tree):
    children = [Coordinates(defaultPointValue,defaultPointValue), Coordinates(defaultPointValue,defaultPointValue)]
    for index in range(i, i+4):
        if(len(list(tree.iter())) <= index):
            return children
        if(list(tree.iter())[index].get("as") == "sourcePoint"):
            if(list(tree.iter())[index].get("x") != None):
                children[0].X = float(list(tree.iter())[index].get("x")) / divisorfactor.X
            else:
                children[0].X = 0
            if (list(tree.iter())[index].get("y") != None):
                children[0].Y = -float(list(tree.iter())[index].get("y")) / divisorfactor.X
            else:
                children[0].Y = 0
        elif(list(tree.iter())[index].get("as") == "targetPoint"):
            if(list(tree.iter())[index].get("x") != None):
                children[1].X = float(list(tree.iter())[index].get("x")) / divisorfactor.X
            else:
                children[1].X = 0
            if (list(tree.iter())[index].get("y") != None):
                children[1].Y = -float(list(tree.iter())[index].get("y")) / divisorfactor.X
            else:
                children[1].Y = 0

    return children


# ------------------------------------------------------
def adjustPoints(pointToAdjust, mxPoints, start):
    if(start):
        if(mxPoints[0].X != defaultPointValue):
            pointToAdjust.X = mxPoints[0].X
        if(mxPoints[0].Y != defaultPointValue):
            pointToAdjust.Y = mxPoints[0].Y
    else:
        if(mxPoints[1].X != defaultPointValue):
            pointToAdjust.X = mxPoints[1].X
        if(mxPoints[1].Y != defaultPointValue):
            pointToAdjust.Y = mxPoints[1].Y
    return pointToAdjust


# ------------------------------------------------------
def setup(mytree):
    divisorfactor.Y = calculateDivisorFactor(mytree, True)
    divisorfactor.X = divisorfactor.Y * 2
    scale = 1 / divisorfactor.Y
    if (divisorfactor.Y > 1):
        print(r"\hspace{-%dcm}" % (divisorfactor.Y - 1))
    print(r"\begin{tikzpicture}[scale = %.2f]" % scale)
    circledFound = False
    mergeFound = False
    checkMark = False
    styleEllipse = ''
    alreadyDefinedColours = []
    for child in mytree.iter():
        if (child.tag == "mxCell"):
            text = getText(child)
            style = child.attrib.get("style")
            if (style == None):
                continue

            alreadyDefinedColours = printStrokeColour(style, alreadyDefinedColours)
            alreadyDefinedColours = printFillColour(style, alreadyDefinedColours)
            alreadyDefinedColours = printFontColour(text, style, alreadyDefinedColours)
            styleEllipse = getStyleEllipse(styleEllipse, mytree)

            if (circledFound == False and text != replaceCircledUnicode(text)):
                circledFound = True
            if (style.find("shape=mxgraph.flowchart.merge_or_storage") != -1):
                mergeFound = True
            if(style.find("shape=mxgraph.gcp2.check") != -1):
                checkMark = True

    if (circledFound == True):
        print(r"\newcommand*\circled[1]{\tikz[baseline=(char.base)]"
              r"{\node[shape=circle,draw,inner sep=0.5pt] (char) {#1};}}")
    if (mergeFound == True):
        print(r"""\tikzset{
    merge/.style={draw,isosceles triangle,isosceles triangle apex angle=60,shape border rotate=-90,align=center},}""")
    if(checkMark == True):
        print(r"\newcommand{\Checkmark}{$\color{green}\checkmark$}")


# ------------------------------------------------------
def start(argv):
    eltree = parseArguments(argv)
    setup(eltree)
    return eltree


# ------------------------------------------------------
def end(tree, mapRemaining):
    if (len(mapRemaining) != 0):
        for object_left in mapRemaining:
            print(r"% this object was not supported and could not be translated:" + object_left + " MIGHT cause errors")
    print(r"\end{tikzpicture}")
    calculateDivisorFactor(tree, False)


# ------------------------------------------------------
def printRectangles(currentStyle, strokeColor, rounded,
                    mapObjectsRemaining, objectID, splittedStyle,
                    currentText, endPoint, startPoint,
                    filterText, align, rotation,
                    width, height, middle,
                    linestyle, innerSep):

    if (rounded != None and int(rounded) == 1 and currentStyle.find("shape=mxgraph.basic.rect") == -1):
        corners = 'rounded corners,'
    else:
        corners = ''
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    fillColor = getFillColour(splittedStyle)
    if (currentText != ""):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
        fontColor = getFontColour(filterText, currentStyle)
        if (align == None or align == 'None'):
            align = "align=center"
        elif(align == "NoAlign"):
            align = 'align=none'
        else:
            align = "align=" + align

        if (rotation != None):
            if (rotation == 90 or rotation == 270):
                tmp = width
                width = height
                height = tmp
                textWidth = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
            print(
                r"\node at %s [%s%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f "
                r"cm,text width=%.1fcm%s%s](%s) {\rotatebox[]{%s}{%s}};" %
                ((middle.X, middle.Y), corners, align, fillColor, linestyle, strokeColor, width, height, textWidth,
                 innerSep, fontColor, objectID, rotation, currentText))
        else:
            print(
                r"\node at %s [%s%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,text width=%.1fcm%s%s]("
                r"%s) {%s};" %
                ((middle.X, middle.Y), corners, align, linestyle, strokeColor, fillColor, width, height,
                 textWidth, innerSep, fontColor, objectID, currentText))

    elif (rotation != None):
        print(
            r"\node at (%.1f,%.1f) [%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,rotate=%s%s](%s){};" %
            (middle.X, middle.Y, corners, strokeColor[1:], fillColor, linestyle, width, height, rotation,
             innerSep, objectID))
    else:
        print(
            r"\node at (%.1f,%.1f) [%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s](%s){};" %
            (middle.X, middle.Y, corners, strokeColor[1:], fillColor, linestyle, width, height, innerSep, objectID))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCircles(mapObjectsRemaining, objectID, strokeColor,
                 splittedStyle, currentText, filterText,
                 endPoint, startPoint, align,
                 currentStyle, rotation, middle,
                 linestyle, width, height, innerSep):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    fillColor = getFillColour(splittedStyle)

    ellipse = getEllipseForm(currentStyle)

    aspect = 'circle'
    if(currentStyle.find("aspect=fixed") == -1):
        aspect = "ellipse"
        if(width > 1):
            width = int(width)
        if(height > 1):
            height = int(height)

    if (currentText != ''):
        textWidth = width
        if (align != None):
            align = ',align=' + align
        else:
            align = ',align=center'
        fontColor = getFontColour(filterText, currentStyle)
        textWidth = ',text width=' + "{0:.1f}".format(textWidth) + 'cm'
        if (rotation != None and int(rotation) % 360 != 0):
            currentText = r'{\rotatebox[]{' + "{0:.1f}".format(-rotation) + '}' + currentText + '}'
        print(r"\node at %s[%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), aspect, ellipse, linestyle, width, height, textWidth, align, strokeColor, fillColor, innerSep,
               fontColor, objectID, currentText))
    else:
        print(r"\node at %s[%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), aspect, ellipse, linestyle, width, height, strokeColor, fillColor, innerSep, objectID, currentText))
    return mapObjectsRemaining


# ------------------------------------------------------
def printClouds(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height, innerSep):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    fillColor = getFillColour(splittedStyle)
    width = width / 2
    height = height / 2
    aspect = ''
    if (currentStyle.find("aspect=fixed") == -1):
        aspect = ",aspect={0:.1f}".format(width/height)
    if (currentText != ''):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.X)
        if (align != None):
            align = ',align=' + align
        else:
            align = ',align=center'
        fontColor = getFontColour(filterText, currentStyle)
        textWidth = ',text width=' + "{0:.1f}".format(textWidth) + 'cm'
        if (rotation != None and int(rotation) % 360 != 0):
            currentText = r'{\rotatebox[]{' + "{0:.1f}".format(-rotation) + '}' + currentText + '}'
        print(r"\node at %s[cloud%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), aspect, linestyle, width, height, textWidth, align, strokeColor, fillColor, innerSep,
               fontColor, objectID, currentText))
    else:
        print(r"\node at %s[cloud%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), aspect, linestyle, width, height, strokeColor, fillColor, innerSep, objectID, currentText))
    return mapObjectsRemaining


# ------------------------------------------------------
def printRhombus(mapObjectsRemaining, objectID, strokeColor,
                 splittedStyle, currentText, filterText,
                 endPoint, startPoint, align,
                 currentStyle, rotation, middle,
                 linestyle, width, height, innerSep):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    fillColor = getFillColour(splittedStyle)
    if (currentText != ''):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
        if (align != None):
            align = ',align=' + align
        else:
            align = ',align=center'
        fontColor = getFontColour(filterText, currentStyle)
        textWidth = ',text width=' + "{0:.1f}".format(textWidth) + 'cm'

        if (rotation != None and int(rotation) % 360 != 0):
            rotation = ',rotate=' + "{0:.1f}".format(-rotation)
        else:
            rotation = ''
        print(
            r"\node at %s[diamond%s,aspect=2,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s%s%s%s](%s){%s};" %
            ((middle.X, middle.Y), linestyle, width, height, textWidth, align, strokeColor, fillColor, innerSep,
             fontColor, rotation, objectID, currentText))
    else:
        print(r"\node at %s[diamond%s,aspect=2,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), linestyle, width, height, strokeColor, fillColor, innerSep, rotation, objectID, currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printText(mapObjectsRemaining, objectID, currentText,
              filterText, endPoint, parent,
              startPoint, align, currentStyle,
              rotation, innerSep, pureText):

    # print(objectID)
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    # if (currentText == ''):
    #     return mapObjectsRemaining
    if (align == None or align == 'None'):
        align = "center"

    fillColor = getFillColour(currentStyle.split(';'))
    fontColor = getFontColour(filterText, currentStyle)
    width = abs((endPoint.X - startPoint.X) / divisorfactor.Y) + 0.1
    textWidth = ", text width = {0:.1f}".format(width) + " cm"
    textCharacterFactor = 0.2


    if(mapObjects.get(getIDNumber(parent)) != None and mapObjects.get(getIDNumber(parent)).find("swimlane;") != -1):
        textWidth = ", text width = {0:.1f}".format(int(width)) + "cm"
        innerSep = getSpacing(currentStyle.split(';') , 2)

    #do not adapt X Coordinate or the textbox will be moved too far
    if(currentStyle.find("points=[[") != -1):
        startpoints = currentStyle[currentStyle.find("points=[[") + len("points=[["):]
        endpoints = startpoints[startpoints.find("[") + 1:]
        startpoints = startpoints[:startpoints.find("]")]
        endpoints = endpoints[:endpoints.find("]")]
        startpoints = startpoints.split(',')
        endpoints = endpoints.split(',')
        startPoint.Y += float(startpoints[1])
        endPoint.Y += float(endpoints[1])

    if(currentStyle.find("overflow=hidden") != -1 and int(width) / len(pureText) < textCharacterFactor):
        textWidth = ''

    if (currentStyle.find("edgeLabel") != -1 and parent == '1'):
        endPoint.X = startPoint.X
        endPoint.Y = startPoint.Y
        textWidth = ''

    if (rotation != None and rotation != 0):
        print(r"\draw [draw=none] (%.1f,%.1f) rectangle node(%s)"
              r"[align = %s%s,  rotate=%s%s%s%s]{%s} (%.1f,%.1f);" % (
                  startPoint.X, startPoint.Y, objectID, align, textWidth, rotation, innerSep, fontColor, fillColor,
                  currentText, endPoint.X, endPoint.Y))
    else:
        print(r"\draw [draw=none] (%.1f,%.1f) rectangle node(%s)"
              r"[align = %s%s%s%s%s] {%s} (%.1f,%.1f);" % (
                  startPoint.X, startPoint.Y, objectID, align, textWidth, innerSep, fontColor, fillColor,
                  currentText, endPoint.X, endPoint.Y))
    return mapObjectsRemaining


# ------------------------------------------------------
def printMerge(mapObjectsRemaining, objectID, middle, currentText):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    print(r"\node(%s)[merge] at (%.1f,%.1f) {%s};" % (objectID, middle.X, middle.Y, currentText))
    return mapObjectsRemaining


# ------------------------------------------------------
#TODO not sure how to deal with images -> leave it be for now
def printImages(mapObjectsRemaining, objectID, middle, currentText, style):
        mapObjectsRemaining.pop(objectID)
        # image = style[style.find("image=") + len("image="):]
        # image = image[:style.find(";") + 1]
        # imageEncoded = image.encode("utf-8")
        # imageDecoded = imageEncoded.decode()
        if(style.find("verticalLabelPosition=bottom") and currentText != ''):
            print(r"%\vspace")
        print(
            r"\node at (%.1f,%.1f) [](%s){%s};" %
            (middle.X, middle.Y, objectID, currentText))
        return mapObjectsRemaining


# ------------------------------------------------------
def printPartialRectangles(currentStyle, strokeColor,
                           mapObjectsRemaining, objectID,
                           currentText, endPoint, startPoint,
                           filterText, align, rotation,
                           width, height, middle,
                           linestyle, innerSep, tableFillColour):

    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    if (currentText != ""):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
        fontColor = getFontColour(filterText, currentStyle)
        if (align == None or align == 'None'):
            align = "align=center"
        else:
            align = "align=" + align

        if (rotation != None):
            if (rotation == 90 or rotation == 270):
                tmp = width
                width = height
                height = tmp
                textWidth = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
            print(
                r"\node at %s [%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f "
                r"cm,text width=%.1fcm%s%s](%s) {\rotatebox[]{%s}{%s}};" %
                ((middle.X, middle.Y), align, tableFillColour, linestyle, strokeColor, width, height, textWidth,
                 innerSep, fontColor, objectID, rotation, currentText))
        else:
            print(
                r"\node at %s [%s%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,text width=%.1fcm%s%s]("
                r"%s) {%s};" %
                ((middle.X, middle.Y), align, linestyle, strokeColor, tableFillColour, width, height,
                 textWidth, innerSep, fontColor, objectID, currentText))

    elif (rotation != None):
        print(
            r"\node at (%.1f,%.1f) [%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,rotate=%s%s](%s){};" %
            (middle.X, middle.Y, strokeColor[1:], tableFillColour, linestyle, width, height, rotation,
             innerSep, objectID))
    else:
        print(
            r"\node at (%.1f,%.1f) [%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s](%s){};" %
            (middle.X, middle.Y, strokeColor[1:], tableFillColour, linestyle, width, height, innerSep, objectID))

    return mapObjectsRemaining


# ------------------------------------------------------
def printSwimlanes(currentStyle, strokeColor,
                      mapObjectsRemaining, objectID,
                      currentText, endPoint, startPoint,
                      filterText, align, rotation,
                      width, height, middle,
                      linestyle, innerSep):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    print(r"\begin{scope}[shift={(%0.1f,%0.1f)}]" % (startPoint.X, startPoint.Y))
    position = Coordinates(round(middle.X - startPoint.X, 2), round(middle.Y - startPoint.Y, 2))
    fillColor = getFillColour(currentStyle.split(';'))
    startSize = currentStyle[currentStyle.find("startSize=") + len("startSize="):]
    positionFactor = 10/3
    startSize = int(startSize[:startSize.find(';')]) / 100

    if (currentText != ""):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
        fontColor = getFontColour(filterText, currentStyle)
        if (align == None or align == 'None'):
            align = "align=center"
        else:
            align = "align=" + align

        currentText = currentText.replace(" ", r" \vspace{" + str(round(height - startSize, 2) ) + "cm}", 1)
        height += startSize - round(startSize/3, 1)

        if (rotation != None):
            if (rotation == 90 or rotation == 270):
                tmp = width
                width = height
                height = tmp
                textWidth = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
            print(r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s]{\rotatebox[]{%s}{}};" % (
                (position.X,  -(startSize * positionFactor)), linestyle[1:], strokeColor, width, startSize * 2, fillColor, rotation))
            print(
                r"\node at %s [%s%s%s,minimum width=%.1f cm,minimum height=%.1f "
                r"cm,text width=%.1fcm%s%s](%s) {\rotatebox[]{%s}{%s}};" %
                ((position.X, position.Y), align, linestyle, strokeColor, width, height, textWidth,
                 innerSep, fontColor, objectID, rotation, currentText))
        else:
            print(r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s]{};" % (
                (position.X,  -(startSize * positionFactor)), linestyle[1:], strokeColor, width, startSize * 2, fillColor))
            print(
                r"\node at %s [%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,text width=%.1fcm%s%s]("
                r"%s) {%s};" %
                ((position.X, position.Y), align, linestyle, strokeColor, width, height,
                 textWidth, innerSep, fontColor, objectID, currentText))

    elif (rotation != None):
        print(r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s]{\rotatebox[]{%s}{}};" % (
            (position.X, -(startSize * positionFactor)), linestyle[1:], strokeColor, width, startSize * 2, fillColor, rotation))
        print(
            r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm,rotate=%s%s](%s){};" %
            ((position.X, position.Y), strokeColor[1:], linestyle, width, height, rotation,
             innerSep, objectID))
    else:
        print(r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s]{};" % (
            (position.X, -(startSize * positionFactor)), linestyle[1:], strokeColor, width, startSize * 2, fillColor))
        print(
            r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s](%s){};" %
            ((position.X, position.Y), strokeColor[1:], linestyle, width, height, innerSep, objectID))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCrosses(mapObjectsRemaining, objectID, strokeColor,
                   splittedStyle, currentText, filterText,
                   endPoint, startPoint, align,
                   currentStyle, rotation, middle,
                   linestyle, width, height,
                   innerSep, lineWidth):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    fillColor = getFillColour(splittedStyle)

    if (lineWidth == ''):
        lineWidth = ",line width=4mm"

    if (currentText != ''):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.X)
        if (align != None):
            align = ',align=' + align
        else:
            align = ',align=center'
        fontColor = getFontColour(filterText, currentStyle)
        textWidth = ',text width=' + "{0:.1f}".format(textWidth) + 'cm'
        if (rotation != None and int(rotation) % 360 != 0):
            currentText = r'{\rotatebox[]{' + "{0:.1f}".format(-rotation) + '}' + currentText + '}'
        print(r"\node at %s[cross out%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), linestyle, lineWidth, width, height, textWidth, align, strokeColor, fillColor, innerSep,
               fontColor, objectID, currentText))
    else:
        fillColor = fillColor.replace(",text opacity=1", "")
        print(r"\node at %s[cross out%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), linestyle, lineWidth, width, height, strokeColor, fillColor, innerSep, objectID, currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printTable(currentStyle, strokeColor,
               mapObjectsRemaining, objectID,
               currentText, endPoint, startPoint,
               filterText, align, rotation,
               width, height, middle,
               linestyle, innerSep):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    position = Coordinates(round(middle.X - startPoint.X, 2), round(middle.Y - startPoint.Y, 2))
    startSize = currentStyle[currentStyle.find("startSize=") + len("startSize="):]
    startSize = int(startSize[:startSize.find(';')]) / 100

    if (currentText != ""):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
        fontColor = getFontColour(filterText, currentStyle)
        if (align == None or align == 'None'):
            align = "align=center"
        else:
            align = "align=" + align

        currentText = r" \vspace{" + str(int(height - startSize)) + "cm}" + currentText

        if (rotation != None):
            if (rotation == 90 or rotation == 270):
                tmp = width
                width = height
                height = tmp
                textWidth = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
            print(
                r"\node at %s [%s%s%s,minimum width=%.1f cm,minimum height=%.1f "
                r"cm,text width=%.1fcm%s%s](%s) {\rotatebox[]{%s}{%s}};" %
                ((position.X, position.Y), align, linestyle, strokeColor, width, height, textWidth,
                 innerSep, fontColor, objectID, rotation, currentText))
        else:
            print(
                r"\node at %s [%s%s%s,minimum width=%.1f cm,minimum height=%.1f cm,text width=%.1fcm%s%s]("
                r"%s) {%s};" %
                ((position.X, position.Y), align, linestyle, strokeColor, width, height,
                 textWidth, innerSep, fontColor, objectID, currentText))

    elif (rotation != None):
        print(
            r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm,rotate=%s%s](%s){};" %
            ((position.X, position.Y), strokeColor[1:], linestyle, width, height, rotation,
             innerSep, objectID))
    else:
        print(
            r"\node at %s [%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s](%s){};" %
            ((position.X, position.Y), strokeColor[1:], linestyle, width, height, innerSep, objectID))


    return mapObjectsRemaining


# ------------------------------------------------------
def printArrow(mapObjectsRemaining, objectID, strokeColor,
                   endPoint, startPoint, style):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)
    arrowStyle = getArrowStyle(style)
    if(style.find("direction=south;") != -1 or style.find("direction=north;") != -1):
        print(r"\draw [%s%s](%.1f,%.1f)--(%.1f,%.1f);" % (
            arrowStyle, strokeColor, middle.X, startPoint.Y, middle.X, endPoint.Y))
    else:
        print(r"\draw [%s%s](%.1f,%.1f)--(%.1f,%.1f);" % (
            arrowStyle, strokeColor, startPoint.X, middle.Y, startPoint.X, middle.Y))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCylinders(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height,
                                           innerSep, lineWidth):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    fillColor = getFillColour(splittedStyle)
    if (currentText != ''):
        textWidth = abs((endPoint.X - startPoint.X) / divisorfactor.X)
        if (align != None):
            align = ',align=' + align
        else:
            align = ',align=center'
        fontColor = getFontColour(filterText, currentStyle)
        textWidth = ',text width=' + "{0:.1f}".format(textWidth) + 'cm'
        if(rotation == None):
            rotation = 0
        rotation = int(rotation) + 90
        currentText = r'{\rotatebox[]{' + "{0:.1f}".format(-rotation) + '}{' + currentText + '}}'
        rotation = ",rotate={0:}".format(rotation)
        print(r"\node at %s[cylinder%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s%s%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), linestyle, lineWidth, width, height, textWidth, align, strokeColor, fillColor, innerSep,
               fontColor, rotation, objectID, currentText))
    else:
        fillColor = fillColor.replace(",text opacity=1", "")
        print(r"\node at %s[cylinder%s%s,minimum width=%.1f cm,minimum height=%.1f cm%s%s%s](%s){%s};" %
              ((middle.X, middle.Y), linestyle, lineWidth, width, height, strokeColor, fillColor, innerSep, objectID, currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCheckmarks(mapObjectsRemaining, objectID, endPoint, startPoint):

    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    checkMark = r"\Checkmark"
    scale = "scale={0:}".format(divisorfactor.Y)
    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)

    print(r"\node at (%.1f,%.1f)[%s](%s){%s};" % (
        middle.X, middle.Y, scale, objectID, checkMark))

    return mapObjectsRemaining


# ------------------------------------------------------
def printLogicShapes(mapObjectsRemaining, objectID, endPoint, startPoint, style):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    logicType = getLogicType(style)
    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)

    rotate = getTransistorRotation(style)
    scale = getTransistorScale(style)
    coordinates = getTransistorCoordinates(rotate, startPoint, endPoint, middle)

    if(style.find("nmos") != -1 or style.find("pmos") != -1):
        print(r"\node at (%.1f,%.1f)[%s%s%s](%s){};" % (
            coordinates.X, coordinates.Y, logicType, rotate, scale, objectID))
    elif(style.find("mxgraph.electrical.diodes") != -1):
        print(r"\draw (%.1f,%.1f)node[%s,draw](%s){};" % (middle.X, middle.Y, logicType, objectID))
    else:
        print(r"\node at (%.1f,%.1f)[%s%s%s](%s){};" % (
            middle.X, middle.Y, logicType, rotate, scale, objectID))

    return mapObjectsRemaining


# ------------------------------------------------------
def printStraightArrows(mapObjectsRemaining, objectID, child, lineWidth,
                        splittedStyle, target,
                        arrowStyle, strokeColor, linestyle,
                        currentText, source, targetPoint,
                        sourcePoint, bracePositions, mapObjectCoordinates,
                        previousChild, mxPoints):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    for element in list(child):
        if (element.get("as") == "sourcePoint"):
            sourcePoint = Coordinates(float(element.attrib.get("x")) / divisorfactor.X,
                                      -float(element.attrib.get("y")) / divisorfactor.X)
        if (element.get("as") == "targetPoint"):
            targetPoint = Coordinates(float(element.attrib.get("x")) / divisorfactor.X,
                                      -float(element.attrib.get("y")) / divisorfactor.X)
    exitAnchor = findExitAnchor(source, splittedStyle)
    entryAnchor = findEntryAnchor(target, splittedStyle)

    if (bracePositions.get(source) != None):
        sourcePoint = Coordinates(bracePositions.get(source).X, bracePositions.get(source).Y)
        source = None
    elif (bracePositions.get(target) != None):
        targetPoint = Coordinates(bracePositions.get(target).X, bracePositions.get(target).Y)
        target = None

    controls = getOrthogonalControls(child, entryAnchor, exitAnchor, previousChild, mapObjectCoordinates, source, target, targetPoint)

    if (strokeColor != ''):
        strokeColor = ',' + strokeColor

    sourcePoint = adjustPoints(sourcePoint, mxPoints, True)
    targetPoint = adjustPoints(targetPoint, mxPoints, False)
    if (source == None and target != None):
            print(r"\draw [%s%s%s%s](%.1f,%.1f)%s(%s%s)%s;" % (
                arrowStyle, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, target, entryAnchor, currentText))

    elif (target == None and source != None):
                print(r"\draw [%s%s%s%s](%s%s)%s(%.1f,%.1f)%s;" % (
                    arrowStyle, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, targetPoint.X, targetPoint.Y,
                    currentText))

    elif (source != None and target != None):
            print(r"\draw [%s%s%s%s](%s%s)%s(%s%s)%s;" % (
                arrowStyle, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, target, entryAnchor, currentText))

    elif (source == None and target == None):
            print(r"\draw [%s%s%s%s](%.1f,%.1f)%s(%.1f,%.1f)%s;" % (
                arrowStyle, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, targetPoint.X,
                targetPoint.Y, currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCurvedArrows(mapObjectsRemaining, objectID, child,
                      splittedStyle, target, lineWidth,
                      arrowStyle, strokeColor, linestyle,
                      currentText, source, targetPoint,
                      sourcePoint, bracePositions, mapObjectCoordinates,
                      mxPoints):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    arc = getArc(splittedStyle)
    exitAnchor = findExitAnchor(source, splittedStyle)
    entryAnchor = findEntryAnchor(target, splittedStyle)

    for element in list(child):
        if (element.get("as") == "sourcePoint"):
            sourcePoint = getSourcePoint(element, sourcePoint)
            sourcePoint.Y -= arc
        if (element.get("as") == "targetPoint"):
            targetPoint = getTargetPoint(element, targetPoint)
            targetPoint.Y -= arc

    if (len(list(child)) > 0):
        controls = getCurvedControls(list(child[-1]), arc)
        arrowInOut = ''
        if(controls == "to"):
            arrowInOut = getInOut(mapObjectCoordinates, source, target, sourcePoint, targetPoint, entryAnchor, exitAnchor, bracePositions)
    else:
        controls = "to"
        arrowInOut = getInOut(mapObjectCoordinates, source, target, sourcePoint, targetPoint, entryAnchor, exitAnchor, bracePositions)

    if (strokeColor != ''):
        strokeColor = ',' + strokeColor

    sourcePoint = adjustPoints(sourcePoint, mxPoints, True)
    targetPoint = adjustPoints(targetPoint, mxPoints, False)
    if (source == None and target != None):
            print(r"\draw [%s%s%s%s%s](%.1f,%.1f)%s(%s%s)%s;" % (
                arrowInOut, arrowStyle, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, target, entryAnchor,
                currentText))

    elif (target == None and source != None):
            print(r"\draw [%s%s%s%s%s](%s%s)%s(%.1f,%.1f)%s;" % (
                arrowInOut, arrowStyle, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, targetPoint.X, targetPoint.Y,
                currentText))

    elif (source != None and target != None):
            print(r"\draw [%s%s%s%s%s](%s%s)%s(%s%s)%s;" % (
                arrowInOut, arrowStyle, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, target, entryAnchor,
                currentText))

    elif (source == None and target == None):
            print(r"\draw [%s%s%s%s%s](%.1f,%.1f)%s(%.1f,%.1f)%s;" % (
                arrowInOut, arrowStyle, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, targetPoint.X,
                targetPoint.Y, currentText))
    return mapObjectsRemaining


# ------------------------------------------------------
def printStraightLines(mapObjectsRemaining, objectID, child, lineWidth,
                       splittedStyle, target, strokeColor, linestyle,
                       currentText, source, targetPoint,
                       sourcePoint, bracePositions, mapObjectCoordinates,
                       previousChild, mxPoints):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    exitAnchor = findExitAnchor(source, splittedStyle)
    entryAnchor = findEntryAnchor(target, splittedStyle)
    if (bracePositions.get(source) != None):
        sourcePoint = Coordinates(bracePositions.get(source).X, bracePositions.get(source).Y)
        source = None
    elif (bracePositions.get(target) != None):
        targetPoint = Coordinates(bracePositions.get(target).X, bracePositions.get(target).Y)
        target = None

    controls = getOrthogonalControls(child, entryAnchor, exitAnchor, previousChild, mapObjectCoordinates, source, target, targetPoint)
    if(strokeColor != ''):
        strokeColor = ',' + strokeColor

    for element in list(child):
        sourcePoint = getSourcePoint(element, sourcePoint)
        targetPoint = getTargetPoint(element, targetPoint)

    sourcePoint = adjustPoints(sourcePoint, mxPoints, True)
    targetPoint = adjustPoints(targetPoint, mxPoints, False)
    if (source == None and target != None):
        print(r"\draw [%s%s%s] (%.1f,%.1f)%s(%s%s)%s;" % (
            linestyle[1:], strokeColor, lineWidth, sourcePoint.X, sourcePoint.Y, controls, target, entryAnchor, currentText))

    elif (target == None and source != None):
        print(r"\draw [%s%s%s] (%s%s)%s(%.1f,%.1f)%s;" % (
            linestyle[1:], strokeColor, lineWidth, source, exitAnchor, controls, targetPoint.X, targetPoint.Y, currentText))

    elif (source != None and target != None):
            print(r"\draw [%s%s%s] (%s%s)%s(%s%s)%s;" % (
                linestyle[1:], strokeColor, lineWidth, source, exitAnchor, controls, target, entryAnchor, currentText))

    elif (source == None and target == None):
        print(r"\draw [%s%s%s] (%.1f,%.1f)%s(%.1f,%.1f)%s;" % (
            linestyle[1:], strokeColor, lineWidth, sourcePoint.X, sourcePoint.Y, controls, targetPoint.X, targetPoint.Y,
            currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCurvedLines(mapObjectsRemaining, objectID, child, lineWidth,
                     splittedStyle, target, strokeColor, linestyle,
                     currentText, source, targetPoint,
                     sourcePoint, bracePositions, mapObjectCoordinates,
                     mxPoints):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining
    arc = getArc(splittedStyle)
    for element in list(child):
        if (element.get("as") == "sourcePoint"):
            sourcePoint = getTargetPoint(element, sourcePoint)
            sourcePoint.Y -= arc
        if (element.get("as") == "targetPoint"):
            targetPoint = getTargetPoint(element, targetPoint)
            targetPoint.Y -= arc
    exitAnchor = findExitAnchor(source, splittedStyle)
    entryAnchor = findEntryAnchor(target, splittedStyle)
    if (len(list(child)) > 0):
        controls = getCurvedControls(list(child[-1]), arc)
        InOut = ''
    else:
        controls = "to"
        InOut = getInOut(mapObjectCoordinates, source, target, sourcePoint, targetPoint, entryAnchor, exitAnchor, bracePositions)

    sourcePoint = adjustPoints(sourcePoint, mxPoints, True)
    targetPoint = adjustPoints(targetPoint, mxPoints, False)
    linestyle = linestyle[1:]
    if(strokeColor != '' and linestyle != ''):
        strokeColor = strokeColor + ','

    if (source == None and target != None):
        print(r"\draw [%s%s%s%s] (%.1f,%.1f)%s(%s%s)%s;" % (
            InOut, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, target, entryAnchor, currentText))

    elif (target == None and source != None):
        print(r"\draw [%s%s%s%s] (%s%s)%s(%.1f,%.1f)%s;" % (
            InOut, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, targetPoint.X, targetPoint.Y, currentText))

    elif (source != None and target != None):
        print(r"\draw [%s%s%s%s] (%s%s)%s(%s%s)%s;" % (
            InOut, strokeColor, linestyle, lineWidth, source, exitAnchor, controls, target, entryAnchor, currentText))

    elif (source == None and target == None):
        print(r"\draw [%s%s%s%s] (%.1f,%.1f)%s(%.1f,%.1f)%s;" % (
            InOut, strokeColor, linestyle, lineWidth, sourcePoint.X, sourcePoint.Y, controls, targetPoint.X,
            targetPoint.Y, currentText))

    return mapObjectsRemaining


# ------------------------------------------------------
def printCurlyBrackets(mapObjectsRemaining, objectID, splittedStyle,
                       currentText, startPoint, endPoint,
                       rotation, width, height,
                       style, curlyBracketsFactor):
    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    offset = "[pos=0.5,rotate={0:}]".format(rotation)
    currentText = prepareLabelText(currentText, offset)
    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)

    if(style.find("flipH=1") == -1 and style.find("shape=mxgraph.flowchart.annotation_2") == -1):
        rotation = getRotation(splittedStyle, True)
        if(rotation == None):
            rotation = 180

    # 2 is an arbitrarily chosen factor by trial and error, might need some refinement
    if (width / height < curlyBracketsFactor):
        endPoint.X = middle.X
        startPoint.X = middle.X
        turnedUpOrDown = False
        #rotation 270 or 90 °
    else:
        endPoint.Y = middle.Y
        startPoint.Y = middle.Y
        turnedUpOrDown = True
        #rotation 180 or 0 °

    strokeColor = getStrokeColour(splittedStyle)
    amplitude = getAmplitude(turnedUpOrDown, width, height)

    if(turnedUpOrDown == True):
        startPoint.X = startPoint.X - height * 2
        endPoint.X = endPoint.X - height * 2
    else:
        startPoint.X = startPoint.X - width * 2
        endPoint.X = endPoint.X - width * 2

    if (rotation != None):
        rotation = r',rotate around={' + "{0:.1f}:({1:.1f},{2:.1f})".format(rotation, middle.X, middle.Y) \
                   + "}" + ",={0:.1f}".format(rotation)
    else:
        rotation = ''

    if (strokeColor != ''):
        strokeColor = ",draw=" + strokeColor
    else:
        strokeColor = ''

    if(style.find("shape=mxgraph.flowchart.annotation_2") != -1):
        fillColor = ''
    else:
        fillColor = getFillColour(splittedStyle)

    if(fillColor == ",fill=white"):
        fillColor = ''

    print(r"\draw[decorate, decoration={brace%s}%s%s%s] (%.1f,%.1f)--(%.1f,%.1f)%s node(%s)[pos=0.5,above]{};" % (
        amplitude, rotation, strokeColor, fillColor, startPoint.X, startPoint.Y, endPoint.X, endPoint.Y, currentText, objectID))
    return mapObjectsRemaining


# ------------------------------------------------------
def printNormalLines(mapObjectsRemaining, objectID, startPoint,
                     endPoint, width, height,
                     linestyle, lineWidth, strokeColour,
                     text, style, mxPoints):

    if (mapObjectsRemaining.get(objectID) != None):
        mapObjectsRemaining.pop(objectID)
    else:
        return mapObjectsRemaining

    #TODO this needs some more changes if there is a rotation if the lines don't need labels etc
    #just in case that one part is not always 10
    if(width < height):
        endPoint.X = startPoint.X
    elif(height < width):
        endPoint.Y = startPoint.Y

    if(strokeColour != ''):
        strokeColour = ',' + strokeColour

    startPoint = adjustPoints(startPoint, mxPoints, True)
    endPoint = adjustPoints(endPoint, mxPoints, False)
    rotation = getRotation(style.split(';'))
    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)

    if(rotation != None):
        rotation = r",rotate around={" + "{0:}:({1:.1f},{2:.1f})".format(rotation, middle.X, middle.Y) + "}" + ",={0:}".format(rotation)
    else:
        rotation = ''

#TODO not sure how to proceed here in order to align all the lines....
    print(r"\draw[%s%s%s%s] (%.0f,%.0f)--(%.0f,%.0f)%s node (%s) {};" %(
        linestyle[1:], lineWidth, strokeColour, rotation, startPoint.X, startPoint.Y, endPoint.X, endPoint.Y,  text, objectID))
    return mapObjectsRemaining


# ------------------------------------------------------
def printAllShapes(currentStyle, strokeColor, rounded,
                   mapObjectsRemaining, objectID, splittedStyle,
                   currentText, endPoint, startPoint,
                   filterText, align, rotation,
                   width, height, middle,
                   linestyle, pureText, innerSep,
                   curlyBracketsFactor, parent, tableFillColour,
                   lineWidth):

    if (strokeColor != '' and strokeColor != "white" and strokeColor != white):
        strokeColor = ',draw=' + strokeColor
    elif (strokeColor == "white" or strokeColor == white):
        strokeColor = ''
    else:
        strokeColor = ',draw'

    # rectangles ---------------------------------------------------------------------------------------------------
    if (((rounded != None and currentStyle.find("whiteSpace=wrap") != -1 and len(strokeColor) >= 5
         and currentStyle.find("shape=curlyBracket") == -1) or currentStyle.find("shape=mxgraph.basic.rect") != -1) or
        currentStyle.find("comic=0;") != -1 or (currentStyle.find("aspect=fixed;") != -1 and currentStyle.find("whiteSpace=wrap;") == 0)):
        mapObjectsRemaining = printRectangles(currentStyle, strokeColor, rounded,
                                              mapObjectsRemaining, objectID, splittedStyle,
                                              currentText, endPoint, startPoint,
                                              filterText, align, rotation,
                                              width, height, middle,
                                              linestyle, innerSep)

    # circles --------------------------------------------------------------------------------------------------
    elif ((currentStyle.find("Ellipse;") != -1 or currentStyle.find("ellipse;") != -1) and currentStyle.find("shape=cloud") == -1):
        mapObjectsRemaining = printCircles(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height, innerSep)

    # clouds -----------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=cloud;") != -1 ):
        mapObjectsRemaining = printClouds(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height, innerSep)

    # rhombus/diamond ----------------------------------------------------------------------------------------------
    elif (currentStyle.find("rhombus;") != -1):
        mapObjectsRemaining = printRhombus(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height, innerSep)

    # text outside ---------------------------------------------------------------------------------------------
    elif ((currentStyle.find("text;") != -1) or (currentStyle.find("edgeLabel;") != -1 and parent == '1') or
          (currentStyle.find("rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=none;")!= -1) or
          (currentStyle.find("fillColor=none;strokeColor=none;") != -1 and currentText != '')):
        mapObjectsRemaining = printText(mapObjectsRemaining, objectID, currentText,
                                        filterText, endPoint, parent,
                                        startPoint, align, currentStyle,
                                        rotation, innerSep, pureText)

    # merge shape ---------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=mxgraph.flowchart.merge_or_storage;") != -1):
        mapObjectsRemaining = printMerge(mapObjectsRemaining, objectID, middle, currentText)

    # square bracket ------------------------------------------------------------------------------------------
    # elif (currentStyle.find("shape=mxgraph.flowchart.annotation_2") != -1):
    #     print("square bracket")

    # curlyBrackets --------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=curlyBracket;") != -1 or currentStyle.find(
            "shape=mxgraph.flowchart.annotation_2;") != -1):
        mapObjectsRemaining = printCurlyBrackets(mapObjectsRemaining, objectID, splittedStyle,
                                                 currentText, startPoint, endPoint,
                                                 rotation, width, height,
                                                 currentStyle, curlyBracketsFactor)

    # images ---------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=image;") != -1):
        mapObjectsRemaining = printImages(mapObjectsRemaining, objectID, middle,
                                          currentText, currentStyle)

    # table rectangles ------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=partialRectangle;") != -1):
        mapObjectsRemaining = printPartialRectangles(currentStyle, strokeColor,
                                              mapObjectsRemaining, objectID,
                                              currentText, endPoint, startPoint,
                                              filterText, align, rotation,
                                              width, height, middle,
                                              linestyle, innerSep, tableFillColour)

    # table ------------------------------------------------------------------------------------------------------
    elif (currentStyle.find("table;") != -1):
        mapObjectsRemaining = printTable(currentStyle, strokeColor,
                                         mapObjectsRemaining, objectID,
                                         currentText, endPoint, startPoint,
                                         filterText, align, rotation,
                                         width, height, middle,
                                         linestyle, innerSep)

    # swimlane ---------------------------------------------------------------------------------------------------
    elif (currentStyle.find("swimlane;") != -1):
        mapObjectsRemaining = printSwimlanes(currentStyle, strokeColor,
                                              mapObjectsRemaining, objectID,
                                              currentText, endPoint, startPoint,
                                              filterText, align, rotation,
                                              width, height, middle,
                                              linestyle, innerSep)

    # crosses -----------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=cross;") != -1):
        mapObjectsRemaining = printCrosses(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height,
                                           innerSep, lineWidth)

    # fixed arrow -------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=mxgraph.arrows2.arrow;") != -1):
        mapObjectsRemaining = printArrow(mapObjectsRemaining, objectID, strokeColor,
                                           endPoint, startPoint, currentStyle)

    # cylinder ----------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=cylinder") != -1):
        mapObjectsRemaining = printCylinders(mapObjectsRemaining, objectID, strokeColor,
                                           splittedStyle, currentText, filterText,
                                           endPoint, startPoint, align,
                                           currentStyle, rotation, middle,
                                           linestyle, width, height,
                                           innerSep, lineWidth)


    # check marks -------------------------------------------------------------------------------------------------
    elif (currentStyle.find("shape=mxgraph.gcp2.check") != -1):
        mapObjectsRemaining = printCheckmarks(mapObjectsRemaining, objectID, endPoint, startPoint)


    # logic gates and transistors ---------------------------------------------------------------------------------
    elif (currentStyle.find("shape=mxgraph.electrical.logic_gates.logic_gate;") != -1 or
          currentStyle.find("shape=mxgraph.electrical.transistors") != -1 or
          currentStyle.find("shape=mxgraph.electrical.electro-mechanical") != -1 or
          currentStyle.find("shape=mxgraph.electrical.diodes") != -1):
        mapObjectsRemaining = printLogicShapes(mapObjectsRemaining, objectID, endPoint, startPoint, currentStyle)

    # some shape that isn't drawn and no text is contained --------------------------------------------------------
    elif((strokeColor == '' or strokeColor.find("white") != -1) and currentStyle.find("endArrow") == -1 and
         currentStyle.find("startArrow") == -1 and (getFillColour(splittedStyle) == '' or getFillColour(splittedStyle).find("white") != -1)):
        if(mapObjectsRemaining.get(objectID) != None):
            mapObjectsRemaining.pop(objectID)

    return mapObjectsRemaining


# ------------------------------------------------------
def printAllLinesArrowsAndObjects(mapObjectsRemaining, objectID, child,
                                  splittedStyle, target, currentStyle,
                                  arrowStyle, strokeColor, linestyle,
                                  startPoint, endPoint, width,
                                  height, lineWidth, currentText,
                                  source, targetPoint, sourcePoint,
                                  bracePositions, mapObjectCoordinates, mxPoints,
                                  previousChild=''):

    if(strokeColor == None):
        strokeColor = ''
    # print(objectID, arrowStyle)
    #TODO all those ifs here might need some rethinking -> not really well designed and very hard to change

    # curved arrows ------------------------------------------------------------------------------------------------
    if ((((currentStyle.find("edgeStyle=orthogonalEdgeStyle") == -1 or currentStyle.find("orthogonalLoop=1") != -1)
          and currentStyle.find("curved") != -1 and currentStyle.find("sketch=0") == -1) or
         (currentStyle.find("edgeStyle=elbowEdgeStyle") != -1 and currentStyle.find("orthogonalLoop=1") != -1 and
          currentStyle.find("endArrow=cross") == -1)) and arrowStyle != None and arrowStyle != '-'):
        mapObjectsRemaining = printCurvedArrows(mapObjectsRemaining, objectID, child,
                                                splittedStyle, target, lineWidth,
                                                arrowStyle, strokeColor, linestyle,
                                                currentText, source, targetPoint,
                                                sourcePoint, bracePositions, mapObjectCoordinates,
                                                mxPoints)

    # straight/cornered arrows  ------------------------------------------------------------------------------------
    elif (arrowStyle != None and arrowStyle != '-' and
          (currentStyle.find("edgeStyle=elbowEdgeStyle") == -1 or currentStyle.find("endArrow=cross") != -1) and
          ((currentStyle.find("endArrow") != -1) or currentStyle.find("edgeStyle=orthogonalEdgeStyle") != -1
           or currentStyle.find("orthogonalLoop=1;") != -1) and
          (currentStyle.find("curved=1") == -1 or currentStyle.find("sketch=0") != -1)):
        mapObjectsRemaining = printStraightArrows(mapObjectsRemaining, objectID, child, lineWidth,
                                                  splittedStyle, target, arrowStyle,
                                                  strokeColor, linestyle, currentText,
                                                  source, targetPoint, sourcePoint,
                                                  bracePositions, mapObjectCoordinates, previousChild,
                                                  mxPoints)

    # curved lines -------------------------------------------------------------------------------------------------
    elif ((currentStyle.find("curved=1") != -1 or currentStyle.find("rounded=1") != -1) and
          (arrowStyle == None or arrowStyle == '-')):
        mapObjectsRemaining = printCurvedLines(mapObjectsRemaining, objectID, child, lineWidth,
                                               splittedStyle, target, strokeColor, linestyle,
                                               currentText, source, targetPoint,
                                               sourcePoint, bracePositions, mapObjectCoordinates,
                                               mxPoints)

    # straight/cornered lines --------------------------------------------------------------------------------------
    elif ((arrowStyle == None or arrowStyle == '-')
          and (currentStyle.find("curved=1") == -1 or currentStyle.find("sketch=0") != -1)):
        mapObjectsRemaining = printStraightLines(mapObjectsRemaining, objectID, child, lineWidth,
                                                 splittedStyle, target, strokeColor, linestyle,
                                                 currentText, source, targetPoint, sourcePoint,
                                                 bracePositions, mapObjectCoordinates, previousChild,
                                                 mxPoints)

    # normal straight lines ----------------------------------------------------------------------------------------
    elif(currentStyle.find("line;") != -1):
        mapObjectsRemaining = printNormalLines(mapObjectsRemaining, objectID, startPoint,
                                               endPoint, width, height,
                                               linestyle, lineWidth, strokeColor,
                                               currentText, currentStyle, mxPoints)


    # edge labels need to be popped --------------------------------------------------------------------------------
    elif (currentStyle.find("edgeLabel;") != -1):
        if (mapObjectsRemaining.get(objectID) != None):
            mapObjectsRemaining.pop(objectID)

    return mapObjectsRemaining


# globals --------------------------------------------------------------------------------------------------------------

configToReadFrom = os.path.abspath("configurations.ini")
config = readConfig(configToReadFrom)
white = "FFFFFF"
drawioEnding = ".drawio"
PNGEnding = ".png"
XMLEnding = ".xml"
divisorfactor = Coordinates(0, 0)
mapObjects = {}
alreadyDefinedColours = []
defaultPointValue = -1.69420


# main part ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------
def main(argv):
    from helper import doEverything
    global config
    global configToReadFrom
    width = float
    height = float
    mapObjectsRemaining = {}
    startPoint = Coordinates(0, 0)
    endPoint = Coordinates(0, 0)
    middle = Coordinates
    currentText = string
    currentStyle = string
    parent = 0
    objectID = 1
    sourcePoint = Coordinates(0, 0)
    targetPoint = Coordinates(0, 0)
    source = string
    target = string
    parentIDList = []
    idFound = False
    offset = ''
    mytree = start(argv)
    labelDict = defineLabelDict(mytree)
    labelPointDict = defineLabelPointDict(mytree)
    bracesPosition = defineBracesPositions(mytree)
    mapObjectCoordinates = defineObjectCoordinates(mytree)
    curlyBracketsFactor = 2
    defaultTableString = "a"
    defaultRowString = "b"
    table = defaultTableString
    tableRow = defaultRowString
    tableFillColour = ''
    splittedStyle = ''
    previousSwimlaneParent = False
    scopeCount = 0

    # ----------------------------------------------------- shapes ---------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    for child in mytree.iter():
        try:
            for ID in parentIDList:
                if (child.attrib.get('parent') == ID):
                    idFound = True
                    break
            if (idFound == True):
                idFound = False
                continue

            # ------------------------------------------------------------------------------------------------------------------
            if (child.tag == "mxCell"):
                objectID = getID('id', child)
                currentStyle = child.attrib.get("style")
                parent = child.attrib.get('parent')
                if (len(child.attrib) != 1 and len(child.attrib) != 2):
                    mapObjectsRemaining[objectID] = currentStyle
                    mapObjects[objectID] = currentStyle
                if (currentStyle == None):
                    continue
                splittedStyle = currentStyle.split(';')

                # ---------------------------------------------------------
                if (currentStyle.find('group') != -1):
                    parentID = child.attrib.get('id')
                    parentIDList.append(parentID)
                    mapObjectsRemaining.pop(objectID)
                    shiftCoordinates = Coordinates(0, 0)
                    for element in list(child):
                        if (element.find("mxGeometry") != -1):
                            if (element.attrib.get("x") != None):
                                shiftCoordinates.X = float(element.attrib.get("x")) / divisorfactor.X
                            if (element.attrib.get("y") != None):
                                shiftCoordinates.Y = -float(element.attrib.get("y")) / divisorfactor.X
                            break
                    if (shiftCoordinates.X != 0 or shiftCoordinates.Y != 0):
                        print(r"\begin{scope}[shift={(%0.1f,%0.1f)}]" % (shiftCoordinates.X, shiftCoordinates.Y))
                    # print(mapObjectsRemaining)
                    mapObjectsRemaining = doEverything(parentID, mytree, mapObjectsRemaining,
                                                       parentIDList, bracesPosition, mapObjectCoordinates)
                    # print(mapObjectsRemaining)
                    if (shiftCoordinates.X != 0 or shiftCoordinates.Y != 0):
                        print(r"\end{scope}")
                currentText = getText(child)

                # ---------------------------------------------------------
                if (currentStyle.find('shape=table;') != -1 or currentStyle.find("shape=tableRow;") != -1):
                    scopeCount += 1
                    if(table == defaultTableString or (table != child.attrib.get('id') and currentStyle.find("shape=table;") != -1)):
                        if(table != defaultTableString):
                            scopeCount -= 2
                            print(r"\end{scope}")
                            print(r"\end{scope}")
                        table = child.attrib.get('id')
                        tableRow = defaultTableString
                        tableFillColour = getFillColour(splittedStyle)
                    if(tableRow == defaultRowString or (tableRow != child.attrib.get('id') and currentStyle.find("shape=tableRow;") != -1)):
                        if(tableRow != defaultRowString and tableRow != defaultTableString):
                            scopeCount -= 1
                            print(r"\end{scope}")
                        tableRow = child.attrib.get('id')

                    if(mapObjectsRemaining.get(objectID) != None and currentStyle.find("shape=tableRow;") != -1):
                        mapObjectsRemaining.pop(objectID)
                    shiftCoordinates = Coordinates(0, 0)

                    for element in list(child):
                        if (element.find("mxGeometry") != -1):
                            if (element.attrib.get("x") != None):
                                shiftCoordinates.X = float(element.attrib.get("x")) / divisorfactor.X
                            if (element.attrib.get("y") != None):
                                shiftCoordinates.Y = -float(element.attrib.get("y")) / divisorfactor.X
                            break

                    if (shiftCoordinates.X == 0 and shiftCoordinates.Y == 0 and currentStyle.find("portConstraint") != -1):
                        if (child.attrib.get("x") != None):
                            shiftCoordinates.X = float(child.attrib.get("x")) / divisorfactor.X
                        if (child.attrib.get("y") != None):
                            shiftCoordinates.Y = -float(child.attrib.get("y")) / divisorfactor.X

                    print(r"\begin{scope}[shift={(%0.1f,%0.1f)}]" % (shiftCoordinates.X, shiftCoordinates.Y))

                if (table != child.attrib.get('parent') and tableRow != child.attrib.get("parent")
                        and table != defaultTableString and table != child.attrib.get('id') and tableRow != child.attrib.get('id')):
                    scopeCount -= 2
                    print(r"\end{scope}")
                    print(r"\end{scope}")
                    table = defaultTableString
                    tableRow = defaultRowString

                # ---------------------------------------------------------
                if ((mapObjects.get(getIDNumber(child.attrib.get("parent"))) != None and
                     mapObjects.get(getIDNumber(child.attrib.get("parent"))).find("swimlane;") == -1 and
                     previousSwimlaneParent == True) or (
                     currentStyle.find("swimlane;") != -1 and previousSwimlaneParent == True)):
                    previousSwimlaneParent = False
                    print(r"\end{scope}")

                if(currentStyle.find("swimlane;") != -1):
                    previousSwimlaneParent = True


            # ------------------------------------------------------------------------------------------------------------------
            if (child.tag == "mxGeometry"):
                if (mapObjectsRemaining.get(objectID) == None):
                    continue
                linestyle = getLineStyle(splittedStyle)
                lineWidth = getLineWidth(splittedStyle)
                innerSep = getSpacing(splittedStyle)
                strokeColor = getStrokeColour(splittedStyle)
                rounded = findAndReturnInSplitted(splittedStyle, "rounded")
                align = getAlign(currentText, splittedStyle, currentStyle)
                rotation = getRotation(splittedStyle)
                if (child.attrib.get("x") != None):
                    startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
                else:
                    startPoint.X = 0
                if (child.attrib.get("y") != None):
                    startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
                else:
                    startPoint.Y = 0
                if (child.attrib.get("height") != None and child.attrib.get("width") != None):
                    endPoint.Y = startPoint.Y - float(child.attrib.get("height")) / divisorfactor.X
                    endPoint.X = startPoint.X + float(child.attrib.get("width")) / divisorfactor.X
                    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)
                    width = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
                    height = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
                    middle.X = float("{:.1f}".format(middle.X))
                    middle.Y = float("{:.1f}".format(middle.Y))

                filterText = currentText
                pureText = prepareText(currentText, currentStyle, height, True)
                currentText = prepareText(currentText, currentStyle, height)
                mapObjectsRemaining = printAllShapes(currentStyle, strokeColor, rounded,
                                                     mapObjectsRemaining, objectID, splittedStyle,
                                                     currentText, endPoint, startPoint,
                                                     filterText, align, rotation,
                                                     width, height, middle,
                                                     linestyle, pureText, innerSep,
                                                     curlyBracketsFactor, parent, tableFillColour,
                                                     lineWidth)
        except:
            print(r"% this object was not supported and could not be translated:" + objectID + " MIGHT cause errors")


    # ----------------------------------------------------- lines ----------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # print(scopeCount)
    while (scopeCount > 0):
        scopeCount -= 1
        print(r"\end{scope}")

    for i,child in enumerate(mytree.iter()):
    # for child in mytree.iter():
        try:
            for ID in parentIDList:
                if (child.attrib.get('parent') == ID):
                    idFound = True
                    break
            if (idFound == True):
                idFound = False
                continue
            if (child.tag == "mxCell"):
                objectID = getID("id", child)
                currentStyle = child.attrib.get(("style"))
                if (currentStyle == None):
                    continue
                source = getSource(child)
                target = getTarget(child)
                currentText = getText(child)

            if (previousSwimlaneParent == True):
                previousSwimlaneParent = False
                print(r"\end{scope}")

            if (child.tag == "mxGeometry"):
                if (mapObjectsRemaining.get(objectID) == None):
                    continue
                if(currentText != ''):
                    currentText = "node[pos=0.5]{" + currentText + "}"
                splittedStyle = currentStyle.split(';')
                for parentID in labelDict:
                    if (parentID == objectID):
                        if (labelDict.get(parentID) != None and labelPointDict.get(
                                getID('id', labelDict.get(parentID))) != None
                                and labelPointDict.get(getID('id', labelDict.get(parentID))).mxPoint.attrib.get(
                                    'as') == 'offset'):
                            offset = getoffset(labelPointDict[getIDNumber(labelDict[parentID].attrib.get('id'))].mxPoint,
                                               labelPointDict[
                                                   getIDNumber(labelDict[parentID].attrib.get('id'))].style,
                                               labelPointDict[getIDNumber(labelDict[parentID].attrib.get('id'))].relative)
                        if (mapObjectsRemaining.get(getID('id', labelDict[parentID])) != None):
                            mapObjectsRemaining.pop(getID('id', labelDict[parentID]))
                        currentText = prepareText(getText(labelDict[parentID]), currentStyle)
                        currentText = prepareLabelText(currentText, offset)
                        labelDict.pop(parentID)
                        break

                if (child.attrib.get("x") != None):
                    startPoint.X = float(child.attrib.get("x")) / divisorfactor.X
                else:
                    startPoint.X = 0

                if (child.attrib.get("y") != None):
                    startPoint.Y = -float(child.attrib.get("y")) / divisorfactor.X
                else:
                    startPoint.Y = 0

                if (child.attrib.get("height") != None and child.attrib.get("width") != None):
                    endPoint.Y = startPoint.Y - float(child.attrib.get("height")) / divisorfactor.X
                    endPoint.X = startPoint.X + float(child.attrib.get("width")) / divisorfactor.X
                    middle = getMiddle(startPoint.X, startPoint.Y, endPoint.X, endPoint.Y)
                    width = abs((endPoint.X - startPoint.X) / divisorfactor.Y)
                    height = abs((endPoint.Y - startPoint.Y) / divisorfactor.Y)
                    middle.X = float("{:.1f}".format(middle.X))
                    middle.Y = float("{:.1f}".format(middle.Y))

                linestyle = getLineStyle(splittedStyle)
                lineWidth = getLineWidth(splittedStyle)
                strokeColor = getStrokeColour(splittedStyle)
                arrowStyle = getArrowStyle(currentStyle)
                mxPoints = getChildrenMxPoint(i, mytree)
                mapObjectsRemaining = printAllLinesArrowsAndObjects(mapObjectsRemaining, objectID, child,
                                                                    splittedStyle, target, currentStyle,
                                                                    arrowStyle, strokeColor, linestyle,
                                                                    startPoint, endPoint, width,
                                                                    height, lineWidth, currentText,
                                                                    source, targetPoint, sourcePoint,
                                                                    bracesPosition, mapObjectCoordinates, mxPoints)
        except:
            print(r"% this object was not supported and could not be translated:" + objectID + " MIGHT cause errors")

    end(mytree, mapObjectsRemaining)


if __name__ == '__main__':
    main(sys.argv)
