from commands import HQFunctions
from commands import EasterEggFunctions
from commands import PostboxFunctions
from commands import KeyFunctions
from commands import HelpFunctions

class Intern(HQFunctions,
             EasterEggFunctions,
             PostboxFunctions,
             KeyFunctions,
             HelpFunctions):

    def __init__(self):
        super(Intern,self).__init__()
