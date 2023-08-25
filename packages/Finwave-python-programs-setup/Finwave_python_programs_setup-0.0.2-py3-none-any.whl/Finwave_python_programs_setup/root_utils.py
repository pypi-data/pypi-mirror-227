import sys
import pathlib

def get_root_folder(path, root_folder="Python_Programs"):
    parents = pathlib.Path(path).parents
    root_folders = [parent for parent in parents if parent.name == root_folder]
    if len(root_folders) >= 2:
        raise RootFolderError(f"Found multiple instances of '{root_folder}' in '{path}'")
    elif len(root_folders) == 0:
        raise RootFolderError(f"Root Folder '{root_folder}' not in path '{path}'")
    else:
        return root_folders[0]

def add_root_to_path(path, root_folder="Python_Programs"):
    root = get_root_folder(path, root_folder)
    sys.path.append(str(root))
    return root

class RootFolderError(Exception):
    '''
    Raised when a measurement range is not supported by a device.
    '''
    pass

