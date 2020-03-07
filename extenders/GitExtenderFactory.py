from . import GitHubExtender
from logger import Logger

def Extend(which, args):
    if which == 'github':
        return GitHubExtender.Extend(args)