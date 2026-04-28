# for implementing a folder of operations
import goose.registry as registry
import typer

# Create folder of operations sub goose for storing discovery operations
discover_operations = registry.goose_operations.create_subfolder("discover", description = "Invokes Football-Goose to search for user-defined operations, model definitions, and models")

# prints tree of accessible operations
# goose discover ops-tree
@discover_operations.operation("ops-tree", description = "Displays tree of all available operations")
def operations_tree():
    print(f"{50 * '-'}")
    print("Accessible operations:")
    registry.goose_operations.print_tree()
    print(f"{50 * '-'}")

# prints list of accessible models
# goose discover models
@discover_operations.operation("models", description = "Displays list of accessible models")
def models():
    registry.models_registry.display()

# prints list of accessible model definitions
# goose discover model-defs 
@discover_operations.operation("model-defs", description = "Displays list of accessible model definitions")
def model_defs():
    registry.model_definitions_registry.display()

# prints display of accesible data types and sources
@discover_operations.operation("data-types", description = "Displays all accessible data types and sources")
def data_types():
    registry.data_types_registry.display()

# prints all structures successfully discovered by goose
# goose discover all
@discover_operations.operation("all", description = "Displays all structures discovered by Football-Goose")
def all():
    operations_tree()
    models()
    model_defs()
    data_types()

# default goose discover to goose discover all
# goose discover
@discover_operations.typer_app.callback(invoke_without_command=True)
def discover_default(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        all()
