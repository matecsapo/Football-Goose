from typing import Callable, Dict
from typer import Typer
import sys

# Defines the data structure for storing a folder of operations
class Operations_Folder:
    # every operation folder has a:
        # name - which doubles as its typer CLI app identifier
        # description - which doubles as its typer CLI help identifier
        # operations - set of operations in the folder
        # sub_folders - sub_folders stemming from this operations folder
        # typer_app - the typer CLI app implementing this operations folder
    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description
        self.operations: Dict[str, tuple] = {}
        # Here is your list of registries under this one!
        self.sub_folders: Dict[str, 'Operations_Folder'] = {}
        self.typer_app = Typer(help = description, add_completion=False)

    # Defines a function decorator for attaching a function to a given operation folder
    # @[operation_folder].operation(name, description)
    def operation(self, name : str, description : str = None):
        def decorator(func: Callable):
            self.operations[name] = (func, description)
            return func
        return decorator

    # Defines a factory method for creating a subfolder of a given folder
    # [operation_folder].create_subfolder(name, description)
    def create_subfolder(self, name : str, description : str = None):
        # Create subfolder
        sub_folder = Operations_Folder(name, description)
        folder_name = f"{name}_operations"
        # store subfolder in registry
        setattr(sys.modules.get('goose.registry'), folder_name, sub_folder)
        # set subfolder as child of this folder
        self.sub_folders[name] = getattr(sys.modules.get('goose.registry'), folder_name)
        # return subfolder Operations_Folder object to interact with it
        return self.sub_folders[name]
    
    # prints operation tree to terminal showcasing all available operations
    def print_tree(self, indent_level : int = 0, indent_size : int = 4):
        # Branch symbols
        folder_icon = "📂"
        op_icon = "⚙️"
        pipe = "│   "
        branch = "├── "
        last_branch = "└── "
        # print operation folder tag
        prefix = (pipe * (indent_level - 1) + branch) if indent_level > 0 else ""
        print(f"{prefix}{folder_icon} {self.name}/")
        # Get a list of all items to print to handle the "last" item differently
        ops = list(self.operations.keys())
        subs = list(self.sub_folders.values())
        total_items = len(ops) + len(subs)
        # print all operations
        for i, name in enumerate(ops):
            is_last = (i == total_items - 1)
            current_prefix = pipe * indent_level + (last_branch if is_last else branch)
            print(f"{current_prefix}{op_icon} {name}")
        # print all sub operation folders
        for i, subfolder in enumerate(subs):
            subfolder.print_tree(indent_level + 1)

