from shell import InitNodejsBackend
from extenders import extenderhelpers as helper
from configuration import config

conf = config.GetConfig()

def Extend(args, Logger):
    switch = helper.GetSwitchFromArgs(args)
    InitNodejsBackend(switch)

    conf['app-type'] = 'non-virtualized'
    conf['features']['backend'] = 'nodejs'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

    return