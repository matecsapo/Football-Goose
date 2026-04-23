# for invoking goose's discovery
from goose.discover import discover

# for accessing root typer app
import goose.registry as registry
from goose.operation.operations_folder import Operations_Folder

# Links up typer CLI objects of all operations folders from tree of operations
def Link_Typer_Tree(folder : Operations_Folder):
    # add operations belonging to this folder
    for name, (func, help_text) in folder.operations.items():
        folder.typer_app.command(name = name, help = help_text)(func)

    # recursively add subfolders stemming from this folder
    for sub_folder_name, sub_folder in folder.sub_folders.items():
        # recursively links up subfolders typer app's tree
        Link_Typer_Tree(sub_folder)
        # add subfolder typer app as sub-app of this folder's app
        folder.typer_app.add_typer(sub_folder.typer_app, name = sub_folder_name)

# goose_cli.py is the entry point for the goose... cli commands
def Goose_CLI():
    # run goose's discovery
    discover()
    # Link up all operation folders' typer apps
    Link_Typer_Tree(registry.goose_operations)
    # launch root typer app
    registry.goose_operations.typer_app()