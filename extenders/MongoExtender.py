from shell import InstallMongoDB
from configuration import config

conf = config.GetConfig()

def Extend(args, Logger):
    InstallMongoDB()

    conf['app-type'] = 'non-virtualized'
    conf['features']['database'] = 'mongodb'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ 'features': conf['features'] })

    return