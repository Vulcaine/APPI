import subprocess
import sys
import os
import ctypes

from logger import Logger
from configuration import config

def AssertCall(cmd):
    return Call(cmd) == 0

def Call(cmd):
    try:
        return subprocess.call(cmd, shell = True)
    except Exception as e:
        Logger.Error("Command " + cmd + " not recognized " + str(e))
        return sys.exit()

def IsAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

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

def InstallExe(exeName):
    return Call('start /wait {}'.format(exeName)) == 0

def DownloadTo(url, folder = "", outName = "output.exe"):
    conf = config.GetConfig()
    
    baseDownloadFolder = conf['temp-download-folder'] + folder
    downloadCommand = 'curl -o {0} "{1}"'.format(baseDownloadFolder + '/' + outName, url)
    
    Logger.Info("\nDownloading {0} to {1}".format(outName, baseDownloadFolder), end = ' ')

    Call('mkdir "{0}"'.format(baseDownloadFolder))
    
    return Call(downloadCommand) == 0

def DownloadAndInstallWindowsService(service, serviceName):
    conf = config.GetConfig()
    
    exeName = serviceName + '.exe'
    exePath = conf['temp-download-folder'] + '/' + serviceName + '/' + exeName
    
    if DownloadTo(service['url'], serviceName, exeName):
        Logger.Success("Download finished")
        Logger.Info("Installing {}.. Follow the instructions.".format(exeName), end = ' ')
    
        if InstallExe(exePath):
            return Logger.Success("Install finished")
        
        return Logger.Failed("Unexpected error during installation..")
    
    return Logger.Failed("Unexpected error during download..")

def InstallViaExecutable(service):
    conf = config.GetConfig()
    
    Logger.Info('Installing executable, follow the instructions..', end = ' ')
    if sys.platform == "linux" or sys.platform == "linux2":
        if not Call('sudo apt-get update'):
            raise Exception('Unexpected: Could not update apt')
        
        if not Call('sudo apt-get install {0}'.format(service)):
            raise Exception('Unexpected: Could not install service: ' + service)

        return Logger.Info(service + " package added", 'green', attrs = ['bold'])
    elif sys.platform == "darwin":
        return
    elif sys.platform == "win32":
        installpath = conf["install-root"] + '' + service
        installer = 'msiexec.exe /i'
        if service in conf['windows-service']:
            if conf['windows-service'][service]['strategy'] == 'msi':
                return Call('{0} "{1}" ^ INSTALLLOCATION="{2}" /qb'.format(installer, conf['windows-service'][service], installpath))
            return DownloadAndInstallWindowsService(conf['windows-service'][service], service)
    else:
        Logger.Error("Unsupported operating system")
        return sys.exit()

def Install(service, via, version = '@latest'):
    if via == 'npm':
        return NpmInstall(service + version, True)
    elif via == 'executable':
        return InstallViaExecutable(service)

def SpecialUbuntuInstall(installSteps):
    if sys.platform == 'linux2':
        for step in InstallSteps:
            Call(step)

def InstallMultiple(services, via):
    try:
        for service in services:
            Install(service, via)
    except Exception as e:
        Logger.Error('Unexpected exception in InstallMultiple')
        raise e
    
    return True

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

def InstallPrompt(serviceBundle, via = 'executable'):
    rootService = serviceBundle[0] # always pass root service as first argument and dependencies to rest
    message = "{0} not found. Would you like to install it now?".format(rootService)
    return CustomPrompt(
                    message,
                    lambda: InstallMultiple(serviceBundle, via),
                    lambda: sys.exit(),
                    Logger.Failed
                 )

def AddToPathPrompt(syspath):
    message = "Would you like to add {} to path?".format(syspath)
    
    return CustomPrompt(
                    message,
                    lambda: AddToPath(syspath)
                )

def IsCommandExists(command):
    return not Call('where {0} /Q'.format(command))

def IsNpmPackageInstalled(package):
    AssertNodeInstalled()
    
    return Call("npm list -g {0}".format(package))

def AssertNPMInstalled():
    Logger.Info("Checking npm install path..", end = ' ')
    if not IsCommandExists("npm"):
        InstallPrompt([ "npm" ])
    else:
        Logger.Success("OK")
        Logger.Info("Verifying latest version of NPM", end = ' ')
        
        Install("npm", "npm")
        
        Logger.Success("OK")

def AssertExpressInstalled():
    Logger.Info("Checking express install path..", end = ' ')
    if not IsCommandExists("express"):
        return InstallPrompt([ "express-generator" ], 'npm')
    else:
        return Logger.Success(" OK")

def AssertNodeInstalled():
    Logger.Info("Checking node install path..", end = ' '),
    if not IsCommandExists("node"):
        return InstallPrompt([ "nodejs", "npm" ])
    else:
        return Logger.Success("OK"),

def AssertMongoInstalled():
    Logger.Info("Checking mongodb install path..", end = ' '),
    if not ( IsCommandExists("mongo") or IsCommandExists("mongod") or IsCommandExists("mongos") ):
        return InstallPrompt([ "mongodb" ])
    else:
        return Logger.Success("OK");

def AssertDockerInstalled():
    Logger.Info("Checking docker install path..", end = ' '),
    if not ( IsCommandExists("docker") ):
        return InstallPrompt([ "docker" ])
    else:
        return Logger.Success("OK");

def AssertGitInstalled():
    Logger.Info("Checking git install path..", end = ' '),
    if not ( IsCommandExists("git") ):
        return InstallPrompt([ "git" ])
    else:
        return Logger.Success("OK");

def NpmInstall(package, isGlobal = False):
    command = "npm install {0} -g"
    if not isGlobal:
        command = "npm install {0}"
    
    return Call(command.format(package))

def CreateNgApp(appName):
    Logger.Info("Creating {} as an angular app..".format(appName))
    
    package = "@angular/cli"
    command = "ng new {}".format(appName)
    
    if not IsNpmPackageInstalled(package):
        Logger.Info("Angular was not found, installing..")
        NpmInstall(package, True)
    
    return Call(command)

def InitSimpleExpressApp(additionalSwitchesString = ''):
    rootCommand = "express"
    
    AssertNodeInstalled()
    AssertNPMInstalled()
    AssertExpressInstalled()
    
    Logger.Info("Initializing simple express app...")
    Call("{0} {1}".format(rootCommand, additionalSwitchesString))

# Example: 'appi add npm backend' gonna create a backend project
def InitNodejsBackend(additionalSwitchesString = '-y'):
    rootCommand = "npm"
    
    AssertNodeInstalled()
    AssertNPMInstalled()

    Logger.Info("Initializing node project...")
    Call("{0} init backend {1}".format(rootCommand, additionalSwitchesString))

def InstallMongoDB():
    conf = config.GetConfig()
    
    installdir = conf["install-root"] + 'mongodb'
    
    if not AssertMongoInstalled():
        if not AddToPathPrompt(installdir + '/bin'):
            Logger.Alert("Make sure to add this path to env")

    return Logger.Success("Mongo is installed in {0}.".format(installdir))

def RegisterGitRemote(remote):
    
    if AssertGitInstalled():
        if AssertCall("git remote add origin {}".format(remote)):
            Call("git remote -v")
            return Logger.Success("git setup complete on: {}".format(remote))
        else:
            return Logger.Failed("Could not add git remote: {}".format(remote))
    else:
        return Logger.Failed("Unexpected error during git installation.")
       

