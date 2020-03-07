from shell import RegisterGitRemote

def Extend(args, Logger):
    if len(args) < 2:
        return Logger.Error("Missing parameters from git initialization")

    url = 'http://github.com'
    username = args[1]
    repo = args[2]

    remote = '{0}/{1}/{2}.git'.format(url, username, repo)

    return RegisterGitRemote(remote)