#!/usr/bin/env python
# -*- coding: ANSI_X3.4-1968 -*-
# generated by wxGlade 0.3.5.1 on Sat Nov 20 13:19:31 2004

import wx
from MyFrame import MyFrame

if __name__ == "__main__":
    import gettext
    gettext.install("FrinkiacBomber") # replace with the appropriate catalog name

    FrinkiacBomber = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    FrinkiacBomber.SetTopWindow(frame_1)
    frame_1.Show()
    FrinkiacBomber.MainLoop()