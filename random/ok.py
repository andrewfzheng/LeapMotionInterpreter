view = slicer.app.layoutManager().threeDWidget(0).threeDView()
# Set text
view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.UpperLeft,"Overview: \n-Point and move 1 finger to navigate slices \n-Point two fingers to lock slice position \n-While locked, gestures will perform specific functions \n-Camera Position \n-Swipe horizontally (X, Y) or vertically (Z), with both fingers to select axis \n-Using the index finger, make a circular motion (clockwise/counterclockwise) to rotate scene view about selected axis")
# Set color
view.cornerAnnotation().GetTextProperty().SetColor(0,0, 2)
# Update the view
view.forceRender()
# Set text
view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerLeft, "Selected:  Slice View")
# Set color
view.cornerAnnotation().GetTextProperty().SetColor(0, 0, 2)
# Update the view
view.forceRender()

# Add connector to text node
snode = slicer.vtkMRMLIGTLConnectorNode()
slicer.mrmlScene.AddNode(snode)
snode.SetName('Connector1')
snode.Start()
snode = slicer.mrmlScene.GetNodeByID('vtkMRMLTextNode1')
snodeText = str(snode)
leapmotionData = snodeText[snodeText.find('Text:'):snodeText.find("Encoding:")]
cnode = slicer.mrmlScene.GetNodeByID('vtkMRMLCameraNode2')
# Set volume node
volumeNode = getNode('MRHead')
displayNode = volumeNode.GetDisplayNode()
displayNode.AutoWindowLevelOff()

# RGY slice setup
lm = slicer.app.layoutManager()
green = lm.sliceWidget('Green')
greenLogic = green.sliceLogic()

lm = slicer.app.layoutManager()
yellow = lm.sliceWidget('Yellow')
yellowLogic = yellow.sliceLogic()

lm = slicer.app.layoutManager()
red = lm.sliceWidget('Red')
redLogic = red.sliceLogic()

# Set scene position
x = 598
y = 606
z = 740
amp = 0
# Just variables
func = "None"
function = 0
zoom = 30
viewer = 3
window = 128
level = 67
cnode.SetViewUp(0, 0, 1)
yellowPos = yellowLogic.GetSliceOffset()
redPos = redLogic.GetSliceOffset()
greenPos = greenLogic.GetSliceOffset()


def leapmotionDataInterpreter(snode, leapmotionData):
    global x
    global y
    global z
    global zoom
    global axis
    global func
    global viewer
    global window
    global level
    global function
    global yellowPos
    global greenPos
    global redPos
    global amp
    layoutManager = slicer.app.layoutManager()
    snode = slicer.mrmlScene.GetNodeByID('vtkMRMLTextNode1')
    snodeText = str(snode)
    leapmotionData = snodeText[snodeText.find('Text: ') + 1:snodeText.find("Encoding:")]
    positionText = (str(cnode)[str(cnode).find("Position: ") + 10:str(cnode).find("FocalPoint: ") - 2])
    x = float((positionText[0:positionText.find(", ")]))
    a = (positionText[positionText.find(", ") + 2:])
    y = float(a[0:a.find(", ")])
    z = float(a[a.find(", ") + 2:len(a)])
    if leapmotionData.find("Key Tap ID:") != -1 and leapmotionData.find("fingers: 3") != -1:
        function += 1
        print func
        if function == 4:
            function = 0
        if function == 0:
            func = "Slice View"
        if function == 1:
            func = "Scene View"
        if function == 2:
            func = "Viewer Layout + Grayscale"
        if function == 3:
            func = "Zoom, 3D View"
    if leapmotionData.find("Swipe ID") != -1 and function == 0:
        yellowPos = yellowLogic.GetSliceOffset()
        redPos = redLogic.GetSliceOffset()
        greenPos = greenLogic.GetSliceOffset()
        swipeDirection = leapmotionData[leapmotionData.find("direction:") + 11:leapmotionData.find("speed:") - 1]
        swipeDirectionX = float((swipeDirection[1:swipeDirection.find(", ")]))
        a = (swipeDirection[swipeDirection.find(", ") + 2:])
        swipeDirectionY = float(a[0:a.find(", ")])
        swipeDirectionZ = float(a[a.find(", ") + 2:len(a) - 1])
        if abs(swipeDirectionX) > abs(swipeDirectionY) and abs(swipeDirectionX) > abs(swipeDirectionZ):
            func = "Slice View, L-R"
        if abs(swipeDirectionZ) > abs(swipeDirectionX) and abs(swipeDirectionZ) > abs(swipeDirectionY):
            func = "Slice View, P-A"
        if abs(swipeDirectionY) > abs(swipeDirectionX) and abs(swipeDirectionY) > abs(swipeDirectionZ):
            func = "Slice View, I-S"
    if leapmotionData.find("Swipe ID") != -1 and function == 2:
        swipeDirection = leapmotionData[leapmotionData.find("direction:") + 11:leapmotionData.find("speed:") - 1]
        swipeDirectionX = float((swipeDirection[1:swipeDirection.find(", ")]))
        a = (swipeDirection[swipeDirection.find(", ") + 2:])
        swipeDirectionY = float(a[0:a.find(", ")])
        swipeDirectionZ = float(a[a.find(", ") + 2:len(a) - 1])
        if abs(swipeDirectionX) > abs(swipeDirectionY) and abs(swipeDirectionX) > abs(swipeDirectionZ):
            func = "Grayscale, Window"
        if abs(swipeDirectionZ) > abs(swipeDirectionX) and abs(swipeDirectionZ) > abs(swipeDirectionY):
            func = "Grayscale, Level"
        if abs(swipeDirectionY) > abs(swipeDirectionX) and abs(swipeDirectionY) > abs(swipeDirectionZ):
            func = "Viewer Layout"
    if leapmotionData.find("Swipe ID") != -1 and function == 1:
        swipeDirection = leapmotionData[leapmotionData.find("direction:") + 11:leapmotionData.find("speed:") - 1]
        swipeDirectionX = float((swipeDirection[1:swipeDirection.find(", ")]))
        a = (swipeDirection[swipeDirection.find(", ") + 2:])
        swipeDirectionY = float(a[0:a.find(", ")])
        swipeDirectionZ = float(a[a.find(", ") + 2:len(a) - 1])
        if abs(swipeDirectionX) > abs(swipeDirectionY) and abs(swipeDirectionX) > abs(swipeDirectionZ):
                func = "Scene View, L-R Rotate"
        if abs(swipeDirectionZ) > abs(swipeDirectionX) and abs(swipeDirectionZ) > abs(swipeDirectionY):
                func = "Scene View, P-A Rotate"
        if abs(swipeDirectionY) > abs(swipeDirectionX) and abs(swipeDirectionY) > abs(swipeDirectionZ):
                func = "Scene View, I-S Rotate"
    if function == 3:
            func = "Zoom, 3D view"
    if leapmotionData.find("Circle ID") != -1:
        amp = int(leapmotionData[len(leapmotionData) - 2])
        print amp
        if func == "Zoom, 3D view":
            if leapmotionData.find("counterclockwise") == -1 and zoom <= 100:
                zoom += 0.5 * amp
            else:
                if z >= 100:
                    zoom -= 0.5 * amp
        if func == "Scene View, L-R Rotate":
            if leapmotionData.find("counterclockwise") == -1 and x <= 598:
                x += 10 * amp
            else:
                if x >= -602:
                    x -= 10 * amp
            print "Position: (%f, %f, %f)" % (x, y, z)
        if func == "Scene View, P-A Rotate":
            if leapmotionData.find("counterclockwise") == -1 and y <= 606:
                y += 10 * amp
            else:
                if y >= -594:
                    y -= 10 * amp
            print "Position: (%f, %f, %f)" % (x, y, z)
        if func == "Scene View, I-S Rotate":
            if leapmotionData.find("counterclockwise") == -1 and z <= 740:
                z += 10 * amp
            else:
                if z >= -540:
                    z -= 10 * amp
            print "Position: (%f, %f, %f)" % (x, y, z)
        if func == "Grayscale, Window":
            if leapmotionData.find("counterclockwise") == -1:
                window += 5 * amp
            else:
                window -= 5 * amp
            print window
        if func == "Grayscale, Level":
            if leapmotionData.find("counterclockwise") == -1:
                level += 5 * amp
            else:
                level -= 5 * amp
            print level
        if func == "Viewer Layout":
            if leapmotionData.find("counterclockwise") == -1:
                if viewer <= 8.5:
                    viewer += 0.1 * amp
                else:
                    viewer = 3 * amp
        if func == "Slice View, L-R":
            if leapmotionData.find("counterclockwise") == -1:
                yellowPos += 5 * amp
            else:
                yellowPos -= 5 * amp
            print window
            yellowLogic.SetSliceOffset(yellowPos)
        if func == "Slice View, P-A":
            if leapmotionData.find("counterclockwise") == -1:
                greenPos += 5 * amp
            else:
                greenPos -= 5 * amp
            print level
        if func == "Slice View, I-S":
            if leapmotionData.find("counterclockwise") == -1:
                redPos += 5 * amp
            else:
                redPos -= 5 * amp
        greenLogic.SetSliceOffset(greenPos)
        redLogic.SetSliceOffset(redPos)
        cnode.SetPosition(x, y, z)
        cnode.SetViewAngle(zoom)
        layoutManager.setLayout(viewer)
        displayNode.SetWindow(window)
        displayNode.SetLevel(level)
    print func
    view = slicer.app.layoutManager().threeDWidget(0).threeDView()
    view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerLeft, "Selected: %s" % func)
    view.cornerAnnotation().GetTextProperty().SetColor(0, 0, 2)
    view.forceRender()


snode.AddObserver("ModifiedEvent", leapmotionDataInterpreter)



