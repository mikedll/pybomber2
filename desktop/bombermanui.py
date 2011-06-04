# -*- coding: ANSI_X3.4-1968 -*-
# generated by wxGlade 0.3.4 on Sun Nov 21 19:27:46 2004

# Keep stuff out of the begin wxGlade comments, and don't modify them
# even if they're in violation of our standards.  If I need to do further
# work in wxGlade there will be problems

import wx
import pygame
import os
from config import *
pygame.joystick.init()
# begin wxGlade: dependencies
# end wxGlade

class BombermanFrame(wx.Frame):
    def __init__(self, options, *args, **kwds):
        sortedMaplist = list(MAPLIST)
        sortedMaplist.sort()
        menuMaps = ["Random"] + sortedMaplist
        colorList = ["black", "light red", "red", "light green",
                     "green", "light blue", "blue", "dark yellow",
                     "teal", "purple", "cyan", "pink", "yellow",
                     "white"]
        namesList = None

        # Attempt to open localfilenames
        try:
          f = open(LOCALNAMESFILE, 'r')
          namesList = f.readlines()
          for name in range(0, len(namesList)):
            namesList[name] = namesList[name][0:-1]
        except:
            namesList = ['name1', 'name2', 'name3', 'name4', 'name5',
                         'name6', 'name7', 'name8', 'name9', 'name10']
        # Finally, 
        self.options = options
        self.exitOnClose = True

        # begin wxGlade
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)

        # Local Game setup pane
        self.lGamePads = wx.SpinCtrl(self.notebook_1_pane_1, -1, "2", min=2,
                                     max=pygame.joystick.get_count()+3)
        self.lMap = wx.ComboBox(self.notebook_1_pane_1, -1,
                                choices=menuMaps, style=wx.CB_DROPDOWN)
        self.name1 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[0])
        self.color1 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name2 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[1])
        self.color2 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name3 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[2])
        self.color3 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name4 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[3])
        self.color4 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name5 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[4])
        self.color5 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name6 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[5])
        self.color6 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name7 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[6])
        self.color7 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name8 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[7])
        self.color8 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name9 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[8])
        self.color9 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                  choices=colorList, style=wx.CB_DROPDOWN)
        self.name10 = wx.TextCtrl(self.notebook_1_pane_1, -1, namesList[9])
        self.color10 = wx.ComboBox(self.notebook_1_pane_1, -1,
                                   choices=colorList, style=wx.CB_DROPDOWN)
        self.lLaunch = wx.Button(self.notebook_1_pane_1, -1, _("Launch Game"))

        # Server Setup pane
        self.sName = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.sClients = wx.SpinCtrl(self.notebook_1_pane_2,
                                    -1, "1", min=1, max=9)
        self.sPort = wx.SpinCtrl(self.notebook_1_pane_2, -1,
                                 "35033", min=1024, max=65535)
        self.sMap = wx.ComboBox(self.notebook_1_pane_2, -1,
                                choices=menuMaps, style=wx.CB_DROPDOWN)
        self.sLaunch = wx.Button(self.notebook_1_pane_2, -1, _("Launch Game"))

        # Client Setup pane
        self.clName = wx.TextCtrl(self.notebook_1_pane_3, -1, "")
        self.clServerAddress = wx.TextCtrl(self.notebook_1_pane_3, -1, "")
        self.clPort = wx.SpinCtrl(self.notebook_1_pane_3, -1,
                                  "35033", min=1024, max=65535)
        self.clLaunch = wx.Button(self.notebook_1_pane_3, -1, _("Launch Game"))

        # Help pane
        self.hButton = wx.Button(self.notebook_1_pane_4, -1, _("Launch help browser"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        wx.EVT_BUTTON(self, self.lLaunch.GetId(), self.pushLocal)
        wx.EVT_BUTTON(self, self.sLaunch.GetId(), self.pushServer)
        wx.EVT_BUTTON(self, self.clLaunch.GetId(), self.pushClient)
        wx.EVT_BUTTON(self, self.hButton.GetId(), self.pushHelp)
        wx.EVT_CLOSE(self, self.OnCloseWindow)

    def __set_properties(self):
        # begin wxGlade
        self.SetTitle(_("Pybomber Setup"))
        self.SetSize(RESOLUTION)
        self.sName.SetToolTipString(_("Your name"))
        self.sClients.SetToolTipString(_("Number of people that will be connecting"))
        self.sPort.SetToolTipString(_("A port number between 1024 and 65535"))
        self.sMap.SetToolTipString(_("Choose a map, random will switch maps after each round"))
        self.sMap.SetSelection(0)
        self.clName.SetToolTipString(_("Your name"))
        self.clServerAddress.SetToolTipString(_("IP address of game server"))
        self.clPort.SetToolTipString(_("A port number between 1024 and 65535"))
        self.notebook_1_pane_3.SetToolTipString(_("Name of player"))
        self.lGamePads.SetToolTipString(_("Total number of players"))
        self.lMap.SetToolTipString(_("Choose a map, random will switch maps after each round"))
        self.lMap.SetSelection(0)
        self.color1.SetSelection(1)
        self.color6.SetSelection(6)
        self.color2.SetSelection(2)
        self.color7.SetSelection(7)
        self.color3.SetSelection(3)
        self.color8.SetSelection(8)
        self.color4.SetSelection(4)
        self.color9.SetSelection(9)
        self.color5.SetSelection(5)
        self.color10.SetSelection(10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(5, 2, 0, 0)
        sizer_24 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 10")), wx.HORIZONTAL)
        sizer_20 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 5")), wx.HORIZONTAL)
        sizer_23 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 9")), wx.HORIZONTAL)
        sizer_19 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 4")), wx.HORIZONTAL)
        sizer_22 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 8")), wx.HORIZONTAL)
        sizer_18 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 3")), wx.HORIZONTAL)
        sizer_21 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 7")), wx.HORIZONTAL)
        sizer_17 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 2")), wx.HORIZONTAL)
        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 6")), wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Player 1")), wx.HORIZONTAL)
        sizer_16 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Map")), wx.HORIZONTAL)
        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("Players")), wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("Server port")), wx.HORIZONTAL)
        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("Server address")), wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("Name")), wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("Map")), wx.HORIZONTAL)
        sizer_11 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("Port number")), wx.HORIZONTAL)
        sizer_10 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("Number of clients")), wx.HORIZONTAL)
        sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("Your name")), wx.HORIZONTAL)

        # Local Game Setup pane
        sizer_5.Add(self.lGamePads, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_16.Add(self.lMap, 0, 0, 0)
        sizer_4.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_12.Add(self.name1, 0, 0, 0)
        sizer_12.Add(self.color1, 0, 0, 0)
        grid_sizer_1.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_13.Add(self.name6, 0, 0, 0)
        sizer_13.Add(self.color6, 0, 0, 0)
        grid_sizer_1.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_17.Add(self.name2, 0, 0, 0)
        sizer_17.Add(self.color2, 0, 0, 0)
        grid_sizer_1.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_21.Add(self.name7, 0, 0, 0)
        sizer_21.Add(self.color7, 0, 0, 0)
        grid_sizer_1.Add(sizer_21, 1, wx.EXPAND, 0)
        sizer_18.Add(self.name3, 0, 0, 0)
        sizer_18.Add(self.color3, 0, 0, 0)
        grid_sizer_1.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_22.Add(self.name8, 0, 0, 0)
        sizer_22.Add(self.color8, 0, 0, 0)
        grid_sizer_1.Add(sizer_22, 1, wx.EXPAND, 0)
        sizer_19.Add(self.name4, 0, 0, 0)
        sizer_19.Add(self.color4, 0, 0, 0)
        grid_sizer_1.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_23.Add(self.name9, 0, 0, 0)
        sizer_23.Add(self.color9, 0, 0, 0)
        grid_sizer_1.Add(sizer_23, 1, wx.EXPAND, 0)
        sizer_20.Add(self.name5, 0, 0, 0)
        sizer_20.Add(self.color5, 0, 0, 0)
        grid_sizer_1.Add(sizer_20, 1, wx.EXPAND, 0)
        sizer_24.Add(self.name10, 0, 0, 0)
        sizer_24.Add(self.color10, 0, 0, 0)
        grid_sizer_1.Add(sizer_24, 1, wx.EXPAND, 0)
        sizer_4.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_4.Add(self.lLaunch, 0, 0, 0)
        self.notebook_1_pane_1.SetAutoLayout(1)
        self.notebook_1_pane_1.SetSizer(sizer_4)
        sizer_4.Fit(self.notebook_1_pane_1)
        sizer_4.SetSizeHints(self.notebook_1_pane_1)

        # Server Setup pane
        sizer_9.Add(self.sName, 0, 0, 0)
        sizer_2.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_10.Add(self.sClients, 0, 0, 0)
        sizer_2.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_11.Add(self.sPort, 0, 0, 0)
        sizer_2.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_15.Add(self.sMap, 0, 0, 0)
        sizer_2.Add(sizer_15, 0, wx.EXPAND, 0)
        sizer_2.Add(self.sLaunch, 0, 0, 0)
        self.notebook_1_pane_2.SetAutoLayout(1)
        self.notebook_1_pane_2.SetSizer(sizer_2)
        sizer_2.Fit(self.notebook_1_pane_2)
        sizer_2.SetSizeHints(self.notebook_1_pane_2)

        # Client Setup pane
        sizer_7.Add(self.clName, 0, 0, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_8.Add(self.clServerAddress, 0, 0, 0)
        sizer_3.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_14.Add(self.clPort, 0, 0, 0)
        sizer_3.Add(sizer_14, 0, wx.EXPAND, 0)
        sizer_3.Add(self.clLaunch, 0, 0, 0)
        self.notebook_1_pane_3.SetAutoLayout(1)
        self.notebook_1_pane_3.SetSizer(sizer_3)
        sizer_3.Fit(self.notebook_1_pane_3)
        sizer_3.SetSizeHints(self.notebook_1_pane_3)

        # Help pane
        sizer_25.Add(self.hButton, 0, 0, 0)
        self.notebook_1_pane_4.SetAutoLayout(1)
        self.notebook_1_pane_4.SetSizer(sizer_25)
        sizer_25.Fit(self.notebook_1_pane_4)
        sizer_25.SetSizeHints(self.notebook_1_pane_4)

        self.notebook_1.AddPage(self.notebook_1_pane_1, _("Local game"))
        self.notebook_1.AddPage(self.notebook_1_pane_2, _("Server"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _("Client"))
        self.notebook_1.AddPage(self.notebook_1_pane_4, _("Help"))
        sizer_1.Add(wx.NotebookSizer(self.notebook_1), 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def pushLocal(self, event):
        self.exitOnClose = False
        self.options.numPlayers = str(self.lGamePads.GetValue())
        self.options.mapFile = str(self.lMap.GetValue())
        if self.options.mapFile == "Random":
            self.options.random = True
        try:
            f = open(LOCALNAMESFILE, 'w')
            f.write(self.name1.GetValue() + "\n")
            f.write(self.name2.GetValue() + "\n")
            f.write(self.name3.GetValue() + "\n")
            f.write(self.name4.GetValue() + "\n")
            f.write(self.name5.GetValue() + "\n")
            f.write(self.name6.GetValue() + "\n")
            f.write(self.name7.GetValue() + "\n")
            f.write(self.name8.GetValue() + "\n")
            f.write(self.name9.GetValue() + "\n")
            f.write(self.name10.GetValue() + "\n")
            f.close()
        except:
            pass
        self.Close(True)

    def pushServer(self, event):
        self.exitOnClose = False

        # Is this necessary?
        # All we need to do is write our name to the first spot
        # in the file.
        #######################################
        f = open(LOCALNAMESFILE, 'r')
        names = f.readlines()
        f.close()
        names[0] = self.sName.GetValue() + "\n"
        try:
            f = open(LOCALNAMESFILE, 'w')
            for name in names:
                f.write(name)
            f.close()
        except:
            pass
        #######################################

        self.options.mapFile = str(self.sMap.GetValue())
        if self.options.mapFile == "Random":
            self.options.random = True
        self.options.serverMode = str(self.sClients.GetValue())
        self.options.port = str(self.sPort.GetValue())
        self.Close(True)

    def pushClient(self, event):
        self.exitOnClose = False
        f = open(LOCALNAMESFILE, 'r')
        names = f.readlines()
        f.close()
        names[0] = self.clName.GetValue() + "\n"
        try:
            f = open(LOCALNAMESFILE, 'w')
            for name in names:
                f.write(name)
            f.close()
        except:
            pass
        self.options.clientMode = str(self.clServerAddress.GetValue())
        self.options.port = str(self.clPort.GetValue())
        self.Close(True)

    def pushHelp(self, event):
        if (os.name=="posix"):
            os.spawnlp(os.P_WAIT, 'mozilla', 'mozilla', HELPURL)

    def OnCloseWindow(self, event):
        self.Destroy()
        if(self.exitOnClose):
            raise SystemExit
# end of class BombermanFrame