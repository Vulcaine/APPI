def GetSwitchFromArgs(args):
    if len(args) > 0:
        return ''.join(args[1:])
    return ''