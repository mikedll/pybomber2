from pygame import event as events
from pygame import key
from pygame.locals import *
from config import *
from joyinput import *
from error import UnexpectedInput


class InputDevice:
    """Encapsulate an input device (keyboard, mouse, etc)

       Untestable without someone using the device.
    """
    def __init__(self, name):
        self.name = name

    def get(self):
        """Return a string representing a command.

        Return "-" (no operation)
        if no command is given.
        """
        raise NotImplementedError('abstract method')


class Joystick(InputDevice):
    def __init__(self, name):
        InputDevice.__init__(self, name)
        self.joyPad = Translator()
        self.joyEnabled = self.joyPad.joyEnabled(name)

    def get(self):
        events.pump()
        notmine = []
        inp = NOOP
        for event in events.get():
            if event.type == QUIT:
                inp = QUITCOMMAND

            elif (event.dict
                and event.dict.has_key('joy')
                and event.dict['joy'] == self.joyEnabled.get_id()):
                if event.type == JOYBUTTONDOWN:
                    if self.joyEnabled.get_button(0):
                        inp = BOMB
                    elif self.joyEnabled.get_button(1):
                        inp = ACTION
                elif event.type == JOYAXISMOTION:
                    if self.joyEnabled.get_numaxes() >= 6:
                        if self.joyEnabled.get_axis(5) > 0.2:
                            inp = DOWN
                        elif self.joyEnabled.get_axis(5) < -0.2:
                            inp = UP
                        elif self.joyEnabled.get_axis(4) < -0.2:
                            inp = LEFT
                        elif self.joyEnabled.get_axis(4) > 0.2:
                            inp = RIGHT
                        elif self.joyEnabled.get_axis(5) <= 0.1 and\
                                 self.joyEnabled.get_axis(5) >= -0.1 and\
                                 self.joyEnabled.get_axis(4) <= 0.1 and\
                                 self.joyEnabled.get_axis(4) >= -0.1:
                            inp = STOP
                    
                    if self.joyEnabled.get_axis(1) > 0.2:
                        inp = DOWN
                    elif self.joyEnabled.get_axis(1) < -0.2:
                        inp = UP
                    elif self.joyEnabled.get_axis(0) < -0.2:
                        inp = LEFT
                    elif self.joyEnabled.get_axis(0) > 0.2:
                        inp = RIGHT
                    elif self.joyEnabled.get_axis(0) <= 0.1 and\
                             self.joyEnabled.get_axis(0) >= -0.1 and\
                             self.joyEnabled.get_axis(1) <= 0.1 and\
                             self.joyEnabled.get_axis(1) >= -0.1:
                        inp = STOP
            else:
                notmine.append(event)

        for yours in notmine:
            events.post(yours)

        return inp


class Keyboard(InputDevice):
    def __init__(self, keyDict, name):
        InputDevice.__init__(self, name)

        self.keyDict = keyDict
        self.commandDict = {}

        # This is the opposite map of the key dictionary.
        # It improves speed at the expense
        # of memory for doing reverse-lookups
        #   e.g. "Is the player pressing up?"
        for k in self.keyDict.keys():
            self.commandDict[self.keyDict[k]] = k

    def get(self):
        events.pump()
        notmine = []
        inp = NOOP
        for event in events.get():
            if event.type == QUIT:
                inp = QUITCOMMAND
            if ((event.type == KEYDOWN or event.type == KEYUP)
                and self.keyDict.has_key(event.key)):
                if event.type == KEYDOWN:
                    inp = self.keyDict[event.key]
                elif event.type == KEYUP:
                    keyDown = key.get_pressed()
                    if(keyDown[self.commandDict[UP]]):
                        inp = UP
                    elif(keyDown[self.commandDict[DOWN]]):
                        inp = DOWN
                    elif(keyDown[self.commandDict[LEFT]]):
                        inp = LEFT
                    elif(keyDown[self.commandDict[RIGHT]]):
                        inp = RIGHT
                    else:
                        inp = STOP
                else:
                    raise UnexpectedInput
            else:
                notmine.append(event)

        for yours in notmine:
            events.post(yours)

        return inp

