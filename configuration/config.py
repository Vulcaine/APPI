
import json
import os
import sys
from logger             import Logger

config = {}

def GetScriptPath(filePath = __file__):
    absFilePath = os.path.abspath(filePath)
    path, filename = os.path.split(absFilePath)
    return path, filename

def GetRootPath():
    return GetScriptPath('../appi.py')

def GetRelativePath(path):
    return os.path.join(os.getcwd(), path)

def GetWorkDir():
    return os.getcwd()

def GetConfig():
    return config

def GetEntryPoint(appType):
    return config['entrypoints'][appType][sys.platform]

def WriteAppiConfig(conf):
        appiConfig = None

        with open(config['root-file'], 'r') as appiFile:
           appiConfig = json.load(appiFile)

        appiConfig = { **appiConfig, **conf }
        appiFile.close()

        with open(config['root-file'], 'w') as appiFile:
                appiFile.write(json.dumps(appiConfig, indent = 4, sort_keys = True))
                appiFile.close()

with open(GetScriptPath()[0] + '/config.jsonc', 'r') as outfile:
    config['features'] = {}
    config['features']['backend'] = {}
    config['features']['frontend'] = {}
    config['features']['database'] = {}

    config = json.load(outfile)

try:
    with open(os.getcwd() + '/appi.json', 'r') as outfile:
        config = {**config, **json.load(outfile)}

except:
    Logger.Warn('appi.json does not exists')
