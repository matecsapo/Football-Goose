from typing import Callable, Dict, Any, Self
from typer import Typer
import sys

# Defines the data structure for storing an operation
    # Contains both a primary logic function defining the operation
    # Supports an optional wrapper function to invoke the primary function via CLI inputs + outputs
class Operation:
    def __init__(self, func: Callable, name : str, automatically_supports_cli : bool = False, description : str = None):
        self.name = name
        self.description = description
        # primary operation logic function
        self.func = func
        # whether primary logic function automatically supports cli interaction
        self.automatically_supports_cli = automatically_supports_cli
        # wrapper around primary logic func for cli input / output
        self.cli_wrapper_func = None

    # Executed when called directly in Python code
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    # Defines a function decorator to attach a custom CLI adapter
    def cli(self, cli_wrapper_func: Callable) -> Self:
        self.cli_wrapper_func = cli_wrapper_func
        return self

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
        self.operations: Dict[str, Operation] = {}
        # Here is your list of registries under this one!
        self.sub_folders: Dict[str, Self] = {}
        self.typer_app = Typer(help = description, add_completion=False)

    # Defines a function decorator for attaching a function to a given operation folder
    # @[operation_folder].operation(name, description)
    def operation(self, name : str, automatically_supports_cli : bool = False, description : str = None):
        def decorator(func: Callable) -> Operation:
            op = Operation(func, name, automatically_supports_cli, description)
            self.operations[name] = op
            return op
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
        cli_icon = "💻"  # Symbol indicating CLI support
        pipe = "│   "
        branch = "├── "
        last_branch = "└── "
        # print operation folder tag
        prefix = (pipe * (indent_level - 1) + branch) if indent_level > 0 else ""
        print(f"{prefix}{folder_icon} {self.name}/")
        # Get a list of all items to print to handle the "last" item differently
        ops = list(self.operations.values())
        subs = list(self.sub_folders.values())
        total_items = len(ops) + len(subs)
        # print all operations
        for i, op in enumerate(ops):
            is_last = (i == total_items - 1)
            supports_cli = (op.cli_wrapper_func is not None) or op.automatically_supports_cli
            cli_badge = f"{cli_icon}" if supports_cli else ""
            current_prefix = pipe * indent_level + (last_branch if is_last else branch)
            print(f"{current_prefix}{op_icon} {op.name} {cli_badge}")
        # print all sub operation folders
        for i, subfolder in enumerate(subs):
            subfolder.print_tree(indent_level + 1)

