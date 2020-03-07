from configuration import config
from . import GitExtenderFactory
from . import NodeExtender
from . import AngularExtender
from . import MongoExtender
from . import ExpressExtender
from . import DockerExtender
from handlers import HandlerFactory


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

def Handler(which):
    if which == 'git':
        return HandlerFactory.Handler('git')