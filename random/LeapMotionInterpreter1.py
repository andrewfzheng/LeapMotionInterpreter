# -*- coding: utf-8 -*-

# node selection
# logic issues
# interaction box visualizer
# options menu
from __main__ import vtk, qt, ctk, slicer

n = 1
class LeapMotionInterpreter:
    def __init__(self, parent):
        parent.title = "Leap Motion Interpreter"
        parent.categories = ["Utilities"]
        parent.contributors = ["Andrew Zheng"]
        parent.helpText = """
        The Leap Motion Intrepreter module enables gesture input from the Leap Motion Controller to be used in controlling Slicer."""
        parent.acknowledgementText = """

        """
        parent.icon = qt.QIcon('C:\Users\Andy Zheng\Pictures\Leap Motion\icon.png')
        self.parent = parent

class LeapMotionInterpreterWidget:
    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QBoxLayout)
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
            self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()
    def setup(self):

        #
        setupWindow = ctk.ctkCollapsibleButton()
        setupWindow.text = 'Setup'
        self.layout.addWidget(setupWindow)
        #
        self.setupLayout = qt.QFormLayout(setupWindow)
        #
        self.selectionWindow = qt.QFormLayout(setupWindow)
        self.labelx = qt.QLabel('vtkMRMLTextNode(n):')
        self.setupLayout.addWidget(self.labelx)
        self.nodeX = qt.QLineEdit()
        self.setupLayout.addWidget(self.nodeX)
        #
        self.labely = qt.QLabel('vtkMRMLScalarVolumeNode(n):')
        self.setupLayout.addWidget(self.labely)
        self.nodeY = qt.QLineEdit()
        self.setupLayout.addWidget(self.nodeY)
        #
        self.labelz = qt.QLabel('vtkMRMLCameraNode(n):')
        self.setupLayout.addWidget(self.labelz)
        self.nodeZ = qt.QLineEdit()
        self.setupLayout.addWidget(self.nodeZ)
        # Start client Server button
        self.serverStart = qt.QPushButton('Start Client Server')
        self.serverStart.clicked.connect(self.StartServer)
        self.setupLayout.addWidget(self.serverStart)
        # Connect nodes button
        self.nodeConnect = qt.QPushButton('Connect Nodes')
        self.nodeConnect.clicked.connect(self.NodeConnect)
        self.setupLayout.addWidget(self.nodeConnect)
        #
        selectionWindow = ctk.ctkCollapsibleButton()
        selectionWindow.text = 'Selection Visualizer'
        self.layout.addWidget(selectionWindow)
        #
        self.selectionLayout = qt.QFormLayout(selectionWindow)
        #
        self.label1 = qt.QLabel('Selected Function:')
        self.selectionLayout.addWidget(self.label1)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
        self.label1.setPixmap(image)
        #
        self.label = qt.QLabel("Spacer:")
        self.selectionLayout.addWidget(self.label)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_spacer.PNG")
        self.label.setPixmap(image)
        #
        self.label2 = qt.QLabel('Selected Category:')
        self.selectionLayout.addWidget(self.label2)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category1.PNG")
        self.label2.setPixmap(image)
        #
        self.label = qt.QLabel("Spacer:")
        self.selectionLayout.addWidget(self.label)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_spacer.PNG")
        self.label.setPixmap(image)
        #
        self.label3 = qt.QLabel('Selected Function:')
        self.selectionLayout.addWidget(self.label3)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview0.PNG")
        self.label3.setPixmap(image)

        slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, self.dataInterpreter)
    def StartServer(self):
        self.client = slicer.vtkMRMLIGTLConnectorNode()
        slicer.mrmlScene.AddNode(self.client)
        self.client.SetTypeClient('localhost', 18944)
        self.client.Start()
        self.status = slicer.vtkMRMLIGTLStatusNode()
        slicer.mrmlScene.AddNode(self.status)
    def NodeConnect(self):
        nodeXtext = self.nodeX.text
        nodeYtext = self.nodeY.text
        nodeZtext = self.nodeZ.text
        nodeXtext = str(nodeXtext)
        nodeYtext = str(nodeYtext)
        nodeZtext = str(nodeZtext)
        global snode
        global cnode
        snode = slicer.mrmlScene.GetNodeByID("vtkMRMLTextNode%s" % nodeXtext)
        svnode = slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode%s" % nodeYtext)
        cnode = slicer.mrmlScene.GetNodeByID("vtkMRMLCameraNode%s" % nodeZtext)
        displayNode = svnode.GetDisplayNode()
        displayNode.AutoWindowLevelOff()
        cnode.SetViewUp(0, 0, 1)
        camera = cnode.GetCamera()
        self.snodeText = "stfu"
        self.leapmotionData = "hi"
        cnodeText = str(cnode)
        self.positionText = (cnodeText[cnodeText.find("Position: ") + 10:cnodeText.find("FocalPoint: ") - 2])
        print self.snodeText
        print cnodeText
    def dataInterpreter(self, caller, event):
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
        global yellownode
        global greennode
        global rednode
        global svnode
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
            # snode = slicer.mrmlScene.GetNodeByID('vtkMRMLTextNode1')
            # snode.AddObserver("ModifiedEvent", self.dataInterpreter)
            # svnode = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
            # cnode = slicer.mrmlScene.GetNodeByID('vtkMRMLCameraNode2')
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
            yellowPos = yellowLogic.GetSliceOffset()
            redPos = redLogic.GetSliceOffset()
            greenPos = greenLogic.GetSliceOffset()
            yellownode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
            rednode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            greennode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
            n -= 1
        if self.snodeText.find("fingercount: 1") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.snodeText.find("fingercount: 2") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview1.PNG")
            self.label1.setPixmap(image)
        if self.snodeText.find("fingercount: 3") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview2.PNG")
            self.label1.setPixmap(image)
        if self.snodeText.find("fingercount: 4") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.snodeText.find("fingercount: 5") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("Key Tap ID:") != -1:
            if self.leapmotionData.find("fingers: 2") != -1:
                function += 1
                count = 0
                if function == 4:
                    function = 0
                if function == 0:
                    x = 0
                    y = 0
                    z = 0
                    func = "Slice View"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category1.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview0.png")
                    self.label3.setPixmap(image)
                if function == 1:
                    x = 0
                    y = 0
                    z = 0
                    func = "Scene View"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category2.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview0.png")
                    self.label3.setPixmap(image)
                    yellownode.SetWidgetVisible(0)
                    rednode.SetWidgetVisible(0)
                    greennode.SetWidgetVisible(0)
                if function == 2:
                    x = 0
                    y = 0
                    z = 0
                    func = "Grayscale"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category3.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale0.png")
                    self.label3.setPixmap(image)
                if function == 3:
                    x = 0
                    y = 0
                    z = 0
                    func = "Viewer Layout"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category4.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_viewerlayout.png")
                    self.label3.setPixmap(image)
            if self.leapmotionData.find("fingers: 3") != -1:
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
                func = "Slice View, Red"
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview1.png")
                self.label3.setPixmap(image)
                yellownode.SetWidgetVisible(0)
                rednode.SetWidgetVisible(1)
                greennode.SetWidgetVisible(0)
            if function == 0 and count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview2.png")
                self.label3.setPixmap(image)
                func = "Slice View, Yellow"
                yellownode.SetWidgetVisible(1)
                rednode.SetWidgetVisible(0)
                greennode.SetWidgetVisible(0)
            if function == 0 and count == 2:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview3.png")
                self.label3.setPixmap(image)
                func = "Slice View, Green"
                yellownode.SetWidgetVisible(0)
                rednode.SetWidgetVisible(0)
                greennode.SetWidgetVisible(1)
            if function == 1 and count == 0:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview1.png")
                self.label3.setPixmap(image)
                func = "Scene View, Yaw"
            if function == 1 and count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview2.png")
                self.label3.setPixmap(image)
                func = "Scene View, Roll"
            if function == 1 and count == 2:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview3.png")
                self.label3.setPixmap(image)
                func = "Scene View, Pitch"
            if function == 1 and count == 3:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview4.png")
                self.label3.setPixmap(image)
                func = "Scene View, Zoom"
            if function == 2 and count == 0:
                func = "Grayscale, Window"
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale1.png")
                self.label3.setPixmap(image)
            if function == 2 and count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale2.png")
                self.label3.setPixmap(image)
                func = "Grayscale, Level"
            if function == 3:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_viewerlayout.png")
                self.label3.setPixmap(image)
                func = "Viewer Layout"
            if func == "Viewer Layout":
                if count != 6:
                    viewer = count + 3
                    print viewer
                else:
                    count == 0
                    viewer = count + 3
        if self.leapmotionData.find("Circle ID") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview3.PNG")
            self.label1.setPixmap(image)
            amp = float(self.leapmotionData[self.leapmotionData.find("hand speed:") + 12:len(self.leapmotionData) - 1])
            if func == "Scene View, Zoom":
                x = 0
                y = 0
                z = 0
                if self.leapmotionData.find("counterclockwise") == -1 and zoom <= 100:
                    zoom += 0.5 * amp
                else:
                    if zoom >= 10:
                        zoom -= 0.5 * amp
            if func == "Scene View, Yaw":
                x = 0
                y = 0
                z = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    x = 1.5 * amp
                else:
                    x = -1.5 * amp
            if func == "Scene View, Roll":
                x = 0
                y = 0
                z = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    y = 1.5 * amp
                else:
                    y = -1.5 * amp
            if func == "Scene View, Pitch":
                x = 0
                y = 0
                z = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    z = 1.5 * amp
                else:
                    z = -1.5 * amp
            if func == "Grayscale, Window":
                if self.leapmotionData.find("counterclockwise") == -1:
                    window += 6 * amp
                else:
                    window -= 6 * amp
            if func == "Grayscale, Level":
                if self.leapmotionData.find("counterclockwise") == -1:
                    level += 4 * amp
                else:
                    level -= 4 * amp
            if func == "Slice View, Red":
                if self.leapmotionData.find("counterclockwise") == -1:
                    redPos += 0.5 * amp
                else:
                    redPos -= 0.5 * amp
            if func == "Slice View, Yellow":
                if self.leapmotionData.find("counterclockwise") == -1:
                    yellowPos += 0.5 * amp
                else:
                    yellowPos -= 0.5 * amp
            if func == "Slice View, Green":
                if self.leapmotionData.find("counterclockwise") == -1:
                    greenPos += 0.5 * amp
                else:
                    greenPos -= 0.5 * amp
            redLogic.SetSliceOffset(redPos)
            yellowLogic.SetSliceOffset(yellowPos)
            greenLogic.SetSliceOffset(greenPos)
            cnode.SetViewAngle(zoom)
            displayNode.SetWindow(window)
            displayNode.SetLevel(level)
            camera.Azimuth(x)
            camera.Roll(y)
            camera.Elevation(z)
            camera.OrthogonalizeViewUp()
        slicer.app.layoutManager().setLayout(viewer)
        view = slicer.app.layoutManager().threeDWidget(0).threeDView()
        view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
        view.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        view.forceRender()
        redview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
        redview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        redview.forceRender()
        greenview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
        greenview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        greenview.forceRender()
        yellowview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % func)
        yellowview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        yellowview.forceRender()
        # v = qt.QWebView()
        # v.setUrl(qt.QUrl('https://developer.leapmotion.com/documentation/python/devguide/Leap_Coordinate_Mapping.html'))
        # v.show()
        # v.url
        # QUrl (https://developer.leapmotion.com/documentation/python/devguide/Leap_Coordinate_Mapping.html, at: 0x000000000BCD0690)
        # QUrl(https://developer.leapmotion.com/documentation/python/devguide/Leap_Coordinate_Mapping.html, 0x7ae6300)
        #
        #
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