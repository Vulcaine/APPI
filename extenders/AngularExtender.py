from shell          import creatorshell         as csh
from extenders      import extenderhelpers      as helper
from configuration  import config
from logger         import Logger

conf = config.GetConfig()

def Extend(args):

    csh.CreateNgApp(args[1])

    conf['app-type'] = 'non-virtualized'
    conf['features']['frontend'] = 'angular'

    config.WriteAppiConfig({ "app-type": conf['app-type'] })
    config.WriteAppiConfig({ "features": conf['features'] })

    return