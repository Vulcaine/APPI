from configuration import config
from . import GitExtenderFactory
from . import NodeExtender
from . import AngularExtender
from . import MongoExtender
from . import ExpressExtender
from . import DockerExtender
from . import SpringMavenExtender
from handlers import HandlerFactory
from logger import Logger


def Extend(which, args):
    if which == 'github':
        return GitExtenderFactory.Extend('github', args)
    if which == 'gitlab':
        return GitExtenderFactory.Extend('gitlab', args)
    if which == 'bitbucket':
        return GitExtenderFactory.Extend('bitbucket', args)
    if which == 'nodejs':
        return NodeExtender.Extend(args)
    if which == 'angular':
        return AngularExtender.Extend(args)
    if which == 'mongodb':
        return MongoExtender.Extend(args)
    if which == 'express':
        return ExpressExtender.Extend(args)
    if which == 'docker':
        return DockerExtender.Extend(args)
    if which == 'spring-maven':
        return SpringMavenExtender.Extend(args, which)
    if which == 'spring-maven-module':
        return SpringMavenExtender.Extend(args, which)

def Handler(which):
    if which == 'git':
        return HandlerFactory.Handler('git')