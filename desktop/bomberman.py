#!/usr/bin/python2.3 -tt
__author__ = """Adam Fomotor, Brandon Sterne, Bryan Cabalo, Mike Rivera, 
                Rima Fata, Shashwati Kasetty, Shawn Lesniak"""
__copyright__ = "Copyright (c) 2004"
__license__ = "GNU GPL v2.0"
__version__ = "PRE1.0"

from optparse import OptionParser
from config import *
from startgame import *
from game import *
from gamesetup import *
import pygame
from widget import *
from splashes import *
from log import *

def getParser():
    # Option parsing
    usage = "usage: %prog [options]"

    parser = OptionParser(usage, version="%prog " + __version__)
    # General opts
    parser.add_option("-o", dest="colors", action="store_true", default=False,
                     help="Choose bomberman colors and player names.")
    parser.add_option("-p", dest="numPlayers", metavar="NUMPLAYERS",
                    default='0', help="Choose the number of players.")
    # Map args
    parser.add_option("-m", dest="mapFile", metavar="FILE", default=DEFAULTMAP,
                     help="Use a custom map.")
    parser.add_option("-r", dest="random", action="store_true", default=False,
                     help="random map, overrides -m")
    # Networking args
    parser.add_option("-s", dest="serverMode", metavar="CLIENTS", default=False,
                     help="Host a network game for an additional CLIENTS number of clients.")
    parser.add_option("-c", dest="clientMode", metavar="SERVERIP", default=False,
                     help="Connect to a server; you must supply a SERVERIP.")
    parser.add_option("-t", dest="port", metavar="PORT", default=FREEPORT,
                     help="For network gaming, use PORT.")
    parser.add_option("--ip", dest="ip", metavar="HOSTIP", default="0.0.0.0",
                     help="Specify an arbitrary ip for server mode. Useful"+\
                           "for machines that don't know their own IP.")
    # testing args
    parser.add_option("--replay", dest="replay", metavar="FILENAME", default='',
                     help="Use scripted testing players using input from the last recorded game.")
    parser.add_option("--record", dest="record", metavar="FILENAME", default='',
                     help="Create replay file(s) for this game.")
    parser.add_option("--logfile", dest="logfile", action="store_true", default=False,
                     help="Create a logfile for debugging purposes.")

    return parser

def startWithOps(options):
    ########################################
    initPygame() # This is a global function
                 # from widget
    ########################################

    # Handle incompatible options
    if options.random and options.clientMode:
        print "Only the server can set random map."
        raise SystemExit

    if int(options.serverMode) > 9:
        print "The server can accept a maximum of 9 players."
        raise SystemExit

    if options.random:
        options.mapFile = "random"

    if options.logfile:
        initDebugLog()

    setupClass = None
    if options.clientMode:
        setupClass = ClientSetup
    elif options.serverMode:
        setupClass = ServerSetup
    elif options.replay:
        setupClass = ScriptedSetup
    else:
        setupClass = LocalSetup

    # Alert player what we are doing
    group, textBar = getLoadScreen()
    initLoadScreen(group, textBar)

    setup = setupClass(options)
    setup.init()

    updateLoadScreen("Starting game...")
    game = Game(setup.getGameMap(), setup.getPlayerList(),\
                setup.getRandomSeed())

    if(options.record):
        game.insertVHS(str(setup.getRandomSeed()), options.record)

    game.start()

def commandLine():
    parser = getParser()
    (options, args) = parser.parse_args()
    options.colors = False
    startWithOps(options)

def graphicalUI():
    import wx
    from bombermanui import BombermanFrame
    parser = getParser()
    (options) = parser.get_default_values()

    import gettext
    # Replace with the appropriate catalog name
    gettext.install("Pybomber")

    BombermanUI = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = BombermanFrame(options, None, -1, "")
    BombermanUI.SetTopWindow(frame_1)
    frame_1.Show()
    BombermanUI.MainLoop()

    # Override default values here
    options.colors = False
    startWithOps(options)

def main():
    if len(sys.argv) > 1:
      commandLine()
    else:
      graphicalUI()

if __name__ == "__main__":
    main()

