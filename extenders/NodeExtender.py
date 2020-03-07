from shell import shellhelper as sh
from extenders import extenderhelpers as helper
from configuration import config
from logger import Logger

conf = config.GetConfig()

def Extend(args):
    switch = helper.GetSwitchFromArgs(args)
    sh.InitNodejsBackend(switch)

    conf['app-type'] = 'non-virtualized'
    conf['features']['backend'] = { 'type': 'nodejs', 'modules': [] }

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

    return