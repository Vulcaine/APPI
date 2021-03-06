from shell              import assertshell          as ash
from extenders          import extenderhelpers      as helper
from configuration      import config
from logger             import Logger

conf = config.GetConfig()

IMAGES = conf['docker-images']

def Extend(args):
    containers = args[0].split(':')[1:]
    switch = helper.GetSwitchFromArgs(args)

    ash.AssertDockerInstalled()

    if not containers or len(containers) == 0:
        return Logger.Error("Error use of " + args + " please read the manual")

    for container in containers:
        if not container:
            return Logger.Error("Error use of " + args + " please read the manual")

        if not ( container in IMAGES ):
            return Logger.Error(container + " is not supported image")

        Logger.Info("Creating docker initialization for: " + container)
        #CreateDockerContainer(container)

    conf['app-type'] = 'virtualized'
    conf['features']['virtualizer'] = 'docker'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "fetures": conf['features'] })

    return