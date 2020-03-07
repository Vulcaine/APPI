import subprocess
import sys
import ctypes
import os

from logger import Logger

def AddToPathPrompt(syspath):
    message = "Would you like to add {} to path?".format(syspath)

    return CustomPrompt(
                    message,
                    lambda: AddToPath(syspath)
                )

def CustomPrompt(message, onAccept = None, onDecline = None, logger = Logger.Input):
    logger('\n\n' + message, end = ' ', attrs = [ 'bold' ])
    answer = input('[Y/n]: ')
    success = True

    if answer.lower() == 'y':
        if onAccept:
            success = onAccept()
        else:
            sys.exit()
    else:
        if onDecline:
            onDecline()

    return ( answer == 'y' and ( success or success == None ))

def ValuePrompt(message, required = False, logger = Logger.Input):
    if required:
        logger = Logger.Required

    logger(message, end = ' ', attrs = [ 'bold' ])
    answer = input()
    if required:
        while not answer:
            logger(message, end = ' ', attrs = [ 'bold' ])
            answer = input()

    return answer

def AddToPath(syspath):
    if not IsAdmin():
        return Logger.Failed("You have no permission to modify the path.")

    Logger.Info("Trying to add {} to path..".format(syspath), end = ' ')

    if not syspath in os.environ['PATH']:
        if sys.platform == "win32":
            path = os.pathsep + syspath
            oldpath = os.environ['PATH']
            Call('setx OLDPATH {}'.format(oldpath))
            Call('setx /M PATH "%PATH%;{}"'.format(path))
        return Logger.Success("OK")
    else:
        return Logger.Success("Path already defined, skipping")


def IsAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

def Call(cmd):
    try:
        return subprocess.call(cmd, shell = True)
    except Exception as e:
        Logger.Error("Command " + cmd + " not recognized " + str(e))
        return sys.exit()