from logger             import Logger
from .                  import installshell         as installhelper
from .                  import assertshell          as asserter
from .                  import shellhelper          as sh

def AssertCall(cmd):
    return sh.Call(cmd) == 0

def IsNpmPackageInstalled(package):
    AssertNodeInstalled()

    return sh.Call("npm list -g {0}".format(package))

def IsCommandExists(command):
    return not sh.Call('where {0} /Q'.format(command))

def AssertNPMInstalled():
    Logger.Info("Checking npm install path..", end = ' ')
    if not asserter.IsCommandExists("npm"):
        installhelper.InstallPrompt([ "npm" ])
    else:
        Logger.Success("OK")
        Logger.Info("Verifying latest version of NPM", end = ' ')

        installhelper.Install("npm", "npm")

        Logger.Success("OK")

def AssertExpressInstalled():
    Logger.Info("Checking express install path..", end = ' ')
    if not asserter.IsCommandExists("express"):
        return installhelper.InstallPrompt([ "express-generator" ], 'npm')
    else:
        return Logger.Success(" OK")

def AssertNodeInstalled():
    Logger.Info("Checking node install path..", end = ' '),
    if not asserter.IsCommandExists("node"):
        return installhelper.InstallPrompt([ "nodejs", "npm" ])
    else:
        return Logger.Success("OK"),

def AssertMongoInstalled():
    Logger.Info("Checking mongodb install path..", end = ' '),
    if not ( asserter.IsCommandExists("mongo") or asserter.IsCommandExists("mongod") or asserter.IsCommandExists("mongos") ):
        return installhelper.InstallPrompt([ "mongodb" ])
    else:
        return Logger.Success("OK");

def AssertDockerInstalled():
    Logger.Info("Checking docker install path..", end = ' '),
    if not ( asserter.IsCommandExists("docker") ):
        return installhelper.InstallPrompt([ "docker" ])
    else:
        return Logger.Success("OK");

def AssertGitInstalled():
    Logger.Info("Checking git install path..", end = ' '),
    if not ( asserter.IsCommandExists("git") ):
        return installhelper.InstallPrompt([ "git" ])
    else:
        return Logger.Success("OK");