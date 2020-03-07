from shell import CreateNgApp
from extenders import extenderhelpers as helper
from configuration import config

conf = config.GetConfig()

def Extend(args, Logger):

    CreateNgApp(args[1])

    conf['app-type'] = 'non-virtualized'
    conf['features']['frontend'] = 'angular'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

    return