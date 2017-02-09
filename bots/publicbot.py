from commands import ServiceFunctions
from commands import HelpFunctions


class Public(ServiceFunctions, HelpFunctions, EasterEggFunctions):

    def __init__(self):
        super(Public,self).__init__()
