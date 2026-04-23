# for discovering user-defined structures
from pathlib import Path
import sys
import importlib

# root = cwd = folder down from which goose discover will search into recursively deeper
global root
root = Path.cwd().resolve()

# discover_models() identifies all .fgm model files recursively deeper than cwd
def discover_models():
    # identify .fgm model files
    import goose.registry as registry
    for fgm in root.rglob('*.fgm'):
        if fgm.is_dir():
            model_name = fgm.stem 
            # store relative path to root
            registry.models[model_name] = fgm.relative_to(root)

# discover_structures() identifies all operations and model definitions recursively deeper than cwd
def discover_structures():
    # add root to sys.path
    sys.path.insert(0, str(root))
    # folders to ignore when discovering
    ignore_folders = [".git", "venv", ".venv", "__pycache__", "build", "dist"]
    # Grab and import every .py module recursively
    for py_file in root.rglob('*.py'):
        # ignore if ignorable file
        if any(ignored in py_file.parts for ignored in ignore_folders):
            continue
        # try to import module
        try:
            # absolute path of found .py file
            py_file_path = py_file.resolve()
            # Default module name to use = relative to root, the cwd
            module_name = ".".join(py_file.relative_to(root).with_suffix("").parts)
            # serach trough sys.path dictionary
            for name, module in list(sys.modules.items()):
                # aboslute path of given entry
                f = getattr(module, "__file__", None)
                # if py_file module has already been imported, adopt its existing name
                if f and Path(f).resolve() == py_file_path:
                    module_name = name
                    break
            # import via existing / new name
            importlib.import_module(module_name)
        # if import fails, print a fail message and move on
        except Exception as e:
            print(f"failed to import {str(module_name)}:")
            print(e)
            continue

# discover() allows Football-Goose to serach and identiy user-defined:
    # operations
    # models definitions
    # models
# Football-Goose will find all definitions starting from cwd and recursively deeper
def discover():
    # Discover goose's built-in operations
    import goose.operation.built_in_operations
    # discover operations + model definitions
    discover_structures()
    # discover .fgm model files
    discover_models()
        