import logging
import numpy as np

logger = logging.getLogger("transformer_log")


'''        
Arguments:
    input_dataframe : input dataframe
    processed_dataframe : result dataframe processed till the previous operation
    column : column name
    
Return:
    Series : data corresponding to the column name
'''    

def return_series(input_dataframe, processed_dataframe, column):
    if column in input_dataframe.columns:
        return input_dataframe[column]
    if column in processed_dataframe.columns:
        return processed_dataframe[column]
        
'''        
Arguments:
    generator_object : generator object that has function and agument details
    input_dataframe : input dataframe
    processed_dataframe : result dataframe processed till the previous operation

    
Return:
    None
''' 
class Operation:
    
    def __init__(self, generator_object, input_dataframe, processed_df):
        logger.info("Operation class initiated")
        logger.debug("Generator class : {generator_object.__dict__}")
        self.generator_object = generator_object
        self.input_df = input_dataframe
        self.processed_df = processed_df
        self.valid_flag = self.perform_operation()
        
        logger.info("Operation class created")
        
    '''
    Arguments:
        self : operation object 
        
    Return:
        False: If any error with the argument and operation
        True : If operation successful
    '''
    def perform_operation(self):
        logger.debug("Operation is {self.generator_object.function}")
        if self.generator_object.function == "idemp":
            return self.idemp()
        
        elif self.generator_object.function == "pct_chng":
            return self.pct_chng()
            
        elif self.generator_object.function == "shift":
            return self.shift()
        
        
    '''
    Arguments:
        self : operation object 
        
    Return:
        False: If any error with the argument and operation
        True : If operation successful
    '''    
    def idemp(self):
        logger.debug("Idemp operation started")
        target_column = self.generator_object.key
        arguments = self.generator_object.arguments
        source_column = arguments[0]
        ip_series = return_series(self.input_df, self.processed_df, source_column)
        self.processed_df[target_column] = ip_series
        logger.debug("Idemp operation completed")
        return True
        
    def pct_chng(self):
        logger.debug("percentage change operation started")
        target_column = self.generator_object.key
        arguments = self.generator_object.arguments
        source_column_1 = arguments[0]
        source_column_2 = arguments[1]
        ip_series_1 = return_series(self.input_df, self.processed_df, source_column_1)
        ip_series_2 = return_series(self.input_df, self.processed_df, source_column_2)
        try:
            ou = ((ip_series_1 - ip_series_2)/ip_series_2)*100
            ds =  np.isinf(ou).values.sum()

            if ds != 0:
                logger.exception("One of the series value is 0. series {ip_series_2.to_list()}. Divide by zero.")
                return False

            self.processed_df[target_column] = ou
        except ZeroDivisionError as e:
            logger.exception("One of the series value is 0. series {ip_series_2.to_list()}. Divide by zero. {e}")
            return False
        logger.debug("percentage change operation completed")
        return True
            
            
    def shift(self):
        target_column = self.generator_object.key
        
        arguments = self.generator_object.arguments
        source_column = arguments[0]
        shift_number = int(arguments[1])
        ip_series = return_series(self.input_df, self.processed_df, source_column)
        if shift_number > len(ip_series):
            logger.error("Size of input series in smaller than the shift. Input data {ip_series.to_list()} and shift number {shift_number}")
            return False
        op = ip_series.iloc[shift_number:].reset_index(drop=True)

        self.processed_df[target_column] = op
        return True

'''
    Arguments:
        df : DataFrame
        
    Return:
        None
    '''
def drop_nan_rows(df):
    return df.dropna(inplace = True)
