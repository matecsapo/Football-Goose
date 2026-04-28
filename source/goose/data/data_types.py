# for creating a template for data types and standardizing data retrieval
from typing import TypeAlias, Callable

# Generalized template for all source data types
class Data_Type():
    # all data types have:
        # (optionally) name and description
        # a contract for functions pulling data of this data type
        # dictionary of data retrieval function associated with data type
    def __init__(self, name : str, data_retrieval_contract : TypeAlias = Callable, description : str = None):
        self.name = name
        self.description = description
        self.data_retrieval_contract = data_retrieval_contract
        self.data_retrieval_functions = {} # func name --> function

    # Factory method for creating a Data Type
    # returns Data_Type object defining the data type
    # registers data type in Goose's registry
    @staticmethod
    def Create_Type(name : str, data_retrieval_contract : TypeAlias = Callable, description : str = None):
        # create data type's object
        data_type = Data_Type(name, data_retrieval_contract, description)
        # register neew data type
        import goose.registry as registry
        registry.data_types_registry.register(data_type)
        # return created data type for interactivity
        return data_type
    
    # Decorator for associating a data retrieval function with a data type
    def Define_Data_Retrieval_Function(self, name : str, description : str = None):
        # function must be of Data_Type's required contract
        def decorator(function : self.data_retrieval_contract):
            data_retrieval_function = Data_Retrieval_Function(function, name, description)
            self.data_retrieval_functions[name] = data_retrieval_function
            return function
        return decorator
    
    # Set desired source data retrieval function
    def Set_Source(self, source_data_retrieval_function_name : str):
        import goose.registry as registry
        selected_function = self.data_retrieval_functions[source_data_retrieval_function_name]
        registry.data_types_registry.set_source(self, selected_function)

    # retrieve data using currently set data retrieval function
    def Retrieve(self, *args, **kwargs):
        import goose.registry as registry
        selected_function : Data_Retrieval_Function = registry.data_types_registry.retrieve_source(self)
        # retrieve data via the selected function
        return selected_function.function(*args, **kwargs)

# Generalized template for functions that retrieve data (i.e. standings, results, etc.)
class Data_Retrieval_Function:
    # A data retrieval function has:
        # (optionally) name and description (i.e., what source is this)
        # function
    def __init__(self, function : Callable, name : str = None, description : str = None):
        self.name = function.__name__ if name == None else name
        self.description = description
        self.function = function