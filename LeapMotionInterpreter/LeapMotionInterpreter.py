# -*- coding: utf-8 -*-
from __main__ import vtk, qt, ctk, slicer

#more functions
#call link from script

class LeapMotionInterpreter:
    def __init__(self, parent):
        parent.title = "Leap Motion Interpreter"
        parent.categories = ["Utilities"]
        parent.contributors = ["Andrew Zheng"]
        parent.helpText = """
        """
        parent.acknowledgementText = """

        """
        parent.icon = qt.QIcon('C:\Users\Andy Zheng\Pictures\Leap Motion\icon1.png')
        self.parent = parent


class LeapMotionInterpreterWidget:
    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
            self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()


    def setup(self):
        self.n = 1

        #
        # Select text, camera, volume nodes
        #
        setupWindow = ctk.ctkCollapsibleButton()
        setupWindow.text = 'Setup'
        self.layout.addWidget(setupWindow)
        self.setupLayout = qt.QFormLayout(setupWindow)

        # Text node selector
        self.textNodeSelector = slicer.qMRMLNodeComboBox()
        self.textNodeSelector.nodeTypes = (("vtkMRMLTextNode"), "")
        self.textNodeSelector.selectNodeUponCreation = True
        self.textNodeSelector.addEnabled = False
        self.textNodeSelector.removeEnabled = False
        self.textNodeSelector.noneEnabled = False
        self.textNodeSelector.showHidden = False
        self.textNodeSelector.showChildNodeTypes = True
        self.textNodeSelector.setMRMLScene(slicer.mrmlScene)
        self.setupLayout.addRow("Controller Data: ", self.textNodeSelector)

        # Camera node selector
        self.cameraNodeSelector = slicer.qMRMLNodeComboBox()
        self.cameraNodeSelector.nodeTypes = (("vtkMRMLCameraNode"), "")
        self.cameraNodeSelector.selectNodeUponCreation = True
        self.cameraNodeSelector.addEnabled = False
        self.cameraNodeSelector.removeEnabled = False
        self.cameraNodeSelector.noneEnabled = False
        self.cameraNodeSelector.showHidden = False
        self.cameraNodeSelector.showChildNodeTypes = True
        self.cameraNodeSelector.setMRMLScene(slicer.mrmlScene)
        self.setupLayout.addRow("Scene Camera: ", self.cameraNodeSelector)

        # Volume node selector
        self.volumeNodeSelector = slicer.qMRMLNodeComboBox()
        self.volumeNodeSelector.nodeTypes = (("vtkMRMLVolumeNode"), "")
        self.volumeNodeSelector.selectNodeUponCreation = True
        self.volumeNodeSelector.addEnabled = False
        self.volumeNodeSelector.removeEnabled = False
        self.volumeNodeSelector.noneEnabled = False
        self.volumeNodeSelector.showHidden = False
        self.volumeNodeSelector.showChildNodeTypes = True
        self.volumeNodeSelector.setMRMLScene(slicer.mrmlScene)
        self.setupLayout.addRow("Selected Volume: ", self.volumeNodeSelector)

        #
        # Connect/Disconnect Leap Motion Controller
        #
        connectWindow = ctk.ctkCollapsibleButton()
        connectWindow.text = "Leap Motion Controller Connector"
        self.layout.addWidget(connectWindow)
        self.connectLayout = qt.QFormLayout(connectWindow)

        # Connect controller
        self.controllerConnect = qt.QPushButton('Connect Leap Motion Controller')
        self.controllerConnect.clicked.connect(self.ControllerConnect)
        self.connectLayout.addWidget(self.controllerConnect)
        # disabled until volume selected
        self.controllerConnect.setEnabled(0)
        self.controllerConnect.setText('Connect Leap Motion Controller (Load a volume first!)')

        # Disconnect controlle
        self.controllerDisconnect = qt.QPushButton('Disconnect Leap Motion Controller')
        self.controllerDisconnect.clicked.connect(self.ControllerConnect)
        self.connectLayout.addWidget(self.controllerDisconnect)
        # disabled until volume selected
        self.controllerDisconnect.setEnabled(0)
        self.controllerDisconnect.setText('Dusconnect Leap Motion Controller (Load a volume first!)')

        #
        # Gesture Selection Visualizer
        #
        menuWindow = ctk.ctkCollapsibleButton()
        menuWindow.text = 'Gesture Selection Visualizer'
        self.layout.addWidget(menuWindow)
        self.menuLayout = qt.QFormLayout(menuWindow)
        # Display data confidence
        self.confidenceLabel = qt.QLabel("")
        self.menuLayout.addRow("Data Confidence:", self.confidenceLabel)

        # Show corner text
        self.cornerTextCheck = qt.QCheckBox()
        self.menuLayout.addRow("Show Corner Text:", self.cornerTextCheck)

        #Gesture Visualizer
        gestureVisualizerCollapsibleBox = ctk.ctkCollapsibleGroupBox()
        gestureVisualizerCollapsibleBox.setTitle("Gesture Visualizer")
        self.menuLayout.addRow(gestureVisualizerCollapsibleBox)
        gestureVisualizerLayout = qt.QFormLayout(gestureVisualizerCollapsibleBox)
        self.label1 = qt.QLabel()

        gestureVisualizerLayout.addWidget(self.label1)
        image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
        self.label1.setPixmap(image)

        #Selection Visualizer
        selectionVisualizerLayoutCollapsibleBox = ctk.ctkCollapsibleGroupBox()
        selectionVisualizerLayoutCollapsibleBox.setTitle("Selected Category:")
        self.menuLayout.addRow(selectionVisualizerLayoutCollapsibleBox)
        selectionVisualizerLayout = qt.QFormLayout(selectionVisualizerLayoutCollapsibleBox)
        self.label2 = qt.QLabel()
        selectionVisualizerLayout.addWidget(self.label2)
        # image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category1.PNG")
        # self.label2.setPixmap(image)
        self.label3 = qt.QLabel()
        selectionVisualizerLayout.addWidget(self.label3)
        # image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview1.PNG")
        # self.label3.setPixmap(image)

        # Add vertical spacer
        self.layout.addStretch(1)

        slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, self.dataInterpreter)

    def ControllerConnect(self):
        self.client = slicer.vtkMRMLIGTLConnectorNode()
        slicer.mrmlScene.AddNode(self.client)
        self.client.SetTypeClient('localhost', 18944)
        self.client.Start()
        self.status = slicer.vtkMRMLIGTLStatusNode()
        slicer.mrmlScene.AddNode(self.status)
    def ControllerDisconnect(self):
        self.client = slicer.vtkMRMLIGTLConnectorNode()
        slicer.mrmlScene.AddNode(self.client)
        self.client.SetTypeClient('localhost', 18944)
        self.client.Stop()
        self.status = slicer.vtkMRMLIGTLStatusNode()
        slicer.mrmlScene.AddNode(self.status)

    def dataInterpreter(self, caller, event):
        if self.volumeNodeSelector.currentNode() is not None:
            self.controllerConnect.setEnabled(1)
            self.controllerConnect.setText('Connect Leap Motion Controller')
            self.controllerDisconnect.setEnabled(1)
            self.controllerDisconnect.setText('Disconnect Leap Motion Controller')
        while self.n > 0:
            self.view = slicer.app.layoutManager().threeDWidget(0).threeDView()
            self.view.forceRender()
            self.redview = slicer.app.layoutManager().sliceWidget('Red').sliceView()
            self.greenview = slicer.app.layoutManager().sliceWidget('Green').sliceView()
            self.yellowview = slicer.app.layoutManager().sliceWidget('Yellow').sliceView()
            self.lm = slicer.app.layoutManager()
            self.green = self.lm.sliceWidget('Green')
            self.greenLogic = self.green.sliceLogic()
            self.lm = slicer.app.layoutManager()
            self.yellow = self.lm.sliceWidget('Yellow')
            self.yellowLogic = self.yellow.sliceLogic()
            self.lm = slicer.app.layoutManager()
            self.red = self.lm.sliceWidget('Red')
            self.redLogic = self.red.sliceLogic()
            self.textNode = self.textNodeSelector.currentNode()
            self.cameraNode = self.cameraNodeSelector.currentNode()
            self.volumeNode = self.volumeNodeSelector.currentNode()
            self.textNode.AddObserver("ModifiedEvent", self.dataInterpreter)
            self.camera = self.cameraNode.GetCamera()
            if self.volumeNode is not None:
                self.displayNode = self.volumeNode.GetDisplayNode()
                if self.displayNode is not None:
                    self.displayNode.AutoWindowLevelOff()
                    self.window = self.displayNode.GetWindow()
                    self.level = self.displayNode.GetLevel()
            self.x = 0
            self.y = 0
            self.z = 0
            self.amp = 0
            self.func = "None"
            self.function = 0
            self.zoom = self.cameraNode.GetViewAngle()
            self.viewer = 3

            self.count = 0
            self.yellowPos = self.yellowLogic.GetSliceOffset()
            self.redPos = self.redLogic.GetSliceOffset()
            self.greenPos = self.greenLogic.GetSliceOffset()
            self.n -= 1
        self.layoutManager = slicer.app.layoutManager()
        self.textNodeText = str(self.textNode)
        self.leapmotionData = self.textNodeText[
                              self.textNodeText.find('Text: ') + 1:self.textNodeText.find("Encoding:")]
        self.yellownode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
        self.rednode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
        self.greennode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
        if self.leapmotionData.find("confidence:") != -1:
            self.confidenceLabel.setText(str(self.leapmotionData[self.leapmotionData.find("confidence:") + 12:len(self.leapmotionData)-1]))
        if self.leapmotionData.find("fingercount: 1") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("fingercount: 2") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview1.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("fingercount: 3") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview2.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("fingercount: 4") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("fingercount: 5") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview0.PNG")
            self.label1.setPixmap(image)
        if self.leapmotionData.find("Key Tap ID:") != -1:
            if self.leapmotionData.find("fingers: 2") != -1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview11.PNG")
                self.label1.setPixmap(image)
                self.function += 1
                self.count = 0
                if self.function == 4:
                    self.function = 0
                if self.function == 0:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                    self.func = "Slice View"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category1.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview0.png")
                    self.label3.setPixmap(image)
                if self.function == 1:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                    self.func = "Scene View"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category2.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview0.png")
                    self.label3.setPixmap(image)
                    self.yellownode.SetWidgetVisible(0)
                    self.rednode.SetWidgetVisible(0)
                    self.greennode.SetWidgetVisible(0)
                if self.function == 2:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                    self.func = "Grayscale"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category3.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale0.png")
                    self.label3.setPixmap(image)
                if self.function == 3:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                    self.func = "Viewer Layout"
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_category4.PNG")
                    self.label2.setPixmap(image)
                    image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_viewerlayout.png")
                    self.label3.setPixmap(image)
            if self.leapmotionData.find("fingers: 3") != -1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview22.PNG")
                self.label1.setPixmap(image)
                self.count += 1
                if self.function == 0:
                    if self.count == 3:
                        self.count = 0
                elif self.function == 1:
                    if self.count == 4:
                        self.count = 0
                elif self.function == 2:
                    if self.count == 2:
                        self.count = 0
                elif self.function == 3:
                    self.layoutcount = self.layoutManager.layout + 1
                    if self.layoutcount == 9:
                        self.count = 3
            if self.function == 0 and self.count == 0:
                self.func = "Slice View, Red"
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview1.png")
                self.label3.setPixmap(image)
                self.yellownode.SetWidgetVisible(0)
                self.rednode.SetWidgetVisible(1)
                self.greennode.SetWidgetVisible(0)
            if self.function == 0 and self.count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview2.png")
                self.label3.setPixmap(image)
                self.func = "Slice View, Yellow"
                self.yellownode.SetWidgetVisible(1)
                self.rednode.SetWidgetVisible(0)
                self.greennode.SetWidgetVisible(0)
            if self.function == 0 and self.count == 2:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sliceview3.png")
                self.label3.setPixmap(image)
                self.func = "Slice View, Green"
                self.yellownode.SetWidgetVisible(0)
                self.rednode.SetWidgetVisible(0)
                self.greennode.SetWidgetVisible(1)
            if self.function == 1 and self.count == 0:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview1.png")
                self.label3.setPixmap(image)
                self.func = "Scene View, Yaw"
            if self.function == 1 and self.count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview2.png")
                self.label3.setPixmap(image)
                self.func = "Scene View, Roll"
            if self.function == 1 and self.count == 2:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview3.png")
                self.label3.setPixmap(image)
                self.func = "Scene View, Pitch"
            if self.function == 1 and self.count == 3:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_sceneview4.png")
                self.label3.setPixmap(image)
                self.func = "Scene View, Zoom"
            if self.function == 2 and self.count == 0:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale1.png")
                self.label3.setPixmap(image)
                self.func = "Grayscale, Window"
            if self.function == 2 and self.count == 1:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_grayscale2.png")
                self.label3.setPixmap(image)
                self.func = "Grayscale, Level"
            if self.function == 3:
                image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_viewerlayout.png")
                self.label3.setPixmap(image)
                self.func = "Viewer Layout"
            if self.func == "Viewer Layout":
                if self.count != 6:
                    self.viewer = self.count + 3
                else:
                    self.count = 0
                    self.viewer = self.count + 3
            slicer.app.layoutManager().setLayout(self.layoutcount)
        if self.leapmotionData.find("Circle ID") != -1:
            image = qt.QPixmap("C:\Users\Andy Zheng\Pictures\Leap Motion\UI_overview3.PNG")
            self.label1.setPixmap(image)
            self.amp = float(
                self.leapmotionData[
                self.leapmotionData.find("hand speed:") + 12:(self.leapmotionData.find(', confidence'))])
            if self.func == "Scene View, Zoom":
                self.x = 0
                self.y = 0
                self.z = 0
                if self.leapmotionData.find("counterclockwise") == -1 and self.zoom <= 100:
                    self.zoom += 0.3 * self.amp
                else:
                    if self.zoom >= 5:
                        self.zoom -= 0.3 * self.amp
            if self.func == "Scene View, Yaw":
                self.y = 0
                self.z = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.x = 1 * self.amp
                else:
                    self.x = -1 * self.amp
            if self.func == "Scene View, Roll":
                self.x = 0
                self.z = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.y = 1 * self.amp
                else:
                    self.y = -1 * self.amp
            if self.func == "Scene View, Pitch":
                self.x = 0
                self.y = 0
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.z = 1 * self.amp
                else:
                    self.z = -1 * self.amp
            if self.func == "Grayscale, Window":
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.window += 2 * self.amp
                else:
                    self.window -= 2 * self.amp
            if self.func == "Grayscale, Level":
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.level += 1 * self.amp
                else:
                    self.level -= 1 * self.amp
            if self.func == "Slice View, Red":
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.redPos += 0.5 * self.amp
                else:
                    self.redPos -= 0.5 *self.amp
            if self.func == "Slice View, Yellow":
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.yellowPos += 0.5 * self.amp
                else:
                    self.yellowPos -= 0.5 * self.amp
            if self.func == "Slice View, Green":
                if self.leapmotionData.find("counterclockwise") == -1:
                    self.greenPos += 0.5 * self.amp
                else:
                    self.greenPos -= 0.5 * self.amp
            self.redLogic.SetSliceOffset(self.redPos)
            self.yellowLogic.SetSliceOffset(self.yellowPos)
            self.greenLogic.SetSliceOffset(self.greenPos)
            self.cameraNode.SetViewAngle(self.zoom)
            self.displayNode.SetWindow(self.window)
            self.displayNode.SetLevel(self.level)
            self.camera.Azimuth(self.x)
            self.camera.Roll(self.y)
            self.camera.Elevation(self.z)
            self.camera.OrthogonalizeViewUp()
        if self.cornerTextCheck.checked:
            self.redview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % self.func)
            self.redview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
            self.greenview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % self.func)
            self.greenview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
            self.yellowview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight,
                                                       "Selected: %s \n" % self.func)
            self.yellowview.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
            self.view.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
            self.view = slicer.app.layoutManager().threeDWidget(0).threeDView()
            self.view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, "Selected: %s \n" % self.func)
            self.view.cornerAnnotation().GetTextProperty().SetColor(2, 2, 2)
        else:
            self.redview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, '')
            self.greenview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, '')
            self.yellowview.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight,
                                                   "Selected: %s \n" % self.func)
            self.view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.LowerRight, '')

        self.redview.forceRender()
        self.greenview.forceRender()
        self.yellowview.forceRender()
        self.view.forceRender()



        # v = qt.QWebView()
        # v.setUrl(
        # qt.QUrl('https://developer.leapmotion.com/documentation/python/devguide/Leap_Coordinate_Mapping.html'))
        # v.show()
        # v.url
        # QUrl (https://developer.leapmotion.com/documentation/python/devguide/Leap_Coordinate_Mapping.html,
        # at: 0x000000000BCD0690)
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