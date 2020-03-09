from logger import Logger
from configuration import config

from . import installshell as ish
from . import assertshell as ash
from . import shellhelper as sh
from xmlparser.pombuilder import PomBuilder

def CreateNgApp(appName):
    Logger.Info("Creating {} as an angular app..".format(appName))

    package = "@angular/cli"
    command = "ng new {}".format(appName)

    if not ash.IsNpmPackageInstalled(package):
        Logger.Info("Angular was not found, installing..")
        ish.NpmInstall(package, True)

    return sh.Call(command)

def InitSimpleExpressApp(additionalSwitchesString = ''):
    rootCommand = "express"

    ash.AssertNodeInstalled()
    ash.AssertNPMInstalled()
    ash.AssertExpressInstalled()

    Logger.Info("Initializing simple express app...")
    sh.Call("{0} {1}".format(rootCommand, additionalSwitchesString))

# Example: 'appi add npm backend' gonna create a backend project
def InitNodejsBackend(additionalSwitchesString = '-y'):
    rootCommand = "npm"

    ash.AssertNodeInstalled()
    ash.AssertNPMInstalled()

    Logger.Info("Initializing node project...")
    sh.Call("{0} init backend {1}".format(rootCommand, additionalSwitchesString))

def InstallMongoDB():
    conf = config.GetConfig()

    installdir = conf["install-root"] + 'mongodb'

    if not ash.AssertMongoInstalled():
        if not sh.AddToPathPrompt(installdir + '/bin'):
            Logger.Alert("Make sure to add this path to env")

    return Logger.Success("Mongo is installed in {0}.".format(installdir))

def CreateSpringRootApp(projectRoot = None,
                        groupId = None,
                        artifactId = None,
                        packaging = None,
                        version = None,
                        name = None):
    if not projectRoot:
        projectRoot = sh.ValuePrompt("project root directory: ", required = True)
    if not groupId:
        groupId = sh.ValuePrompt("groupId: ", required = True)
    if not artifactId:
        artifactId = sh.ValuePrompt("artifactId: ") or "spring-parent"
    if not packaging:
        packaging = sh.ValuePrompt("packaging: ") or "pom"
    if not version:
        version = sh.ValuePrompt("version: ") or "1.0.0"
    if not name:
        name = sh.ValuePrompt("name: ") or "Parent Spring App"

    companyName = sh.ValuePrompt("company name: ")
    appFileName = sh.ValuePrompt("main class name: ")

    builder = PomBuilder()

    builder.SetArtifactId(artifactId)
    builder.SetGroupId(groupId)
    builder.SetPackaging(packaging)
    builder.SetVersion(version)
    builder.SetName(name)

    builder.AddPlugin(
        'org.apache.maven.plugins',
        'maven-compiler-plugin',
        {
            'source': '1.5',
            'target': '1.5'
        }
    )

    builder.AddDependency(
        'junit',
        'junit',
        '3.8.1',
        'test'
    )

    builder.AddModule('module-1')

    return companyName, projectRoot, builder.ToString(), appFileName
