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
        self.decide_generator_list_order()
        print(self.columns)
        self.decide_columns()


        logger.info("Transformer Object created ")

    '''
    Decide the order of the generator
    '''
    def decide_generator_list_order(self):
        temp_dictionary = {i.key: i for i in self.generator_list}
        execute_list = []
        for key in temp_dictionary:
            if key in execute_list:
                continue
            vals = temp_dictionary[key].arguments
            for temp in vals:
                if temp in execute_list or temp not in temp_dictionary:
                    continue
                execute_list.append(temp)
            execute_list.append(key)

        temp_generator_list = []
        for i in execute_list:
            temp_generator_list.append(temp_dictionary[i])
        
        self.generator_list = temp_generator_list

    '''
    Decide column order
    '''
    def decide_columns(self):
        column_ordered = []
        for i in self.generator_list:
            if i.key in self.columns and i.key not in column_ordered:
                column_ordered.append(i.key)
        
        self.columns  = column_ordered
        
 
    '''
    Arguments:
        self : Transformer Object
        
    Return:
        True: If transformer columns and generator columns are same
        False : If transformer columns and generator columns are not same
    '''
    def validate_columns(self):
        generator_keys = self.generators.keys()

        if set(self.columns) - set(generator_keys) != {}:
            logger.error("one or more columns are not matching with the transformer columns {set(self.columns) - set(generator_keys)}")
            #print(f"one or more columns are not matching with the transformer columns {set(self.columns) - set(generator_keys)}")
            return True
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
            logger.error("Invalid function name {self.function}. Please choose from te {valid_functions}")
            #print(f"Invalid function name {self.function}")
            return False
        
        if self.function.strip() == "idemp" and len(self.arguments) == 1:
            return True
        elif self.function.strip() == "pct_chng" and len(self.arguments) == 2:
            return True
        elif self.function.strip() == "shift" and len(self.arguments) == 2:
            return True
        else:
            logger.error("Please check the function {self.function} and argument {self.arguments}")
        
        
    
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
            logger.error("Transformer json key is not matching with the template transformer key. Please chech {key}")
            #print(f"key is not as expected. Rename its to {key}")
            return False
    return True
        
