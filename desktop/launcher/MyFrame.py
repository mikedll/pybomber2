# -*- coding: ANSI_X3.4-1968 -*-
# generated by wxGlade 0.3.4 on Mon Nov 22 09:12:53 2004

import wx

# begin wxGlade: dependencies
# end wxGlade

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.sName = wx.TextCtrl(self.notebook_1_pane_1, -1, "")
        self.sClients = wx.SpinCtrl(self.notebook_1_pane_1, -1, "1", min=1, max=9)
        self.sPort = wx.SpinCtrl(self.notebook_1_pane_1, -1, "35033", min=1024, max=65535)
        self.sMap = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[_("random"), _("default")], style=wx.CB_DROPDOWN)
        self.sLaunch = wx.Button(self.notebook_1_pane_1, -1, _("Launch Game"))
        self.clName = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.clServerAddress = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.clPort = wx.SpinCtrl(self.notebook_1_pane_2, -1, "35033", min=1024, max=65535)
        self.clLaunch = wx.Button(self.notebook_1_pane_2, -1, _("Launch Game"))
        self.spGamePads = wx.SpinCtrl(self.notebook_1_pane_3, -1, "0", min=0, max=10)
        self.spMap = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[_("random"), _("default")], style=wx.CB_DROPDOWN)
        self.name1 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name1"))
        self.color1 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name6 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name6"))
        self.color6 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name2 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name2"))
        self.color2 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name7 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name7"))
        self.color7 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name3 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name3"))
        self.color3 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name8 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name8"))
        self.color8 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name4 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name4"))
        self.color4 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name9 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name9"))
        self.color9 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name5 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name5"))
        self.color5 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.name10 = wx.TextCtrl(self.notebook_1_pane_3, -1, _("name10"))
        self.color10 = wx.ComboBox(self.notebook_1_pane_3, -1, choices=[], style=wx.CB_DROPDOWN)
        self.spLaunch = wx.Button(self.notebook_1_pane_3, -1, _("Launch Game"))
        self.hButton = wx.Button(self.notebook_1_pane_4, -1, _("launch help browser"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("frame_1"))
        self.SetSize((567, 687))
        self.sName.SetToolTipString(_("your name"))
        self.sClients.SetToolTipString(_("number of people that will be connecting"))
        self.sPort.SetToolTipString(_("a port number between 1024 and 65535"))
        self.sMap.SetToolTipString(_("choose a map, random will switch maps after each round"))
        self.sMap.SetSelection(0)
        self.clName.SetToolTipString(_("your name"))
        self.clServerAddress.SetToolTipString(_("IP address of game server"))
        self.clPort.SetToolTipString(_("A port number between 1024 and 65535"))
        self.notebook_1_pane_2.SetToolTipString(_("name of player"))
        self.spGamePads.SetToolTipString(_("number of gamepad players"))
        self.spMap.SetToolTipString(_("choose a map, random will switch maps after each round"))
        self.spMap.SetSelection(0)
        self.color1.SetSelection(-1)
        self.color6.SetSelection(-1)
        self.color2.SetSelection(-1)
        self.color7.SetSelection(-1)
        self.color3.SetSelection(-1)
        self.color8.SetSelection(-1)
        self.color4.SetSelection(-1)
        self.color9.SetSelection(-1)
        self.color5.SetSelection(-1)
        self.color10.SetSelection(-1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(5, 2, 0, 0)
        sizer_24 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player10")), wx.HORIZONTAL)
        sizer_20 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player5")), wx.HORIZONTAL)
        sizer_23 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player9")), wx.HORIZONTAL)
        sizer_19 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player4")), wx.HORIZONTAL)
        sizer_22 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player8")), wx.HORIZONTAL)
        sizer_18 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player3")), wx.HORIZONTAL)
        sizer_21 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player7")), wx.HORIZONTAL)
        sizer_17 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player2")), wx.HORIZONTAL)
        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("name6")), wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("player1")), wx.HORIZONTAL)
        sizer_16 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("map")), wx.HORIZONTAL)
        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, -1, _("Gamepads")), wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("server port")), wx.HORIZONTAL)
        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("server address")), wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, -1, _("name")), wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("map")), wx.HORIZONTAL)
        sizer_11 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("port number")), wx.HORIZONTAL)
        sizer_10 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("number of clients")), wx.HORIZONTAL)
        sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_1, -1, _("your name")), wx.HORIZONTAL)
        sizer_9.Add(self.sName, 0, 0, 0)
        sizer_2.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_10.Add(self.sClients, 0, 0, 0)
        sizer_2.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_11.Add(self.sPort, 0, 0, 0)
        sizer_2.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_15.Add(self.sMap, 0, 0, 0)
        sizer_2.Add(sizer_15, 0, wx.EXPAND, 0)
        sizer_2.Add(self.sLaunch, 0, 0, 0)
        self.notebook_1_pane_1.SetAutoLayout(1)
        self.notebook_1_pane_1.SetSizer(sizer_2)
        sizer_2.Fit(self.notebook_1_pane_1)
        sizer_2.SetSizeHints(self.notebook_1_pane_1)
        sizer_7.Add(self.clName, 0, 0, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_8.Add(self.clServerAddress, 0, 0, 0)
        sizer_3.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_14.Add(self.clPort, 0, 0, 0)
        sizer_3.Add(sizer_14, 0, wx.EXPAND, 0)
        sizer_3.Add(self.clLaunch, 0, 0, 0)
        self.notebook_1_pane_2.SetAutoLayout(1)
        self.notebook_1_pane_2.SetSizer(sizer_3)
        sizer_3.Fit(self.notebook_1_pane_2)
        sizer_3.SetSizeHints(self.notebook_1_pane_2)
        sizer_5.Add(self.spGamePads, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_16.Add(self.spMap, 0, 0, 0)
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
        sizer_4.Add(self.spLaunch, 0, 0, 0)
        self.notebook_1_pane_3.SetAutoLayout(1)
        self.notebook_1_pane_3.SetSizer(sizer_4)
        sizer_4.Fit(self.notebook_1_pane_3)
        sizer_4.SetSizeHints(self.notebook_1_pane_3)
        sizer_25.Add(self.hButton, 0, 0, 0)
        self.notebook_1_pane_4.SetAutoLayout(1)
        self.notebook_1_pane_4.SetSizer(sizer_25)
        sizer_25.Fit(self.notebook_1_pane_4)
        sizer_25.SetSizeHints(self.notebook_1_pane_4)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("server"))
        self.notebook_1.AddPage(self.notebook_1_pane_2, _("client"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _("local game"))
        self.notebook_1.AddPage(self.notebook_1_pane_4, _("help"))
        sizer_1.Add(wx.NotebookSizer(self.notebook_1), 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class MyFrame


