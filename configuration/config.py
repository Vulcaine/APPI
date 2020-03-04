
import json
import os

config = {}
with open(os.getcwd() + '/configuration/config.jsonc', 'r') as outfile:
        config = json.load(outfile)
config['features'] = {}

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