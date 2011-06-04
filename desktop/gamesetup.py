import re
import pygame
from time import time
from error import *
from inputdevice import *
from player import *
from splashes import *
from error import *
from log import *
from socket import error as SocketError
from socket import gaierror as SocketServiceError
from socket import *
from time import time as timeSinceStart
from config import HAMMERDELAY, CONNECTTIMEOUT

class GameSetup:
    def __init__(self, options):
        self.randomSeed = str(time())
        self.playerList = []
        self.localPlayerList = []
        self.options = options
        self.buildLocalPlayers()

    def init(self):
        """This method must be called before using
           the GameSetup classes.
        """
        return

    def buildLocalPlayers(self):
        # The list of all local players that could be in a game.
        self.localPlayerList = []
        self.playerNames = None
        # Attempt to open playernames file to load saved names.
        try:
            f = open(LOCALNAMESFILE, 'r')
            self.playerNames = f.readlines()
            f.close()
        except:
            self.playerNames = None

        # The mumber of players can be number of game pads +3 keyboard players,
        # with max of 10.
        # (Unless this is going to be a network game)
        i = 0
        gamepads = pygame.joystick.get_count()
        if gamepads != 0:
            print gamepads, 'game pads detected...'
        if gamepads > 10:
            gamepads = 10
            print 'A maximum of 10 game pads can used.'
        for gamepad in range (0, gamepads):
            # This creates a joy stick object to get the name for each
            gamepad = pygame.joystick.Joystick(i)
            print i, gamepad.get_name()
            inputDev = Joystick(str(i))
            if self.playerNames != None:
                self.playerNames[i] = self.playerNames[i][0:-1]
                self.localPlayerList.append(LocalPlayer(inputDev, str(i),
                self.playerNames[i], COLORDICT[i]))
            else:
                self.localPlayerList.append(LocalPlayer(inputDev, str(i),
                'Gamepad Player ' + str(i + 1), COLORDICT[i]))
            i += 1

        j = 0
        while i < 10 and j < len(KEYDICTLIST):
            inputDev = Keyboard(KEYDICTLIST[j], str(i))
            if self.playerNames != None:
                self.playerNames[i] = self.playerNames[i][0:-1]
                self.localPlayerList.append(LocalPlayer(inputDev, str(i),
                self.playerNames[i], COLORDICT[i]))
            else:
                self.localPlayerList.append(LocalPlayer(inputDev, str(i),
                'Keyboard Player ' + str(i + 1), COLORDICT[i]))
            i += 1
            j += 1

    def gatherAtServer(self):
        """
           Build a player dictionary with server-client
           with clients and a centralized serer.
        """
        raise NotImplementedError('abstract method')

    def getRandomSeed(self):
        return str(self.randomSeed)

    def getPlayerList(self):
        return self.playerList

    def getGameMap(self):
        return self.options.mapFile


class ScriptedSetup(GameSetup):
    def __init__(self, options):
        GameSetup.__init__(self, options)
        self.playerList = self.localPlayerList

    def buildLocalPlayers(self):
        # The list of all local players that could be in a game.
        self.localPlayerList = []
        playerNames = []
        # Attempt to open playernames file to load saved names.
        try:
            f = file(self.options.replay + ".replay", "r")
            seed = f.readline()
            self.randomSeed = seed[0:-1]
            numPlayers = f.readline()
            numPlayers = int(numPlayers[0:-1])
            self.options.mapFile = f.readline()
            self.options.mapFile = self.options.mapFile[0:-1]
            for i in range(0, numPlayers):
                playerName = f.readline()
                playerName = playerName[0:-1]
                playerNames.append(playerName)
            f.close()
        except IOError:
            raise ReplayNotLoaded, ReplayNotLoaded.message

        # Create scripted players to read input from file.
        for i in range(0, numPlayers):
            inputFile = self.options.replay + str(i) + '.replay'
            scriptedPlayer = ScriptedPlayer(str(i), playerNames[i],
              COLORDICT[i], inputFile)
            self.localPlayerList.append(scriptedPlayer)


class LocalSetup(GameSetup):
    def __init__(self, options):
        GameSetup.__init__(self, options)

        # Start game with splash screen
        #startGame()
        numGamePads = pygame.joystick.get_count()
        numPlayers = int(options.numPlayers)
        # If the number of players was not given at the command line...
        if numPlayers == 0:
            # If there are at least 2 joysticks, the number of joysticks as the
            # number of players.
            if numGamePads >= 2:
                numPlayers = numGamePads
            # Otherwise, set the default, which is 2.
            else:
                numPlayers = 2
        # append all the players to the self.playerList
        if 2 <= numPlayers and numPlayers <= 10 and \
            numPlayers <= len(self.localPlayerList):
            for player in range (0, numPlayers):
                self.playerList.append(self.localPlayerList[player])
        else :
            raise error, 'Number of players can be between 2 and 10, but can'\
                        ' not be more than the number of game pads connected'\
                        ' plus 3 keyboard controlled players.'

        if options.colors:
            BomberColors = ColorPicker(0)
            BomberColors.pickColors(self.playerList)

            # Atempt to open playername file to save players name
            try:
                f = open(LOCALNAMESFILE, 'w')
                i = 1
                for player in self.playerList:
                    f.write(player.playerName + '\n')
                    i += 1
                while i <= 10:
                    f.write(str(i) + '\n')
                    i += 1
                f.close()
            except IOError:
                print 'Failed to save player names!'
        else:
            import color_picker
            BomberColors = color_picker.ColorPicker(1)
            BomberColors.pickColors(self.playerList)


class NetworkSetup(GameSetup):
    def __init__(self, options):
        GameSetup.__init__(self, options)
        self.port = int(options.port)
        self.clientNamesToIPs = {}
        self.clientIPsToNames = {}
        self.namesToHandles = []
        
        try:
            self.hostToBindTo = gethostbyname(gethostname())
        except SocketServiceError, msg:
            if self.options.serverMode:
                if self.options.ip != "0.0.0.0":
                    self.hostToBindTo = self.options.ip
                else:
                    raise IPNotFound, IPNotFound.message
            pass
        
        

    def init(self):
        # Hax. need to get to work with > 1 player.
        self.localPlayerList = [self.localPlayerList[0]]
        self.gatherAtServer()
        self.loadNetworkNames()
        self.peerConnect()

    def getNamesToIPs(self):
        return self.clientNamesToIPs

    def getNameByIP(self, ip):
        return self.clientIPsToNames[str(ip)]

    def getIPsToNames(self):
        return self.clientIPsToNames

    def getIPByName(self, name):
        return self.clientNamesToIPs[name]

    def playerCount(self):
        return len(self.clientNamesToIPs)

    def connectAsClient(self, host, port, timelimit = CONNECTTIMEOUT):
        freshSocket = socket(AF_INET, SOCK_STREAM)
        freshSocket.settimeout(HAMMERDELAY)
        notConnected = True
        startConn = time()
        while notConnected and (time() - startConn < timelimit):
            try:
                freshSocket.connect((str(host), port))
                notConnected = False
            except SocketError:
                pass

        if(notConnected):
            print "Could not connect to", host
            raise ConnectionTimeout

        return freshSocket

    def connectAsServer(self, host, port, timelimit = CONNECTTIMEOUT):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((host, port))
        serverSocket.listen(1)
        serverSocket.settimeout(HAMMERDELAY)
        notConnected = True
        startConn = time()
        while notConnected and (time() - startConn < timelimit):
            try:
                (freshSocket, addy) = serverSocket.accept()
                notConnected = False
            except SocketError, msg:
                pass
        if(notConnected):
            print "Could not connect to", host
            raise ConnectionTimeout, ConnectionTimeout.message
        freshSocket.settimeout(HAMMERDELAY)
        return freshSocket

    def loadNetworkNames(self):
        # Attempt to open playernames file to load saved names.
        try:
            f = open(NETWORKNAMESFILE, 'r')
            self.namesToHandles = f.readlines()
            f.close()
            # Remove newlines
            for i in range(0, self.playerCount()):
                self.namesToHandles[i] = self.namesToHandles[i][0:-1]
        except:
            print 'Failed to load player names...'
            self.namesToHandles = [1,2,3,4,5,6,7,8,9,10]

    def getHandleByName(self, name):
        return self.namesToHandles[name]

    def peerConnect(self):
        """Adam and Mike's Helen Keller reconnection algorithm."""

        updateLoadScreen("Connecting to peers...")

        # Iterate from player 0 to N
        # Have player i listen for all connections it has not made
        connectedPlayers = []
        i = 0
        while i < self.playerCount():
            if self.getIPByName(i) == "0.0.0.0":
                localPlayer = self.localPlayerList.pop()
                localPlayer.name = str(i)
                localPlayer.playerName = self.getHandleByName(i)
                localPlayer.setColor(COLORDICT[i])
                self.playerList.append(localPlayer)
                connectedPlayers.append(i)

                # Start listening for connections
                # upward of yourself
                j = i
                while j < self.playerCount():
                    if self.getIPByName(j) != "0.0.0.0" and \
                      j not in connectedPlayers:
                        port = int(self.port) + j + 1
                        try:
                            sock = self.connectAsServer(self.hostToBindTo,
                                                        port,
                                                        CONNECTTIMEOUT)
                        except ConnectionTimeout:
                            raise SystemExit, ConnectionTimeout.message

                        netPlayer = NetworkPlayer(str(j),
                                                  self.getHandleByName(j),
                                                  COLORDICT[j])
                        netPlayer.setConnection(sock)
                        self.playerList.append(netPlayer)
                        connectedPlayers.append(j)
                    j += 1
            else:
                if i not in connectedPlayers:
                    ip = self.getIPByName(i)
                    port = int(self.port) + self.getNameByIP("0.0.0.0") + 1

                    try:
                        sock = self.connectAsClient(ip, port, CONNECTTIMEOUT)
                    except ConnectionTimeout:
                        raise SystemExit, ConnectionTimeout.message

                    netPlayer = NetworkPlayer(str(i),
                                              self.getHandleByName(i),
                                              COLORDICT[i])
                    netPlayer.setConnection(sock)
                    self.playerList.append(netPlayer)
                    connectedPlayers.append(i)
            i += 1

        BomberColors = ColorPicker(1)
        BomberColors.pickColors(self.playerList)


class ClientSetup(NetworkSetup):
    def __init__(self, options):
        NetworkSetup.__init__(self, options)
        self.server = gethostbyname(options.clientMode)

    def gatherAtServer(self):
        encodedPlayerNames = ''
        for player in self.localPlayerList:
            encodedPlayerNames += player.playerName + '\n'

        updateLoadScreen("Connecting to server...")

        sockToServer = None
        try:
            sockToServer = self.connectAsClient(self.server,
                                                self.port,
                                                CONNECTTIMEOUT)
        except ConnectionTimeout:
            raise SystemExit, ConnectionTimeout.message

        try:
            sockToServer.sendall(encodedPlayerNames)
        except SocketError:
            raise ServerHiccup, ServerHiccup.message

        waitingForStart = True
        startConn = time()
        serverString = ""
        while waitingForStart and (time() - startConn < STARTGAMEDELAY):
            try:
                updateLoadScreen("Waiting for server to start game...")
                serverString = sockToServer.recv(1024)
                waitingForStart = False
            except:
                pass

        if waitingForStart:
            raise SystemExit, "Server did not start game soon enough."

        updateLoadScreen("Got start signal from server...")

        # The incoming string will have 0.0.0.0 in place of the server's ip,
        # and local.0.0.0 in place of this local computer's ip.
        #
        # (some computers have trouble figuring out their WAN ip)

        # Put in the server's real IP
        serverString = re.sub("0\.0\.0\.0",self.server,serverString)

        # Set this computer ip to be 0.0.0.0
        serverString = re.sub("local\.0\.0\.0","0.0.0.0",serverString)

        encodedList, \
          self.randomSeed, \
          self.options.mapFile, \
          encodedPlayerNames = serverString.split('*')
        encodings = encodedList.split(',')
        f = open(NETWORKNAMESFILE, 'w')
        f.write(encodedPlayerNames)
        f.close()
        for encoding in encodings:
            (name, ip) = encoding.split(":")
            self.clientNamesToIPs[int(name)] = ip
            self.clientIPsToNames[ip] = int(name)


class ServerSetup(NetworkSetup):
    def __init__(self, options):
        NetworkSetup.__init__(self, options)
        self.clientCount = int(options.serverMode)

    def gatherAtServer(self):
        sockForArrivals = socket(AF_INET, SOCK_STREAM)
        sockForArrivals.bind((self.hostToBindTo,self.port))
        sockForArrivals.settimeout(HAMMERDELAY)
        sockForArrivals.listen(self.clientCount)

        # Initialize encoded names list
        encodedPlayerNames = self.localPlayerList[0].playerName + '\n'

        # Start building ip-to-name and name-to-ip dictionaries
        self.clientNamesToIPs[len(self.clientNamesToIPs)] = "0.0.0.0"
        self.clientIPsToNames["0.0.0.0"] = len(self.clientIPsToNames)

        connected = []
        lastBreak = timeSinceStart()
        while len(connected) < self.clientCount:
            notConnected = self.clientCount - len(connected)
            updateLoadScreen("Waiting for " + str(notConnected) + " client(s) to connect...")
            arrivalSocket, addy = None, None
            try:
                (arrivalSocket, addy) = sockForArrivals.accept()
            except SocketError, msg:
                pass

            if arrivalSocket != None:
                nameOfArrival = arrivalSocket.recv(1024)
                encodedPlayerNames += nameOfArrival
                self.clientNamesToIPs[len(self.clientNamesToIPs)] =\
                  gethostbyname(addy[0])
                self.clientIPsToNames[addy[0]] = len(self.clientNamesToIPs)
                connected.append((arrivalSocket, addy))
                nameOfArrival = re.sub(r"\n","",nameOfArrival)
                print nameOfArrival,"at", addy[0], "connected..."

            # Give a chance to kill the program - for some reason
            # signals still don't make it to the program
            # even if there is a delay.
            while(timeSinceStart() - lastBreak < HAMMERDELAY):
                pass
            lastBreak = timeSinceStart()

        # Write player names to file
        try:
            f = open(NETWORKNAMESFILE, 'w')
            f.write(encodedPlayerNames)
            f.close()
        except:
            print 'Failed to write to network player names file.'

        # Encode info to send to clients
        encodings = []
        for playerNum in self.clientNamesToIPs.keys():
            encodings.append(":".join([str(playerNum),\
                                       str(self.clientNamesToIPs[playerNum])]))

        encodedList = ",".join(encodings)
        encodedList += "*" + str(self.randomSeed)
        encodedList += "*" + self.options.mapFile
        encodedList += "*" + encodedPlayerNames

        for conn in connected:
            sock = conn[0]
            addy = conn[1]
            ipOfTarget = addy[0]

            # The computer you are sending info to has to realize
            # which # it is without knowing its own WAN ip, so mark it
            # explicitely.
            customizedList = re.sub(ipOfTarget, "local.0.0.0", encodedList)
            sock.sendall(customizedList)

