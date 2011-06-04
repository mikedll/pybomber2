from socket import error as SocketError
from socket import *
from inputdevice import *
from error import *
from config import *

"""Encapsulate a player's input and output.  (as a protocol standard, all input
   must be followed by output from the server)
"""


class Player:
    """
        >>> import player
        >>> p1 = Player('0',"Stan",0)
        >>> p1.setColor(1)
        >>> p1.getColor()
        1
        >>> p1.disableInput()
        >>> p1.dead
        True
        >>> p1.neuralize()
        >>> p1.dead
        False
        >>> p1.lives
        1
    """
    def __init__(self, folderName, playerName, color):
        self.cachedCommand = NOOP
        self.name = folderName          # Folder name (i.e. number)
        self.playerName = playerName    # People playing game 
        self.dead = False
        self.lives = BMANLIVES
        self.score = 0
        self.kills = 0
        self.color = color
        self.commandSet = COMMANDSET[0]

    def neuralize(self):
        self.dead = False
        self.lives = BMANLIVES

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def getHandle(self):
        return self.playerName

    def disableInput(self):
        self.dead = True

    def getBroadcastable(self):
        return ""

    def getInput(self):
        """
        >>> import player
        >>> p1 = Player('0',"Stan",0)
        >>> p2 = Player('1',"Betsy",1)
        >>> command = p1.getInput()
        >>> command
        ''
        """
        return ""

    def sendCommand(self, state):
        """
        >>> import player
        >>> p3 = Player('0',"Stan",0)
        >>> stateAsString = "Hello"
        >>> p3.sendCommand(stateAsString)
        0
        """
        return 0


class ScriptedPlayer(Player):
    def __init__(self, name, playerName, color, fileName):
        Player.__init__(self, name, playerName, color)
        self.commands = []
        self.nextCommand = 0
        self.currentLoop = 0
        self.loadFile(fileName)

    def loadFile(self, fileName):
        self.commands = []
        self.nextCommand = 0
        self.currentLoop = 0
        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                line = line[0:-1]
                loopNum, command = line.split(',')
                self.commands.append((loopNum, command))
        except:
            raise error

    def getInput(self):
        command = "----"
        if self.nextCommand < len(self.commands) and \
           self.currentLoop == int(self.commands[self.nextCommand][0]):
            command = self.commands[self.nextCommand][1]
            self.nextCommand += 1
        self.currentLoop += 1
        self.cachedCommand = command
        return self.cachedCommand


class NetworkPlayer(Player):
    def __init__(self, name, playerName, color):
        Player.__init__(self, name, playerName, color)

    def setConnection(self, conn):
      """Set socket for this player"""
      self.conn = conn

    def getInput(self):
        """Return "command" if an actual command is received
           from the player. Return "" if no command is received.

           >>> import player
           >>> from threading import Thread
           >>> from time import sleep
           >>> from time import time as now
           >>> from socket import *

           >>> responses = []
           >>> FREEPORT = 35024
           >>> expectedHost = gethostname()
           >>> inputFailures = 0

           >>> def remoteSend():
           ...     global FREEPORT
           ...     guestSocket = socket(AF_INET, SOCK_STREAM)
           ...     notConnected = True
           ...     startConn = now()
           ...     while(notConnected and (now() - startConn < 5)):
           ...         try:
           ...             guestSocket.connect((gethostname(), FREEPORT))
           ...             notConnected = False
           ...         except SocketError:
           ...             passrespon
           ...     guestSocket.sendall("1st command")

           >>> def playerListen():
           ...     global responses, FREEPORT, inputFailures
           ...     serverSocket = socket(AF_INET, SOCK_STREAM)
           ...     serverSocket.bind((gethostname(),FREEPORT))
           ...     serverSocket.listen(1)
           ...     (playerSocket, addy) = serverSocket.accept()
           ...     playerSocket.setblocking(False)
           ...     a = NetworkPlayer('0',"Steve",0)
           ...     a.setConnection(playerSocket)
           ...     noSignal = True
           ...     startListen = now()
           ...     while(noSignal and (now() - startListen < 1)):
           ...         try:
           ...             responses.append(a.getInput())
           ...             noSignal = False
           ...         except InputTimeout:
           ...             inputFailures = inputFailures + 1
           ...             pass
           ...     serverSocket.close()

           >>> playerThread = Thread(None, playerListen, None)
           >>> guestThread = Thread(None, remoteSend, None)
           >>> playerThread.start()
           >>> while(not playerThread.isAlive()):
           ...     pass
           >>> guestThread.start()
           >>> startTime = now()
           >>> while((now() - startTime < 3) and
           ...       (playerThread.isAlive() or guestThread.isAlive())):
           ...     pass
           >>> responses
           ['1st command']
        """

        msg = ""
        try:
            msg = self.conn.recv(PACKETSIZE)
        except (SocketError):
            msg = ""
            raise InputTimeout

        self.cachedCommand = msg

        if(self.dead):
            return NOOP
        else:
            return self.cachedCommand

    def getBroadcastable(self):
        return ""

    def sendCommand(self, cmd):
        if(cmd != ""):
            self.conn.sendall(cmd)


class LocalPlayer(Player):
    def __init__(self, inputDevice, folderName, playerName, color):
        Player.__init__(self, folderName, playerName, color)
        self.inputDevice = inputDevice

    def getInput(self):
        self.cachedCommand = self.inputDevice.get()
        if(self.dead):
            return NOOP
        return self.cachedCommand

    def getBroadcastable(self):
        return self.cachedCommand

