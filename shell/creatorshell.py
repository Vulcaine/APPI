import os

from logger                 import Logger
from configuration          import config

from .                      import installshell     as ish
from .                      import assertshell      as ash
from .                      import shellhelper      as sh
from xmlparser.pombuilder   import PomBuilder

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

def CreateSpringModule():
    conf = config.GetConfig()

    pomRoot = config.GetRelativePath(conf['features']['backend']['root-directory'])
    rootPomBuilder = PomBuilder.Parse(os.path.join(pomRoot, 'pom.xml'))

    projectRoot = sh.ValuePrompt("module directory: ", required = True)
    groupId = sh.ValuePrompt(
        "company package (com.mycompany): ") or "com.mycompany"
    artifactId = sh.ValuePrompt(
        "module name (spring-boot): ") or "spring-boot"
    packaging = sh.ValuePrompt("packaging (jar): ") or "jar"
    name = sh.ValuePrompt("name (Parent Spring App): ") or "Parent Spring App"
    appFileName = sh.ValuePrompt("main class name (Main): ") or "SpringMain"
    javaVersion = sh.ValuePrompt("Java version (1.8): ") or "1.8"

    modulePomBuilder = PomBuilder()
    rootPomBuilder.AddModule(artifactId)

    modulePomBuilder.SetArtifactId(artifactId)
    modulePomBuilder.SetGroupId(groupId)
    modulePomBuilder.SetName(name)
    modulePomBuilder.SetPackaging(packaging)

    modulePomBuilder.AddProperty(
        'java.version',
        javaVersion
    )

    modulePomBuilder.AddParent(
        'org.springframework.boot',
        'spring-boot-starter-parent',
        '2.2.5.RELEASE',
        True
    )

    modulePomBuilder.AddPlugin(
        'org.apache.maven.plugins',
        'maven-compiler-plugin',
        {
            'source': '1.6',
            'target': '1.6'
        }
    )

    modulePomBuilder.AddPlugin(
        'org.springframework.boot',
        'spring-boot-maven-plugin'
    )

    modulePomBuilder.AddDependency(
        'org.springframework.boot',
        'spring-boot-starter-web',
        '2.2.5.RELEASE',
    )

    modulePomBuilder.AddDependency(
        'junit',
        'junit',
        '3.8.1',
        'test'
    )

    return appFileName, groupId, projectRoot, rootPomBuilder.ToString(), modulePomBuilder.ToString()

def CreateSpringRootApp(isDefault = None):

    if isDefault == '-d':
        projectRoot = sh.ValuePrompt("project root directory: ", required = True)
        groupId = "com.mycompany"
        artifactId = "spring-boot"
        packaging = "pom"
        version = "1.0-SNAPSHOT"
        name = "Parent Spring App"
        appFileName = "SpringMain"
        javaVersion = "1.8"
    else:
        projectRoot = sh.ValuePrompt("project root directory: ", required = True)
        groupId = sh.ValuePrompt(
            "company package (com.mycompany): ") or "com.mycompany"
        artifactId = sh.ValuePrompt("project name (spring-boot): ") or "spring-boot"
        packaging = sh.ValuePrompt("packaging (jar): ") or "jar"
        version = sh.ValuePrompt("version (1.0-SNAPSHOT): ") or "1.0-SNAPSHOT"
        name = sh.ValuePrompt("name (Parent Spring App): ") or "Parent Spring App"
        appFileName = sh.ValuePrompt("main class name (Main): ") or "SpringMain"
        javaVersion = sh.ValuePrompt("Java version (1.8): ") or "1.8"

    rootPomBuilder = PomBuilder()
    modulePomBuilder = PomBuilder()

    rootPomBuilder.SetArtifactId('spring-parent')
    rootPomBuilder.SetGroupId(groupId)
    rootPomBuilder.SetVersion(version)
    rootPomBuilder.SetPackaging('pom')
    rootPomBuilder.SetName('Parent Spring App')

    rootPomBuilder.AddModule(projectRoot)

    modulePomBuilder.SetArtifactId(artifactId)
    modulePomBuilder.SetGroupId(groupId + '.' + projectRoot)
    modulePomBuilder.SetPackaging(packaging)
    modulePomBuilder.SetName(name)

    modulePomBuilder.AddProperty(
        'java.version',
        javaVersion
    )

    modulePomBuilder.AddParent(
        'org.springframework.boot',
        'spring-boot-starter-parent',
        '2.2.5.RELEASE',
        True
    )

    modulePomBuilder.AddPlugin(
        'org.apache.maven.plugins',
        'maven-compiler-plugin',
        {
            'source': '1.6',
            'target': '1.6'
        }
    )

    modulePomBuilder.AddPlugin(
        'org.springframework.boot',
        'spring-boot-maven-plugin'
    )

    modulePomBuilder.AddDependency(
        'org.springframework.boot',
        'spring-boot-starter-web',
        '2.2.5.RELEASE',
    )

    modulePomBuilder.AddDependency(
        'junit',
        'junit',
        '3.8.1',
        'test'
    )

    '''
    modulePomBuilder.AddDependencyManagementDependency(
        'org.springframework.boot',
        'spring-boot-dependencies',
        'pom',
        '2.0.2.RELEASE',
        'import'
    )
    '''

    return groupId, projectRoot, appFileName, rootPomBuilder.ToString(), modulePomBuilder.ToString()
