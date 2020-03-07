from . import GitHubExtender

def Extend(which, args, Logger):
    if which == 'github':
        return GitHubExtender.Extend(args, Logger)