import os
import sys

#fast forward the import of the module toward the proper path

#the root folder
cwd = os.path.join(os.path.dirname(__file__), 'src')
if cwd not in sys.path:
    sys.path.append(cwd)


def main(*args, **kwargs):
    import studiolibrary
    studiolibrary.main(*args, **kwargs)

def reload():
    import studiolibrary
    studiolibrary.reload()
