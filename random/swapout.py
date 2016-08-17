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
        func = "Grayscale, Window"
    if function == 1 and count == 1:
        func = "Grayscale, Level"
    if function == 1 and count == 2:
        func = "Viewer Layout"
    if function == 2 and count == 1:
        func = "Scene View, L-R Rotate"
    if function = 2 and count == 1:
        func = "Scene View, P-A Rotate"
    if function == 2 and count == 2:
        func = "Scene View, I-S Rotate"

##############################################################

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
            yellownode.SetWidgetVisible(1)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(0)
        if abs(swipeDirectionZ) > abs(swipeDirectionX) and abs(swipeDirectionZ) > abs(swipeDirectionY):
            func = "Slice View, P-A"
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(0)
            greennode.SetWidgetVisible(1)
        if abs(swipeDirectionY) > abs(swipeDirectionX) and abs(swipeDirectionY) > abs(swipeDirectionZ):
            func = "Slice View, I-S"
            yellownode.SetWidgetVisible(0)
            rednode.SetWidgetVisible(1)
            greennode.SetWidgetVisible(0)
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
