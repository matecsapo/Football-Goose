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
    print(f"{50 * '-'}")
    print(f"Accessible models ({len(registry.models)}):")
    for model_name, fgm_path in registry.models.items():
        print(f"🧠 {model_name:^30} | ➔  {fgm_path}")
    print(f"{50 * '-'}")

# prints list of accessible model definitions
# goose discover model-defs 
@discover_operations.operation("model-defs", description = "Displays list of accessible model definitions")
def model_defs():
    print(f"{50 * '-'}")
    print(f"Accesible model definitions ({len(registry.model_definitions)}):")
    for name, (cls, description) in registry.model_definitions.items():
        print(f"📍 {name:^30} | {f'[ {cls.__name__} ]':^30} ➔  {description}")
    print(f"{50 * '-'}")

# prints all structures successfully discovered by goose
# goose discover all
@discover_operations.operation("all", description = "Displays all structures discovered by Football-Goose")
def all():
    operations_tree()
    models()
    model_defs()

# default goose discover to goose discover all
# goose discover
@discover_operations.typer_app.callback(invoke_without_command=True)
def discover_default(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        all()
