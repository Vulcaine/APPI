from .                  import shellhelper      as sh
from .                  import assertshell      as assertsh
from .                  import installshell     as installsh

from configuration      import config
from logger             import Logger

def InstallMultiple(services, via):
    try:
        for service in services:
            Install(service, via)
    except Exception as e:
        Logger.Error('Unexpected exception in InstallMultiple')
        raise e

    return True

def InstallExe(exeName):
    return assertsh.AssertCall('start /wait {}'.format(exeName))

def DownloadTo(url, folder = "", outName = "output.exe"):
    conf = config.GetConfig()

    baseDownloadFolder = conf['temp-download-folder'] + folder
    downloadCommand = 'curl -o {0} "{1}"'.format(baseDownloadFolder + '/' + outName, url)

    Logger.Info("\nDownloading {0} to {1}".format(outName, baseDownloadFolder), end = ' ')

    sh.Call('mkdir "{0}"'.format(baseDownloadFolder))

    return assertsh.AssertCall(downloadCommand)

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
        if not assertsh.AssertCall('sudo apt-get update'):
            raise Exception('Unexpected: Could not update apt')

        if not assertsh.AssertCall('sudo apt-get install {0}'.format(service)):
            raise Exception('Unexpected: Could not install service: ' + service)

        return Logger.Info(service + " package added", 'green', attrs = ['bold'])
    elif sys.platform == "darwin":
        return
    elif sys.platform == "win32":
        installpath = conf["install-root"] + '' + service
        installer = 'msiexec.exe /i'
        if service in conf['windows-service']:
            if conf['windows-service'][service]['strategy'] == 'msi':
                return assertsh.AssertCall('{0} "{1}" ^ INSTALLLOCATION="{2}" /qb'.format(installer, conf['windows-service'][service], installpath))
            return DownloadAndInstallWindowsService(conf['windows-service'][service], service)
    else:
        Logger.Error("Unsupported operating system")
        return sys.exit()

def Install(service, via, version = '@latest'):
    if via == 'npm':
        return NpmInstall(service + version, True)
    elif via == 'executable':
        return InstallViaExecutable(service)

def NpmInstall(package, isGlobal = False):
    command = "npm install {0} -g"
    if not isGlobal:
        command = "npm install {0}"

    return assertsh.AssertCall(command.format(package))

def SpecialUbuntuInstall(installSteps = []):
    if sys.platform == 'linux2':
        for step in installSteps:
            sh.Call(step)

def InstallPrompt(serviceBundle, via = 'executable'):
    rootService = serviceBundle[0] # always pass root service as first argument and dependencies to rest
    message = "{0} not found. Would you like to install it now?".format(rootService)
    return assertsh.CustomPrompt(
                    message,
                    lambda: installsh.InstallMultiple(serviceBundle, via),
                    lambda: sys.exit(),
                    Logger.Failed
                 )
