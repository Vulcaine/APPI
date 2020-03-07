from shell import InitSimpleExpressApp
from extenders import extenderhelpers as helper
from configuration import config

conf = config.GetConfig()

def Extend(args, Logger):
    switch = helper.GetSwitchFromArgs(args)
    InitSimpleExpressApp(switch)

    conf['features']['app'] = 'express'
    conf['app-type'] = 'simple-express-app'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ 'features': conf['features'] })

    return