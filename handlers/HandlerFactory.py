from .          import GitHandler

def Handler(which):
    if which == 'git':
        return GitHandler