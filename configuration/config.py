
import json
import os
from logger             import Logger

config = {}

with open(os.getcwd() + '/configuration/config.jsonc', 'r') as outfile:
        config['features'] = {}
        config['features']['backend'] = {}
        config['features']['frontend'] = {}
        config['features']['database'] = {}

        config = json.load(outfile)

try:
        with open(os.getcwd() + '/appi.json', 'r') as outfile:
                config = { **config, **json.load(outfile) }

except:
        Logger.Warn('appi.json does not exists')

def GetConfig():
    return config

def WriteAppiConfig(conf):
        appiConfig = None

        with open(config['root-file'], 'r') as appiFile:
           appiConfig = json.load(appiFile)

        appiConfig = { **appiConfig, **conf }
        appiFile.close()

        with open(config['root-file'], 'w') as appiFile:
                appiFile.write(json.dumps(appiConfig))
                appiFile.close()