n = 1
def dataInterpreter(caller, event):
# replace with self
    global x
    global y
    global z
    global zoom
    global func
    global viewer
    global window
    global level
    global function
    global yellowPos
    global greenPos
    global redPos
    global amp
    global count
    global camera
    global n
    global displayNode
    global redLogic
    global greenLogic
    global yellowLogic
    global redview
    global greenview
    global yellowview
    global snode
    while n > 0:
        view = slicer.app.layoutManager().threeDWidget(0).threeDView()
        view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.UpperLeft, "LeapMotionInterpreter")
        view.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        view.forceRender()
        redview = slicer.app.layoutManager().sliceWidget('Red').sliceView()
        greenview = slicer.app.layoutManager().sliceWidget('Green').sliceView()
        yellowview = slicer.app.layoutManager().sliceWidget('Yellow').sliceView()
        lm = slicer.app.layoutManager()
        green = lm.sliceWidget('Green')
        greenLogic = green.sliceLogic()
        lm = slicer.app.layoutManager()
        yellow = lm.sliceWidget('Yellow')
        yellowLogic = yellow.sliceLogic()
        lm = slicer.app.layoutManager()
        red = lm.sliceWidget('Red')
        redLogic = red.sliceLogic()
        snode = slicer.mrmlScene.GetNodeByID('vtkMRMLTextNode1')
        snode.AddObserver("ModifiedEvent", dataInterpreter)
        volumeNode = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode2')
        displayNode = volumeNode.GetDisplayNode()
        displayNode.AutoWindowLevelOff()
        n = 1
        x = 0
        y = 0
        z = 0
        amp = 0
        func = "None"
        function = 0
        zoom = 30
        viewer = 3
        window = 128
        level = 67
        count = 0
        cnode = slicer.mrmlScene.GetNodeByID('vtkMRMLCameraNode2')
        cnode.SetViewUp(0, 0, 1)
        camera = cnode.GetCamera()
        yellowPos = yellowLogic.GetSliceOffset()
        redPos = redLogic.GetSliceOffset()
        greenPos = greenLogic.GetSliceOffset()
        n -= 1
    snodeText = str(snode)
    leapmotionData = snodeText[snodeText.find('Text: ') + 1:snodeText.find("Encoding:")]
    amp = float(leapmotionData[leapmotionData.find("hand speed:") + 12:len(leapmotionData) - 1])
    cnode = slicer.mrmlScene.GetNodeByID('vtkMRMLCameraNode2')
    cnodeText = str(cnode)
    positionText = (cnodeText[cnodeText.find("Position: ") + 10:cnodeText.find("FocalPoint: ") - 2])
    a = (positionText[positionText.find(", ") + 2:])
    zPos = float(a[a.find(", ") + 2:len(a)])
    yellownode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    rednode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    greennode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    if leapmotionData.find("Key Tap ID:") != -1:
        if leapmotionData.find("fingers: 2") != -1:
            function += 1
            count = 0
            if function == 4:
                function = 0
            if function == 0:
                x = 0
                y = 0
                z = 0
                func = "Slice View"
            if function == 1:
                x = 0
                y = 0
                z = 0
                func = "Scene View"
                yellownode.SetWidgetVisible(0)
                rednode.SetWidgetVisible(0)
                greennode.SetWidgetVisible(0)
            if function == 2:
                x = 0
                y = 0
                z = 0
                func = "Grayscale"
            if function == 3:
                x = 0
                y = 0
                z = 0
                func = "Viewer Layout"
        if leapmotionData.find("fingers: 3") != -1:
            count += 1
            if function == 0:
                if count == 3:
                    count = 0
            elif function == 1:
                if count == 4:
                    count = 0
            elif function == 2:
                if count == 2:
                    count = 0
            elif function == 3:
                if count == 6:
                    count = 0
        if function == 0 and count == 0:
            func = "Slice View, L-R"
            yellownode.SetWidgetVisible(1)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(0)
        if function == 0 and count == 1:
            func = "Slice View, P-A"
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(1)
        if function == 0 and count == 2:
            func = "Slice View, I-S"
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(1)
            greennode.SetWidgetVisible(0)
        if function == 1 and count == 0:
            func = "Scene View, Yaw"
        if function == 1 and count == 1:
            func = "Scene View, Roll"
        if function == 1 and count == 2:
            func = "Scene View, Pitch"
        if function == 1 and count == 3:
            func = "Scene View, Zoom"
        if function == 2 and count == 0:
            func = "Grayscale, Window"
        if function == 2 and count == 1:
            func = "Grayscale, Level"
        if function == 3:
            func = "Viewer Layout"
        if func == "Viewer Layout":
            if count != 6:
                viewer = count + 3
                print viewer
            else:
                count == 0
                viewer = count + 3
    if leapmotionData.find("Circle ID") != -1:
        amp = float(leapmotionData[leapmotionData.find("hand speed:") + 12:len(leapmotionData) - 1])
        if func == "Scene View, Zoom":
            x = 0
            y = 0
            z = 0
            if leapmotionData.find("counterclockwise") == -1 and zoom <= 100:
                zoom += 0.2 * amp
            else:
                if zoom >= 10:
                    zoom -= 0.2 * amp
        if func == "Scene View, Yaw":
            y = 0
            z = 0
            if leapmotionData.find("counterclockwise") == -1:
                x = 0.5 * amp
            else:
                x = -0.5 * amp
        if func == "Scene View, Roll":
            x = 0
            z = 0
            if leapmotionData.find("counterclockwise") == -1:
                y = 0.5 * amp
            else:
                y = -0.5 * amp
        if func == "Scene View, Pitch":
            x = 0
            y = 0
            if leapmotionData.find("counterclockwise") == -1:
                z = 0.5 * amp
            else:
                 z = -0.5 * amp
        if func == "Grayscale, Window":
            if leapmotionData.find("counterclockwise") == -1:
                window += 5 * amp
            else:
                window -= 5 * amp
        if func == "Grayscale, Level":
            if leapmotionData.find("counterclockwise") == -1:
                level += 5 * amp
            else:
                level -= 5 * amp
        if func == "Slice View, L-R":
            yellownode.SetWidgetVisible(1)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(0)
            if leapmotionData.find("counterclockwise") == -1:
                yellowPos += 1 * amp
            else:
                yellowPos -= 1 * amp
        if func == "Slice View, P-A":
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(1)
            if leapmotionData.find("counterclockwise") == -1:
                greenPos += 1 * amp
            else:
                greenPos -= 1 * amp
        if func == "Slice View, I-S":
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(1)
            greennode.SetWidgetVisible(0)
            if leapmotionData.find("counterclockwise") == -1:
                redPos += 1 * amp
            else:
                redPos -= 1 * amp
    greenLogic.SetSliceOffset(greenPos)
    redLogic.SetSliceOffset(redPos)
    yellowLogic.SetSliceOffset(yellowPos)
    cnode.SetViewAngle(zoom)
    slicer.app.layoutManager().setLayout(viewer)
    displayNode.SetWindow(window)
    displayNode.SetLevel(level)
    camera.Azimuth(x)
    camera.Roll(y)
    camera.Elevation(z)
    view = slicer.app.layoutManager().threeDWidget(0).threeDView()
    view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
    view.cornerAnnotation().GetTextProperty().SetColor(2,2,2)
    view.forceRender()
    redview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
    redview.cornerAnnotation().GetTextProperty().SetColor(2,2,2)
    redview.forceRender()
    greenview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
    greenview.cornerAnnotation().GetTextProperty().SetColor(2,2,2)
    greenview.forceRender()
    yellowview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
    yellowview.cornerAnnotation().GetTextProperty().SetColor(2,2,2)
    yellowview.forceRender()
    # viewnode = slicer.mrmlScene.GetNodeByID("vtkMRMLViewNode1")
    # viewnode.SetBackgroundColor(0, 0, 0)
    # color = str(viewnode.GetBackgroundColor())
    # c0 = float((color[0:color.find(", ")]))
    # a = (color[color.find(", ") + 2:])
    # c1 = float(a[0:a.find(", ")])
    # c2 = float(a[a.find(", ") + 2:len(a)])
    # color2 = str(viewnode.GetBackgroundColor2())
    # c3 = float((color2[0:color2.find(", ")]))
    # a1 = (color2[color2.find(", ") + 2:])
    # c4 = float(a1[0:a1.find(", ")])
    # c5 = float(a1[a1.find(", ") + 2:len(a1)])

slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, dataInterpreter)



