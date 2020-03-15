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
    SpringProjectRootDirName = 'spring-app'

    if len(args) == 1:
        groupId, rootDir, mainClassName, pomContent, modulePomContent = csh.CreateSpringRootApp()
    elif len(args) == 2:
        groupId, rootDir, mainClassName, pomContent, modulePomContent = csh.CreateSpringRootApp(
            args[1])

    conf['app-type'] = 'non-virtualized'

    src = 'src/main/java'
    resources = 'resources'

    srcPath = '{0}/{1}/{2}/{3}'.format(SpringProjectRootDirName, rootDir, src, groupId.replace(".", "/"))
    testPath = '{0}/{1}/src/test'.format(SpringProjectRootDirName, rootDir)
    resourcesPath = '{0}/{1}/{2}/{3}'.format(SpringProjectRootDirName, rootDir, src, resources)
    pomPath = '{0}/pom.xml'.format(SpringProjectRootDirName)
    modulePomPath = '{0}/{1}/pom.xml'.format(SpringProjectRootDirName, rootDir)
    springAppFileNamePath = '{0}/{1}.java'.format(srcPath, mainClassName)

    backendFeature = {
        'features':
        {
            'backend':
            {
                'type': 'spring-maven',
                'root-directory': SpringProjectRootDirName,
                'company-name': groupId,
                'modules': [
                    {
                        'root-directory': rootDir,
                        'src': src,
                        'resources': resources,
                    }
                ],
                'entrypoint': "cd {0} && {1}".format(SpringProjectRootDirName, conf['entrypoints']['spring-maven'][sys.platform])
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

    pomFile = open(modulePomPath, 'w')
    pomFile.write(modulePomContent)
    pomFile.close()

    # TODO: install maven for it
    # need solution to install latest
    Logger.Info('Installing maven wrapper..')
    mvnwVersion = sh.ValuePrompt("maven wrapper version (3.3.3): ") or "3.3.3"
    if not ash.AssertCall("cd {0} && mvn -N io.takari:maven:wrapper -Dmaven={1}".format(SpringProjectRootDirName, mvnwVersion)):
        Logger.Error("Error during maver wrapper installation")
        return sys.exit()

    conf.update(backendFeature)
    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

    Logger.Success("Spring app created on path: {}. Feel free to type `appi start`".format(
        SpringProjectRootDirName))

def ExtendModule(args):
    rootAppPath = config.GetRelativePath(conf['features']['backend']['root-directory'])

    mainClassName, groupId, moduleDir, pomContent, modulePomContent = csh.CreateSpringModule()

    src = 'src/main/java'
    resources = 'resources'

    srcPath = '{0}/{1}/{2}/{3}'.format(rootAppPath,
                                       moduleDir, src, groupId.replace(".", "/"))
    testPath = '{0}/{1}/src/test'.format(rootAppPath, moduleDir)
    resourcesPath = '{0}/{1}/{2}/{3}'.format(
        rootAppPath, moduleDir, src, resources)
    pomPath = '{0}/pom.xml'.format(rootAppPath)
    modulePomPath = '{0}/{1}/pom.xml'.format(rootAppPath, moduleDir)
    springAppFileNamePath = '{0}/{1}.java'.format(srcPath, mainClassName)

    moduleFeature =  {
        'root-directory': moduleDir,
        'src': src,
        'resources': resources,
    }

    os.makedirs(testPath, exist_ok=False)
    os.makedirs(srcPath, exist_ok=False)
    os.makedirs(resourcesPath, exist_ok=False)

    springMainContent = GenerateSpringMainClass(groupId, mainClassName)
    springAppFile = open(springAppFileNamePath, 'w')
    springAppFile.write(springMainContent)
    springAppFile.close()

    pomFile = open(pomPath, 'w')
    pomFile.write(pomContent)
    pomFile.close()

    pomFile = open(modulePomPath, 'w')
    pomFile.write(modulePomContent)
    pomFile.close()

    conf['features']['backend']['modules'].append(moduleFeature)
    config.WriteAppiConfig({"app-type": conf['app-type']})
    config.WriteAppiConfig({"features": conf['features']})

    return

def Extend(args, which):
    if which == 'spring-maven':
        return ExtendRootApp(args)
    else:
        return ExtendModule(args)


