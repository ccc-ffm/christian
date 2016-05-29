from commands import HQFunctions
from commands import EasterEggFunctions
from commands import PostboxFunctions
from commands import KeyFunctions
from commands import HelpFunctions

from commands import ServiceFunctions

class Intern(HQFunctions,
             EasterEggFunctions,
             PostboxFunctions,
             KeyFunctions,
             HelpFunctions):

    def __init__(self):
        PostboxFunctions.__init__(self)
        HelpFunctions.__init__(self)
