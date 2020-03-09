import os

from shell          import shellhelper as sh
from shell          import creatorshell as csh

from configuration  import config

conf = config.GetConfig()

def GenerateSpringMainClass(srcPath, mainClassName):
    package = srcPath.replace('/', '.') + ';';
    annotations = '@Configuration\n@EnableAutoConfiguration'
    mainMethod = '\n\tpublic static void main ( String[] args ) {{\n\t\tSpringApplication.run({0}.class, args);\n\t}}'.format(mainClassName)
    mainClass = "package {0}\n\n{1}\npublic class {2} {{\t{3}\n}}".format(package, annotations, mainClassName, mainMethod)

    return mainClass

def ExtendRootApp(args):
    if len(args) == 1:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp()
    elif len(args) == 2:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1])
    elif len(args) == 3:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2])
    elif len(args) == 4:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3])
    elif len(args) == 5:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4])
    elif len(args) == 6:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4], args[5])
    elif len(args) == 7:
        companyName, rootDir, pomContent, mainClassName = csh.CreateSpringRootApp(args[1], args[2], args[3], args[4], args[5], args[6])

    conf['app-type'] = 'non-virtualized'

    srcPath = '{0}/src/main/java/{1}'.format(rootDir, companyName)
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
                'company-name': companyName,
                'modules': [],
            }
        }
    }

    os.makedirs( testPath, exist_ok = True )
    os.makedirs( srcPath, exist_ok = True )
    os.makedirs( resourcesPath, exist_ok = True )

    springMainContent = GenerateSpringMainClass(srcPath, mainClassName)
    springAppFile = open(springAppFileNamePath, 'w')
    springAppFile.write(springMainContent)
    springAppFile.close()

    pomFile = open(pomPath, 'w')
    pomFile.write(pomContent)
    pomFile.close()

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


