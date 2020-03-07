from . import assertshell as assertsh
from . import shellhelper as sh

from logger import Logger

def GitListBranch(args):
    return assertsh.AssertCall("git branch -r")

def GitStatus(args):
    return assertsh.AssertCall("git status")

def RegisterGitRemote(remote):

    if assertsh.AssertGitInstalled():
        if assertsh.AssertCall("git remote add origin {}".format(remote)):
            sh.Call("git remote -v")
            return Logger.Success("git setup complete on: {}".format(remote))
        else:
            return Logger.Failed("Could not add git remote: {}".format(remote))
    else:
        return Logger.Failed("Unexpected error during git installation.")
