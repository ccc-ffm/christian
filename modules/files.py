"""Provide filehandling"""
import os
import random

class Filehandler(object):
    """Get content of files"""

    def __init__(self):
        pass

    @classmethod
    def exists(cls, filename):
        """Check if file exists"""
        if not os.path.isfile(filename):
            return False
        else:
            return True

    @classmethod
    def getcontent(cls, filename):
        """Return full content"""
        filecont = ""
        if not cls.exists(filename):
            return "Something went terribly wrong, better luck next time!"
        with open(filename, 'r') as infile:
            for line in infile:
                filecont += line.strip() + "\n"
        infile.close()
        return filecont

    @classmethod
    def getrandomline(cls, filename):
        """Return a random line from a file"""
        if not cls.exists(filename):
            return "Something went terribly wrong, better luck next time!"

        else:
            #Jonathan Kupferman:
            #http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
            #Open the file:

            my_file = open(filename, 'r')

            #Get the total file size
            file_size = os.stat(filename)[6]

            #seek to a place in the file which is a random distance away
            #Mod by file size so that it wraps around to the beginning
            my_file.seek((my_file.tell()+random.randint(0, file_size-1))%file_size)

            #dont use the first readline since it may fall in the middle of a line
            my_file.readline()

            #this will return the next (complete) line from the file
            line = my_file.readline()
            my_file.close()
            return line
