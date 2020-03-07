from shell import shellhelper as sh
from shell import creatorshell as csh

from configuration import config

conf = config.GetConfig()

def Extend(args):
    if len(args) == 1:
        companyName, rootDir = csh.CreateSpringRootApp()
    elif len(args) == 2:
        companyName, rootDir = csh.CreateSpringBootRootApp(args[1])
    elif len(args) == 3:
        companyName, rootDir = csh.CreateSpringBootRootApp(args[1], args[2])
    elif len(args) == 4:
        companyName, rootDir = csh.CreateSpringBootRootApp(args[1], args[2], args[3])
    elif len(args) == 5:
        companyName, rootDir = csh.CreateSpringBootRootApp(args[1], args[2], args[3], args[4])
    elif len(args) == 6:
        companyName, rootDir =csh.CreateSpringBootRootApp(args[1], args[2], args[3], args[4], args[5])
    elif len(args) == 7:
        companyName, rootDir = csh.CreateSpringBootRootApp(args[1], args[2], args[3], args[4], args[5], args[6])

    conf['app-type'] = 'non-virtualized'
    backendFeature = {
        'features':
            {
                'backend':
                    {
                    'type': 'spring-maven',
                    'root-directory': rootDir,
                    'src': '{0}/src/main/java/{1}'.format(rootDir, companyName),
                    'resources': '{0}/resources'.format(rootDir),
                    'company-name': companyName,
                    'modules': []
                    }
            }

    }
    conf.update(backendFeature)

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })


