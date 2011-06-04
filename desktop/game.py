import pygame
import sys

from time import time
from random import *
import pygame.mixer as sound
import pygame.display as Display
from pygame.time import get_ticks
from pygame import event as events
from pygame.sprite import spritecollide
from pygame.locals import *
from config import *
from player import *
from widget import *
from bomber import *
from explosion import *
from bomb import *
from powerup import *
from log import debug
from gameworld import *
from splashes import *
from socket import *
from map import *


class Game:
    def __init__(self, mapFile, playerList, randSeed):
        # This class will hold all sprites

        self.screen = Display.get_surface()
        self.randomizer = Random()
        self.randomizer.seed(randSeed[0:randSeed.find('.')])

        self.mapFile = mapFile
        self.randomMap = False
        if self.mapFile == 'random':
            self.randomMap = True

        self.world = GameWorld(self.randomizer)
        self.playerList = playerList

        self.respawnPoints = []
        self.timeToLive = TIMETOLIVE
        self.ticks = get_ticks()
        self.timeRoundStarted = self.ticks
        self.gameLoopCount = 0
        self.totalGameLoops = 0
        self.inputLogs = []

        # For recording player inputs for later testing
        self.record = False
        self.playerInputFileList = []

        # Load in sounds
        self.backgroundMusicList = [None]
        try:
            self.ES = sound.Sound(BOMBEXPLOSION)
            self.DB = sound.Sound(DROPBOMBSOUND)
            self.DS = sound.Sound(BOMBERMANDYING)
            self.BG = sound.Sound(BACKGROUNDMUSIC)
            self.RS = sound.Sound(RESPAWN)
            self.VS = sound.Sound(VICTORYMUSIC)

            # Load in sound tracks in BACKGROUNDMUSICLIST
            self.backgroundMusicList = []
            for track in BACKGROUNDMUSICLIST:
               try:
                   self.backgroundMusicList.append(sound.Sound(track))
               except:
                   print "BACKGROUNDMUSICLIST:", track, "could not load"

            self.sound = True
        except:
            self.sound = False
            self.backgroundMusicList = [None]

    def insertVHS(self, randSeed, fileName):
        f = file(fileName + '.replay', 'w')
        f.write(randSeed + '\n')
        f.write(str(len(self.playerList)) + '\n')
        f.write(self.mapFile + '\n')
        for i in range(0, len(self.playerList)):
            f.write(self.playerList[i].playerName + '\n')
        f.close()
        self.record = True
        for i in range(0, len(self.playerList)):
            self.playerInputFileList.append(file(fileName + str(i) + '.replay', 'w'))

    def start(self):
        self.setupWorld()
        while 1:
            self.gameLoopCount += 1
            debug('### Loop ' + str(self.gameLoopCount) + '\n')
            # Set the caption
            self.setCaption()

            # Revive dead players
            self.reviveDeadPlayers()

            # Check end game conditions
            playerWon = self.checkPlayerWon()
            if playerWon != None:
                self.endGame(playerWon)
                self.setupWorld()
            elif playerWon == None and len(self.world.bomberGroup.sprites())\
                     < 1:
                print 'Tie Game!'
                self.endGame(None)
                self.setupWorld()

            # Process all players input
            # and returned disconnected players.
            disconnectedPlayers = self.processInput()

            # If any player fails to talk,
            # kill that player and remove the player
            # from the player list
            for discedPlayer in disconnectedPlayers:
                # Kill the correct bomber
                for bomber in self.world.bomberGroup.sprites():
                    if bomber.player == discedPlayer:
                        self.world.removeBomber(bomber)
                # Kill the correct player
                print discedPlayer.getHandle(),'was dropped from the game.'
                self.playerList.remove(discedPlayer)

            # Decrement the TTL in all bombs
            self.decrementBombTTL()

            # Move everything
            self.world.update()

            rectsCleared = self.world.dirtyGroup.clear(self.world.screen,
                                                       self.world.background)

            dirtyShadows = SpriteGroup()
            for dirt in self.world.dirtyGroup.sprites():
                dirtyShadows.add(spritecollide(dirt.getShadow(),\
                                               self.world.flyOverGroup, 0))

            for bomber in self.world.bomberGroup.sprites():
                dirtyShadows.add(spritecollide(bomber.getShadow(),\
                                               self.world.bombGroup, 0))

            for explosion in self.world.explosionGroup.sprites():
                dirtyShadows.add(spritecollide(explosion.getShadow(),
                                               self.world.powerUpGroup, 0))

            dirtyRects = dirtyShadows.draw(self.world.screen)
            dirtyRects += self.world.dirtyGroup.draw(self.world.screen)
            pygame.display.update(dirtyRects)
            self.world.dirtyGroup.empty()

            # Run-out remaining time
            while(get_ticks() - self.ticks < GAMELOOPTIME):
                pass

            # Check tie game
            if(self.gameLoopCount > GAMETIMEINLOOPS):
                self.endGame(None)
                self.setupWorld()

            # Get time since game started
            self.ticks = get_ticks()

        # End of main game loop
        return None

    def actionBomb(self, bomber):
        if bomber.detonateEnable:
            for bomb in self.world.bombGroup.sprites():
                if bomb.getName() == bomber.getName():
                    bomb.TTL = 0

    def checkPlayerWon(self):
        # If only 1 bomber remains, end game.
        if len(self.world.bomberGroup.sprites()) == 1:
            if self.timeToLive == 0:
                # Turn off repeating background song channel
                if self.sound:
                    self.BG.stop()
                return self.world.bomberGroup.sprites()[0].player
            else:
                self.timeToLive -= 1

        # If all the bombers happen to die in the exact same game loop,
        # or if last remaining player fails to surive the timeToLive period.
        elif len(self.world.bomberGroup.sprites()) < 1:
            # Turn off repeating background song channel
            if self.sound:
                self.BG.stop()
        return None

    # Create all the widgets
    def createWidgets(self):
        """Create all the starting widgets"""
        mapFileLoaded = False


        # Attempt to load map given at command line
        if self.randomMap:
            randomI = self.randomizer.randint(0, len(MAPLIST) - 1)
            self.mapFile = MAPLIST[randomI]

        map = Map(self.mapFile,
                  self.world,
                  self.playerList)

        while len(self.playerList) > map.getCapacity():
            self.world.cleanState()
            self.mapFile = DEFAULTMAP
            map = Map(self.mapFile,
                      self.world,
                      self.playerList)

        self.respawnPoints = map.getRespawnPoints()

    def checkBomb(self, bombPos):
        """Return 1 if there is a bomb in given position."""
        bombPos = self.world.snapToGrid(bombPos)
        for bomb in self.world.bombGroup.sprites():
            if bomb.getPosition() == bombPos:
                return True
        return False

    def decrementBombTTL(self):
        """Decrement the TTL in all bombs
           Detonate bomb if TTL reaches zero
        """
        for bomb in self.world.bombGroup.sprites():
            bomb.tick()
            if bomb.readyToExplode():
                # If the bomb was in motion from a kick, make it snap to grid.
                bomb.setPosition(self.world.snapToGrid(bomb.getPosition()))
                # Create Explosion where bomb is
                explosionRect = Rect(((bomb.getPosition()), BLOCKSIZE))
                explosion = Explosion(Surface(BMANSIZE),\
                            explosionRect, EXPLOSIONTTL, bomb.napalm,\
                            bomb.radius, (0, 0), bomb.name, self.world)
                self.world.appendExplosion(explosion)
                explosion.attachToWorld(self.world)
                # Detonate bomb
                self.world.detonateBomb(bomb)
                self.explodeSound()

    def dropBomb(self, bomber):
        """Attempt to let bomber drop a bomb."""
        # Check current number of bombs droped by bomber in gameworld
        bombCount = 1
        for bomb in self.world.bombGroup.sprites():
            if bomb.getName() == bomber.getName():
                bombCount += 1

        # Ensure bomb count is less than bomber's capacity,
        # bomber doesn't have constipation, and there is no
        # bomb currently where bomb is to be placed.
        bombPos = bomber.getPosition()
        # Check bomber capasity and constipation
        if bombCount <= bomber.capacity and\
            bomber.virusDict[CONSTIPATION] == 0:
            # Check if a bomb is there
            if not self.checkBomb(bombPos):

                # If not, create bomb
                bombRect = Rect(((bombPos), BLOCKSIZE))

                # Set bomb TTL
                bombTTL = bomber.TTL
                if bomber.virusDict[SHORTFUSE] > 0:
                    if not bomber.detonateEnable:
                        bombTTL = SHORTBOMBTTL
                    else:
                        bombTTL = SHORTBOMBTTL * 2

                # If bomber has short fuse and romote detonate bombs,
                # they last longer than if bomber didn't have
                elif bomber.virusDict[SHORTFUSE] > 0 and bomber.detonateEnable:
                    bombTTL = SHORTBOMBTTL * 2
                # Set bomb's explosion radius
                bombRadius = bomber.radius
                if bomber.virusDict[SHORTRADIUS] > 0:
                    bombRadius = 1

                # Create bomb
                bomb = Bomb(Surface(BMANSIZE), bombRect, bombTTL,
                      bomber.napalm, bombRadius, bomber.getName())
                self.world.appendBomb(bomb)
                bomber.lastBombPlaced = bomb

                # If the bomber has napalm bombs
                if bomber.napalm > 0:
                    bomber.decrementNapalm()
                bombsPos = bomb.getPosition()
                bomb.setPosition(self.world.snapToGrid(bombsPos))
                bomb.attachToWorld(self.world)

                # Check for players standing on top of the bomb
                # add them to a list
                playersOnTop = spritecollide(bomb, self.world.bomberGroup, 0)
                playersOnTop.sort(lambda x, y: cmp(x.id, y.id))
                bomb.setPlaced(playersOnTop)
                self.world.appendPopulatedBomb(bomb)

                self.dropBombSound()

            else:
                # Check if bomber has spooge power-up
                pass
                #Insert code for spooge power-up here

    def dropBombSound(self):
        """Output drop bomb sound"""
        # We still have to make a new drop bomb sound
        #if (self.sound):
        #    self.DB.play(0)

    def victorySound(self):
        """Output victory sound"""
        if (self.sound):
            self.VS.play(1)

    def respawnSound(self):
        """Output respawn sound"""
        if (self.sound):
            self.RS.set_volume(0.75)
            self.RS.play(0)

    def dyingSound(self):
        """Output dying sound"""
        if (self.sound):
            self.DS.set_volume(0.75)
            self.DS.play(0)

    def explodeSound(self):
        """Output explosion sound"""
        if (self.sound):
            self.ES.set_volume(0.30)
            self.ES.play(0)

    def exchangeInput(self):
        """Exchange a round of inputs in a network-safe
           manner.
        """
        inputs = []
        for player in self.playerList:
            inp = self.getPlayerInput(player)
            debug("Player " + str(player.name) +\
                  " input: " + inp + "\n")
            if self.record and inp != NOOP:
                self.playerInputFileList[int(player.name)].write( \
                  str(self.totalGameLoops) +\
                  ',' + inp + '\n')

            # Check players input
            if len(inp) != len(UP):
                print "Bad input from player",player.getHandle()
                inp = DISCONNECT

            # Can quit the game from end splash screen
            if inp == QUITCOMMAND:
                sys.exit()

            inputs.append((player.name,inp))
            for netplayer in self.playerList:
                netplayer.sendCommand(player.getBroadcastable())

        self.totalGameLoops += 1
        # Clear all useless events
        eventsWeWant = events.get([KEYDOWN, KEYUP, JOYBUTTONDOWN,\
                                   JOYAXISMOTION])
        events.clear()
        for event in eventsWeWant:
            events.post(event)
        return inputs

    def getPlayerInput(self, player):
        """Get a single player's input. Do not return
           without input unless player dropped.
        """
        command = ""
        noSignal = True
        startListen = time()
        while(noSignal and (time() - startListen < LISTENTIMEOUT)):
            try:
                command = player.getInput()
                noSignal = False
            except InputTimeout:
                pass
        if(noSignal):
            print "A player's input seems to have timed out."
            return DISCONNECT

        return str(command)

    def processInput(self):
        """Get all players input and process it

           move player, exit game,
           and handle bomb creation if command was given.
        """
        disconnectPlayers = []
        inputs = self.exchangeInput()

        bomberGroupSorted = self.world.bomberGroup.sprites()
        bomberGroupSorted.sort(lambda x, y: cmp(x.id, y.id))
        for w in bomberGroupSorted:
            debug("Player " + str(w.name) + " position: "\
                  + str(w.getPosition()) + "\n")

        for (currentBomberName, command) in inputs:
            if (command == QUITCOMMAND):
                sys.exit()

            # Move bomber in direction of command given
            # If command is not 'Stop'
            if(command != STOP):
                bomber = None
                bomberGroupSorted = self.world.bomberGroup.sprites()
                bomberGroupSorted.sort(lambda x, y: cmp(x.id, y.id))
                for w in bomberGroupSorted:
                    if w.getName() == str(currentBomberName):
                        bomber = w
                if bomber != None:
                    # Make the bomber drop a bomb if he has 'the runs'
                    if bomber.virusDict[RUNS] > 0:
                        self.dropBomb(bomber)
                    # Set the bombers speed for next step
                    speed = bomber.speed
                    if bomber.virusDict[TURTLE] > 0:
                        speed = BMANTURTLE
                    # Up
                    if(command == bomber.player.commandSet[0]):
                        bomber.setMovement((0, -speed))
                    # Down
                    elif(command == bomber.player.commandSet[1]):
                        bomber.setMovement((0, speed))
                    # Left
                    elif(command == bomber.player.commandSet[2]):
                        bomber.setMovement((-speed, 0))
                    # Right
                    elif(command == bomber.player.commandSet[3]):
                        bomber.setMovement((speed, 0))
                    # Action
                    elif(command == bomber.player.commandSet[4]):
                        self.actionBomb(bomber)
                    # Bomb
                    elif(command == bomber.player.commandSet[5]):
                        # Attempt to let player drop a bomb.
                        self.dropBomb(bomber)
                    elif(command == DISCONNECT):
                        disconnectPlayers.append(bomber.player)

            # Stop bomber and drop a bomb if bomber has 'the runs'
            else:
                for bomber in self.world.bomberGroup.sprites():
                    if(bomber.getName() == str(currentBomberName)):
                        # Make the bomber drop a bomb if he has 'the runs'
                        if bomber.virusDict[RUNS] > 0:
                            self.dropBomb(bomber)
                        # Stop bomber
                        bomber.setStop()

        return disconnectPlayers

    def reviveDeadPlayers(self):
        """If players are dead and have more lives remaining revive them."""
        for player in self.playerList:
            if player.dead:
                # If player has more lives
                if player.lives > 0:
                    # Player is now alive
                    player.dead = False
                    # Recreate players bomberperson
                    respawnPoint = \
                    self.respawnPoints[self.randomizer.randint(0,\
                                       len(self.respawnPoints) - 1)]
                    bomberRect = Rect(((respawnPoint), BMANSIZE))
                    bomber = Bomber(Surface((0, 0)), bomberRect, player)
                    self.world.appendBomber(bomber)
                    bomber.attachToWorld(self.world)
                    # Play respawn sound
                    self.respawnSound()

    def endGame(self, winningPlayer):
        # Assume a tie game.
        # If there is a winner, reconstruct the endSplash.

        # Stop background music for endgame splash
        if self.sound:
            self.BG.stop()

        endSplash = getEndGameSplash()
        if winningPlayer != None:
            for player in self.playerList:
                if player.playerName == winningPlayer.playerName:
                    player.score += 1
            endSplash = getEndGameSplash(winningPlayer.playerName,
                                         winningPlayer.color)

            # Play winning sound
            self.victorySound()

        print self.score(self.playerList)
        self.world.screen.blit(self.world.background,
                               self.world.background.get_rect())
        endSplash.draw(self.world.screen)
        pygame.display.flip()
        for player in self.playerList:
            player.neuralize()
        donePeeps = {}
        while len(donePeeps) != len(self.playerList):
            inputs = self.exchangeInput()
            for inp in inputs:
                currentBomberName = inp[0]
                command = inp[1]
                if command != NOOP:
                    donePeeps[currentBomberName]  = True
            endSplash.clear(self.world.screen, self.world.background)
            endSplash.update()
            dirty = endSplash.draw(self.world.screen)
            pygame.display.update(dirty)

    def score(self, playerList):
        '''display the players score with top players on top'''
        scoreList = list(playerList)

        scoreList.sort(lambda x, y: -cmp(x.score, y.score))
        string = 'Score\tPlayer Name\n'
        for player in scoreList:
            string = string + '%3d\t%s\n' % (player.score, player.playerName)
        return string

    def removePlayer(self, player):
        """When a Player is killed, remove his/her Player object from
           the player group
        """
        self.playerList.remove(player)

    def setCaption(self):
        """Set the Caption with game time remaining and players'\
           remaining lives.
        """
        roundTimeRemaining = (((GAMETIMEINLOOPS - self.gameLoopCount)\
                               * GAMELOOPTIME) / 1000)
        caption = 'Pybomber [Time:' + \
                  str(roundTimeRemaining) + '] Player Lives Remaining:'
        debug("Time remaining: " + str(roundTimeRemaining) + "\n")
        for player in self.playerList:
            if player.lives == 0 :
                caption = caption + '   P' + str(int(player.name) + 1) +\
                          ': X'
            else:
                caption = caption + '   P' + str(int(player.name) + 1) +\
                          ': ' + str(player.lives)
        pygame.display.set_caption(caption)

    def setupWorld(self):
        self.world.cleanState()
        self.respawnPoints = []

        # This MUST be executed regardless of self.sound's value
        # (if self.randomizer is going to be used)
        bgMusicIndex = self.randomizer.randint(0, \
                         len(self.backgroundMusicList) - 1)

        # Sound effects
        if (self.sound):
            # Kill Victory Music
            self.VS.stop()

      # Choose in random background song from
      # backgroundMusicList
            self.BG = self.backgroundMusicList[bgMusicIndex]
            # Loops song until pygame terminates
            self.BG.set_volume(1.0)
            self.BG.play(-1)

        # Create all the Widgets
        self.createWidgets()

        self.ticks = get_ticks()
        self.timeToLive = TIMETOLIVE
        self.timeRoundStarted = self.ticks
        self.gameLoopCount = 0

        # Move everything
        self.world.universalGroup.clear(self.world.screen, \
                                        self.world.background)
        self.world.update()
        self.world.universalGroup.draw(self.world.screen)
        pygame.display.flip()
