from shell import creatorshell as csh
from extenders import extenderhelpers as helper
from configuration import config
from logger import Logger

conf = config.GetConfig()

def Extend(args):
    switch = helper.GetSwitchFromArgs(args)
    csh.InitSimpleExpressApp(switch)

    conf['features']['app'] = 'express'
    conf['app-type'] = 'simple-express-app'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ 'features': conf['features'] })

    return