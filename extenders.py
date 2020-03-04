import os.path

from configuration import config

from shell import InitNodejsBackend
from shell import InitSimpleExpressApp
from shell import InstallMongoDB
from shell import CreateNgApp
from shell import AssertDockerInstalled
from shell import RegisterGitRemote
#from shell import CreateDockerContainer

conf = config.GetConfig()

def GetSwitchFromArgs(args):
    if len(args) > 0:
        return ''.join(args[1:])
    return ''

class ExtenderFactory:
    @staticmethod
    def Extend(which, args, Logger):
        if which == 'github':
            return GitExtenderFactory.Extend('github', args, Logger)
        if which == 'gitlab':
            return GitExtenderFactory.Extend('gitlab', args, Logger)
        if which == 'bitbucket':
            return GitExtenderFactory.Extend('bitbucket', args, Logger)
        if which == 'nodejs':
            return NodeExtender.Extend(args, Logger)
        if which == 'angular':
            return AngularExtender.Extend(args, Logger)
        if which == 'mongodb':
            return MongoExtender.Extend(args, Logger)
        if which == 'express':
            return ExpressExtender.Extend(args, Logger)
        if which == 'docker':
            return DockerExtender.Extend(args, Logger)
    
    @staticmethod
    def Handler(which):
        if which == 'git':
            return HandlerFactory.Handler('git')

class HandlerFactory:
    @staticmethod
    def Handler(which):
        if which == 'git':
            return GitHandler

class GitHandler:
    @staticmethod
    def ToBranch(args):
        return
    
    @staticmethod
    def Status(args):
        return
    
    @staticmethod
    def Commit(args):
        return
    
    @staticmethod
    def Push(args):
        return
    
    @staticmethod
    def Pull(args):
        return
    
    @staticmethod
    def Diff(args):
        return

class GitExtenderFactory:
    @staticmethod
    def Extend(which, args, Logger):
        if which == 'github':
            return GitHubExtender.Extend(args, Logger)

class GitHubExtender:
    @staticmethod
    def Extend(args, Logger):
        if len(args) < 2:
            return Logger.Error("Missing parameters from git initialization")
        
        url = 'http://github.com'
        username = args[1]
        repo = args[2]
        
        remote = '{0}/{1}/{2}.git'.format(url, username, repo)

        return RegisterGitRemote(remote)

class NodeExtender:
    @staticmethod
    def Extend(args, Logger):
        switch = GetSwitchFromArgs(args)
        InitNodejsBackend(switch)
        
        conf['app-type'] = 'non-virtualized'
        conf['features']['backend'] = 'nodejs'
        
        config.WriteAppiConfig({ "app-type": conf['app-type'] })
        config.WriteAppiConfig({ "features": conf['features'] })
        
        return
        
class AngularExtender:
    @staticmethod
    def Extend(args, Logger):
        
        CreateNgApp(args[1])
        
        conf['app-type'] = 'non-virtualized'
        conf['features']['frontend'] = 'angular'
        
        config.WriteAppiConfig({ "app-type": conf['app-type'] })
        config.WriteAppiConfig({ "features": conf['features'] })
        
        return
    
class MongoExtender:
    @staticmethod
    def Extend(args, Logger):
        InstallMongoDB()
        
        conf['app-type'] = 'non-virtualized'
        conf['features']['database'] = 'mongodb'
        
        config.WriteAppiConfig({ "app-type": conf['app-type'] })
        config.WriteAppiConfig({ 'features': conf['features'] })
        
        return

class ExpressExtender:
    @staticmethod
    def Extend(args, Logger):
        switch = GetSwitchFromArgs(args)
        InitSimpleExpressApp(switch)
        
        conf['features']['app'] = 'express'
        conf['app-type'] = 'simple-express-app'
        
        config.WriteAppiConfig({ "app-type": conf['app-type'] })
        config.WriteAppiConfig({ 'features': conf['features'] })

        return

class DockerExtender:
    IMAGES = conf['docker-images']
    
    @staticmethod
    def Extend(args, Logger):
        containers = args[0].split(':')[1:]
        switch = GetSwitchFromArgs(args)

        AssertDockerInstalled()
        
        if not containers or len(containers) == 0:
            return Logger.Error("Error use of " + args + " please read the manual")

        for container in containers:
            if not container:
                return Logger.Error("Error use of " + args + " please read the manual")
            
            if not ( container in DockerExtender.IMAGES ):
                return Logger.Error(container + " is not supported image")
            
            Logger.Info("Creating docker initialization for: " + container)
            #CreateDockerContainer(container)
        
        conf['app-type'] = 'virtualized'
        conf['features']['virtualizer'] = 'docker'
        
        config.WriteAppiConfig({ "app-type": conf['app-type'] })
        config.WriteAppiConfig({ "fetures": conf['features'] })
        
        return