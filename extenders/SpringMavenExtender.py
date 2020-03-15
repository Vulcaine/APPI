import os
import sys

from shell          import shellhelper as sh
from shell          import creatorshell as csh
from shell          import assertshell  as ash

from logger         import Logger

from configuration  import config

conf = config.GetConfig()

def GenerateSpringMainClass(groupId, mainClassName):
    package = groupId.replace('/', '.') + ';'
    importsArray = [
        'org.springframework.boot.autoconfigure.SpringBootApplication',
        'org.springframework.boot.SpringApplication'
    ]

    importString = ''
    for i in importsArray:
        importString += 'import {};\n'.format(i)

    annotations = '@SpringBootApplication'
    mainMethod = '\n\tpublic static void main ( String[] args ) {{\n\t\tSpringApplication.run({0}.class, args);\n\t}}'.format(mainClassName)
    mainClass = "package {0}\n\n{1}\n{2}\npublic class {3} {{\t{4}\n}}".format(package, importString, annotations, mainClassName, mainMethod)

    return mainClass

def ExtendRootApp(args):
    if len(args) == 1:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp()
    elif len(args) == 2:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1])
    elif len(args) == 3:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2])
    elif len(args) == 4:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3])
    elif len(args) == 5:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4])
    elif len(args) == 6:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4], args[5])
    elif len(args) == 7:
        groupId, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4], args[5], args[6])

    conf['app-type'] = 'non-virtualized'

    srcPath = '{0}/src/main/java/{1}'.format(rootDir, groupId.replace(".", "/"))
    testPath = '{0}/src/test'.format(rootDir)
    resourcesPath = '{0}/src/main/java/resources'.format(rootDir)
    pomPath = '{0}/pom.xml'.format(rootDir)
    springAppFileNamePath = '{0}/{1}.java'.format(srcPath, mainClassName)

    backendFeature = {
        'features':
        {
            'backend':
            {
                'type': 'spring-maven',
                'root-directory': rootDir,
                'src': srcPath,
                'resources': resourcesPath,
                'company-name': groupId,
                'modules': [],
                'entrypoint': "cd {0} && {1}".format(rootDir, conf['entrypoints']['spring-maven'][sys.platform])
            }
        }
    }

    os.makedirs( testPath, exist_ok = True )
    os.makedirs( srcPath, exist_ok = True )
    os.makedirs( resourcesPath, exist_ok = True )

    springMainContent = GenerateSpringMainClass(groupId, mainClassName)
    springAppFile = open(springAppFileNamePath, 'w')
    springAppFile.write(springMainContent)
    springAppFile.close()

    pomFile = open(pomPath, 'w')
    pomFile.write(pomContent)
    pomFile.close()

    # TODO: install maven for it
    # need solution to install latest
    Logger.Info('Installing maven wrapper..')
    mvnwVersion = sh.ValuePrompt("maven wrapper version (3.3.3): ") or "3.3.3"
    if not ash.AssertCall("cd {0} && mvn -N io.takari:maven:wrapper -Dmaven={1}".format(rootDir, mvnwVersion)):
        Logger.Error("Error during maver wrapper installation")
        return sys.exit()

    conf.update(backendFeature)
    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

def ExtendModule(args):
    return

def Extend(args, which):
    if which == 'spring-maven':
        return ExtendRootApp(args)
    else:
        return ExtendModule(args)


