import os.path
import sys
import json

from configuration import config

from extenders import ExtenderFactory as EF

from logger    import Logger
from shell     import CustomPrompt

class CLIParser:
    def __init__(self, cml):
        self.rootFile = None
        self.commandLine = cml
        self.cmCursor = 0
        
        self.conf = config.GetConfig()
        self.rootFileName = self.conf['root-file']
        self.repoConfig = {}

        self.version = self.conf['version']
        self.OPTIONS = self.conf['cli-options']
        self.ADD_OPTIONS = self.conf['cli-add-options']
        
    def GetCMDOptions(self):
        if len(self.commandLine) <= self.cmCursor:
            return sys.exit()

        options = [ self.commandLine[self.cmCursor] ]
        tempCursor = self.cmCursor + 1

        while(
                len(self.commandLine) > tempCursor and (
                not ( self.commandLine[tempCursor] in self.OPTIONS ) 
                and
                not ( self.commandLine[tempCursor] in self.ADD_OPTIONS )
                and
                not ':' in self.commandLine[tempCursor]
                or
                '-' in self.commandLine[tempCursor][0]
                )
                
            ):
            options.append(self.commandLine[tempCursor])
            tempCursor += 1
            self.cmCursor += 1
        
        return options

    def OpenRepository(self):
        self.rootFile = open(self.rootFileName, "r+")
        repoConfig = json.load(self.rootFile)
        
        if 'app-type' in repoConfig:
            self.conf['app-type'] = repoConfig['app-type']
        
        if 'version' in repoConfig:
            self.conf['version'] = repoConfig['version']
        
        self.rootFile.close()
    
    def CreateRepository(self):
        self.rootFile = open(self.rootFileName, "w+")
        self.rootFile.write(json.dumps({ "version": self.conf['version'] }))
        self.rootFile.close()
        
        return True
    
    def IsValidAppiRepository(self):
        if os.path.isfile('./' + self.rootFileName):
            return True
        return False

    def ValidateRepository(self, callback, args):
        if not self.IsValidAppiRepository():
            Logger.Error("This is not a valid APPI repository")
            answer = CustomPrompt(
                                    "Would you like to create it? ",
                                    lambda: self.CreateRepository(),
                                    lambda: sys.exit()
                                )
            if answer:
                callback(args)
        else:
            self.OpenRepository()
            callback(args)

    def GitBranch(self, args):
        return EF.Handler('git').ToBranch(args)

    def GitHubSetup(self, args):
        return EF.Extend('github', args, Logger)
    
    def Start(self, args):
        return
    
    def Version(self, args):
        Logger.Info('Current version: ' + self.version)    
    
    def InitSimpleExpressApp(self, args):
        if self.conf['app-type'] == 'virtualized' or self.conf['app-type'] == 'simple-express-app':
            return Logger.Error("This is already an {0} based repo, can't add this feature".format(self.conf['app-type']))
        
        return EF.Extend('express', args, Logger)
    
    def Init(self, args):
        if self.IsValidAppiRepository():
            Logger.Error("It is already an APPI repository try adding features with --add")
        else:
            Logger.Info("New appi repository created, you can add features with --add")
        
        self.CreateRepository()
        self.Process()

    def Add(self, args):
        self.cmCursor += 1

        cmdOptions = self.GetCMDOptions()

        for k, option in self.ADD_OPTIONS.items():
            if k in cmdOptions[0] or cmdOptions[0] in self.ADD_OPTIONS[k]['aliases']:
                eval( self.ADD_OPTIONS[k]['function'], {"self": self} )(cmdOptions)
                return self.Add(cmdOptions)

        self.cmCursor -= 1
        self.Process()

    # TODO: Beletenni appi.json fájlba hogy milyen komponenseket adtunk hozzá
    # azzal eldönteni hogy lehet-e hozzáadni, nem az app-type alapján
    def AddNodeJS(self, args):
        if self.conf['app-type'] == 'virtualized':
            return Logger.Error("This is already an {0} based repo, can't add this feature".format(self.conf['app-type']))
        
        if 'backend' in self.conf['features'] and self.conf['features']['backend'] == 'nodejs':
            return Logger.Error("Feature nodejs already in this repo")
        
        return EF.Extend('nodejs', args, Logger)
    
    def AddAngular(self, args):
        if self.conf['app-type'] == 'virtualized':
            return Logger.Error("This is already an {0} based repo, can't add this feature".format(self.conf['app-type']))
        
        if 'frontend' in self.conf['features'] and self.conf['features']['frontend'] == 'angular':
            return Logger.Error("Feature angular already in this repo")

        return EF.Extend('angular', args, Logger)
    
    def AddMongoDB(self, args):
        if self.conf['app-type'] == 'virtualized':
            return Logger.Error("This is already an {0} based repo, can't add this feature".format(self.conf['app-type']))
        
        if 'database' in self.conf['features'] and self.conf['features']['database'] == 'mongodb':
            return Logger.Error("Feature mongodb already in this repo")

        return EF.Extend('mongodb', args, Logger)
        
    def AddDocker(self, args):
        if self.conf['app-type'] == 'non-virtualized':
            return Logger.Error("This is already an {0} based repo, can't add this feature".format(self.conf['app-type']))
        
        return EF.Extend('docker', args, Logger)
    
    def Process(self):
        self.cmCursor += 1
        
        if len(self.commandLine) == 1:
            return Logger.Error("You have to specify options")

        cmdOptions = self.GetCMDOptions()
        for k, option in self.OPTIONS.items():
            if k in cmdOptions[0] or cmdOptions[0] in self.OPTIONS[k]['aliases']:
                return eval( self.OPTIONS[k]['function'], {"self": self} )(cmdOptions)
        
        return Logger.Error("Wrong usage of cli")