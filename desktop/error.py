from config import DEBUG, ROWS, COLUMNS, RESOLUTION
import pygame.display as Display
from pygame.surface import Surface


class InputTimeout(Exception):
    message = "Could not get input from device."


class InvalidOptions(Exception):
    message = "Invalid option:"


class ServerHiccup(Exception):
    message = "There was a hiccup on the server. Bad server."


class UnexpectedInput(Exception):
    message = "Unexpected event type was returned."


class ConnectionTimeout(Exception):
    message = "Connection attempt timed out (took too long)."


class MapCapacityOverflow(Exception):
    message = "Map loaded but failed to comform to size" +\
              "constraints. map can only have" +\
              str(COLUMNS + 2) + " columns and " +\
              str(ROWS + 1) + " rows. Loading default map."

                  
class MapNotLoaded(Exception):
    message = "Default map failed to load."

class ReplayNotLoaded(Exception):
    message = "Replay failed to load."

class IPNotFound(Exception):
    message = "Could not determine this system's ip. Try --ip"

