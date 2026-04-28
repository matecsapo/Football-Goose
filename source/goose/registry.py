# registry.py stores registries of:
    # operations
    # models
    # model definitions
    # data types


# for implementing operations registry
from goose.operation.operations_folder import Operations_Folder

# for implementing data types registry
from goose.data.data_types import Data_Type, Data_Retrieval_Function

# opeations registry (root operations folder)
global goose_operations
goose_operations = Operations_Folder("goose", "Football-Goose")

# model definitions registry
class Model_Definitions_Registry:
    # dictionary : model_class_name --> (class, description)
    def __init__(self):
        self.model_definitions_dict = {}

    # register a new model definition
    def register(self, model_class, name, description):
        self.model_definitions_dict[model_class.__name__ if name == None else name] = (model_class, description)

    # retrieves given model_class_names defn
    def retrieve_definition(self, model_class_name):
        cls, _ = self.model_definitions_dict[model_class_name]
        return cls
    
    # Displays Model_Definitions_Registry
    def display(self):
        print(f"{50 * '-'}")
        print(f"Accesible model definitions ({len(self.model_definitions_dict)}):")
        for name, (cls, description) in self.model_definitions_dict.items():
            print(f"📍 {name:^30} | {f'[ {cls.__name__} ]':^30} ➔  {description}")
        print(f"{50 * '-'}")

global model_definitions_registry 
model_definitions_registry = Model_Definitions_Registry()

# models registry
class Models_Registry:
    # dictionary : model_name --> .fgm folder path
    def __init__(self):
        self.models_dict = {}
    
    # register a new model
    def register(self, model_name, fgm_folder_path):
        self.models_dict[model_name] = fgm_folder_path
    
    # retrieve model_path
    def retrieve_path(self, model_name):
        return self.models_dict[model_name]
    
    # Displays Model_Registry
    def display(self):
        print(f"{50 * '-'}")
        print(f"Accessible models ({len(self.models_dict)}):")
        for model_name, fgm_path in self.models_dict.items():
            print(f"🧠 {model_name:^30} | ➔  {fgm_path}")
        print(f"{50 * '-'}")

global models_registry
models_registry = Models_Registry()

# data types registry
class Data_Types_Registry:
    # dictionary : data type name --> data type object
    # dictionary : data type object --> currently selected Data_Retrieval_Function
    def __init__(self):
        self.data_types_dict = {}
        self.selected_sources = {}

    # register a new data type
    def register(self, data_type : Data_Type):
        self.data_types_dict[data_type.name] = data_type

    # set data retrieval source of specified data
    def set_source(self, data_type : Data_Type, retrieval_function : Data_Retrieval_Function):
        self.selected_sources[data_type] = retrieval_function

    # retrieves currently selected source
    def retrieve_source(self, data_type : Data_Type):
        return self.selected_sources[data_type]
    
    # Displays Data_Types_Registry
    def display(self):
        print(f"{50 * '-'}")
        print(f"Accessible data types ({len(self.data_types_dict)}):")
        # print all data types
        for name, data_type in self.data_types_dict.items():
            # Get the currently active source for this type
            active_source = self.selected_sources[data_type]
            active_name = active_source.name
            # print data type
            print(f"📦 {name}")
            # list-print all available source data retrieval functions as "cables"
            for src_name in data_type.data_retrieval_functions.keys():
                # if active source
                if src_name == active_name:
                    # inidicate this is the active source
                    print(f"    🔌 {src_name:<30} 🟢 [ACTIVE]")
                # if other source
                else:
                    print(f"    🔌 {src_name:<30}")
            # if no sources available
            if not data_type.data_retrieval_functions:
                print("    (No sources available)")
        print(f"{50 * '-'}")

# dictionary of data types and respective sources
global data_types_registry
data_types_registry = Data_Types_Registry()