# registry.py stores all the recursive operation folders defining all operations
# goose_operations is the root operation folder
# all recursive sub-folders are added dynamically to this module when the goose CLI is run
from goose.operation.operations_folder import Operations_Folder

# root operations folder
global goose_operations
goose_operations = Operations_Folder("goose", "Football-Goose")

# dictionary of model definitions
global model_definitions 
model_definitions = {} # name --> (class, description)

# list of models
global models
models = {} # model_name --> .fgm folder path
