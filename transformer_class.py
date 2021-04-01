import logging

logger = logging.getLogger("transformer_log")


'''
Arguments:
    json_data : Transformer Data
Return:
    Transformer object
'''

class TransFormer:
    def __init__(self, json_data):
        logger.info("Transformer Object initiated ")
        self.json_data = json_data
        self.error = False

        input_key_validation = validate_input_keys(['cols','generators'], json_data)
        if not input_key_validation:
            self.error = True

        self.columns = json_data['cols']
        self.generators = json_data['generators']
        column_validation = self.validate_columns()
        if not column_validation:
            self.error = True
        
        self.generator_list = []
        for column in self.generators:
            generator_object = Generator(column, self.generators[column])
            if generator_object.error:
                self.error = True
                break

            self.generator_list.append(generator_object)

        logger.info("Transformer Object created ")
        
 
    '''
    Arguments:
        self : Transformer Object
        
    Return:
        True: If transformer columns and generator columns are same
        False : If transformer columns and generator columns are not same
    '''
    def validate_columns(self):
        generator_keys = self.generators.keys()

        if set(self.columns) != set(generator_keys):
            logger.error(f"one or more columns are not matching with the transformer columns {set(self.columns) - set(generator_keys)}")
            #print(f"one or more columns are not matching with the transformer columns {set(self.columns) - set(generator_keys)}")
            return False
        return True
        
        
            
'''        
Arguments:
    key : Column name for which operation needs to perform
    value : Function name and arguments
Return:
    Generator object
'''
class Generator:
    def __init__(self, key, value):
        logger.info("Generator class initiated")
        self.key = key
        self.error = False
        input_key_validation = validate_input_keys(['fn','args'], value)
        if not input_key_validation:
            self.error = True
        
        self.function = value['fn']
        self.arguments = value['args']
        if self.validate_function_argument() == False:
            self.error = True
        logger.info("Generator class created")
        
     
    '''        
    Arguments:
        self : Generator Object
        
    Return:
        True: If function name in the function name list 
        False : If function name not in the function name list 
    '''
    def validate_function_argument(self):
        valid_functions = ['idemp', 'pct_chng', 'shift']
        if self.function.strip() not in valid_functions:
            logger.error(f"Invalid function name {self.function}. Please choose from te {valid_functions}")
            #print(f"Invalid function name {self.function}")
            return False
        
        if self.function.strip() == "idemp" and len(self.arguments) == 1:
            return True
        elif self.function.strip() == "pct_chng" and len(self.arguments) == 2:
            return True
        elif self.function.strip() == "shift" and len(self.arguments) == 2:
            return True
        else:
            logger.error(f"Please check the function {self.function} and argument {self.arguments}")
        
        
    
'''        
Arguments:
    list_of_keys : transformer data keys
    data : transformer data dictionary
    
Return:
    True: If all the keys are present in dictionary
    False : If all the keys are not present in dictionary
'''    
def validate_input_keys(list_of_keys, data):
    for key in list_of_keys:
        if key not in data:
            logger.error(f"Transformer json key is not matching with the template transformer key. Please chech {key}")
            #print(f"key is not as expected. Rename its to {key}")
            return False
    return True
        