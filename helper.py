from parseXML import *

class Anchors:
    def __init__(self, entry, exit):
        self.entry = entry
        self.exit = exit

configToReadFrom = os.path.abspath("configurations.ini")
config = readConfig(configToReadFrom)

def doEverything(parent, tree, objectsRemaining, parents, bracesPosition, mapObjectCoordinates):
    global config
    global configToReadFrom
    width = float
    height = float
    mapObjectsRemaining = objectsRemaining
    startPoint = Coordinates(0, 0)
    endPoint = Coordinates(0, 0)
    middle = Coordinates
    currentText = string
    currentStyle = string
    objectID = 1
    sourcePoint = Coordinates(0, 0)
    targetPoint = Coordinates(0, 0)
    source = string
    target = string
    idFound = False
    offset = ''
    mytree = tree
    previousAnchors = Anchors('','')
    divisorfactor.X = calculateDivisorFactor(tree) * 2
    childParent = ''
    divisorfactor.Y = calculateDivisorFactor(tree)
    labelDict = defineLabelDict(mytree)
    labelPointDict = defineLabelPointDict(mytree)
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
        # this is for multiple nested scopes if we don't end all together at once
            for ID in parents:
                if (child.attrib.get('parent') == ID and ID != parent):
                    idFound = True
                    break
            if (idFound == True):
                idFound = False
                continue

            # ------------------------------------------------------------------------------------------------------------------
            if (child.tag == "mxCell"):
                if (child.attrib.get('parent') == parent):
                    childParent = child.attrib.get('parent')
                else:
                    continue
                objectID = getID('id', child)
                currentStyle = child.attrib.get("style")
                if (len(child.attrib) != 1 and len(child.attrib) != 2):
                    mapObjectsRemaining[objectID] = currentStyle
                    mapObjects[objectID] = currentStyle
                if (currentStyle == None):
                    continue
                splittedStyle = currentStyle.split(';')

                # ---------------------------------------------------------
                if (currentStyle.find('group') != -1):
                    parentID = child.attrib.get('id')
                    parents.append(parentID)
                    mapObjectsRemaining.pop(objectID)
                    shiftCoordinates = Coordinates(0, 0)
                    for element in list(child):
                        if (element.find("mxGeometry") != -1):
                            if(element.attrib.get("x") != None):
                                shiftCoordinates.X = float(element.attrib.get("x")) / divisorfactor.X
                            if (element.attrib.get("y") != None):
                                shiftCoordinates.Y = -float(element.attrib.get("y")) / divisorfactor.X
                            break
                    if(shiftCoordinates.X != 0 or shiftCoordinates.Y != 0):
                        print(r"\begin{scope}[shift={(%0.1f,%0.1f)}]" % (shiftCoordinates.X, shiftCoordinates.Y))
                    mapObjectsRemaining = doEverything(parentID, mytree, mapObjectsRemaining,
                                                       parents, bracesPosition, mapObjectCoordinates)
                    if(shiftCoordinates.X != 0 or shiftCoordinates.Y != 0):
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

            # ------------------------------------------------------------------------------------------------------------------
            if (childParent == parent and child.tag == "mxGeometry"):
                if (mapObjectsRemaining.get(objectID) == None):
                    continue
                childParent = ''
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
                currentText = prepareText(currentText, currentStyle, height)
                pureText = prepareText(currentText, currentStyle, height, True)

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

    while (scopeCount > 0):
        scopeCount -= 1
        print(r"\end{scope}")

    for i,child in enumerate(mytree.iter()):
        try:
            for ID in parents:
                if (child.attrib.get('parent') == ID and ID != parent):
                    idFound = True
                    break
            if (idFound == True):
                idFound = False
                continue
            if (child.tag == "mxCell"):
                if (child.attrib.get('parent') == parent):
                    childParent = child.attrib.get('parent')
                else:
                    continue
                objectID = getID("id", child)
                currentStyle = child.attrib.get(("style"))
                if (currentStyle == None):
                    continue
                source = getSource(child)
                target = getTarget(child)

            if (previousSwimlaneParent == True):
                previousSwimlaneParent = False
                print(r"\end{scope}")

            if (childParent == parent and child.tag == "mxGeometry"):
                if (mapObjectsRemaining.get(objectID) == None):
                    continue
                childParent = ''
                currentText = ''
                splittedStyle = currentStyle.split(';')
                for parentID in labelDict:
                    if (parentID == objectID):
                        if (labelDict.get(parentID) != None and labelPointDict.get(getID('id', labelDict.get(parentID))) != None
                                and labelPointDict.get(getID('id', labelDict.get(parentID))).mxPoint.get('as') == 'offset'):
                            offset = getoffset(labelPointDict[getIDNumber(labelDict[parentID].attrib.get('id'))].mxPoint,
                                               labelPointDict[getIDNumber(labelDict[parentID].attrib.get('id'))].style,
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
                if(findEntryAnchor(target, splittedStyle) != '' and findExitAnchor(source, splittedStyle) != ''):
                    previousAnchors = Anchors(findEntryAnchor(target, splittedStyle), findExitAnchor(source, splittedStyle))


                mapObjectsRemaining = printAllLinesArrowsAndObjects(mapObjectsRemaining, objectID, child,
                                                                    splittedStyle, target, currentStyle,
                                                                    arrowStyle, strokeColor, linestyle,
                                                                    startPoint, endPoint, width,
                                                                    height, lineWidth, currentText,
                                                                    source, targetPoint, sourcePoint,
                                                                    bracesPosition, mapObjectCoordinates, mxPoints,
                                                                    previousAnchors)
        except:
            print(r"% this object was not supported and could not be translated:" + objectID + " MIGHT cause errors")

    return mapObjectsRemaining
