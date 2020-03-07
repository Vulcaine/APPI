from shell import installshell as ish
from configuration import config
from logger import Logger

conf = config.GetConfig()

def Extend(args):
    ish.InstallMongoDB()

    conf['app-type'] = 'non-virtualized'
    conf['features']['database'] = 'mongodb'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ 'features': conf['features'] })

    return