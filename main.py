import pandas as pd
import logging
from transformer import create_transformer_output
import operation as operation
import logger_config as lc

logger = lc.get_logger("transformer_log", "logs/logger.log")
logger.setLevel(logging.DEBUG)

#logger.debug(pd.show_versions(as_json=False))

def transform_tr_set(input_df, transformer_data):
    logger.info("Start Processing ")
    logger.debug(f"Transformer Data\n{transformer_data}")
    logger.debug(f"Input Dataframe\n{input_df}")
    output_df = create_transformer_output(input_df, transformer_data)
    logger.debug(f"Output is\n{output_df}")
    logger.info("Process completed")
    return output_df

def delete_r_nan(df):
    logger.info("Start Processing - Delete NaN")
    logger.debug(f"Input DataFrame\n{df}")
    operation.drop_nan_rows(df)
    logger.debug(f"Output Data\n{df}")
    logger.info("End Processing ")

'''
if __name__ == '__main__':
    d = {'A': [10,6,10,10,10], 'B': [20,30,12,15,8], 'C':[1,2,3,4,5], 'D': [9,2,3,4,8]}
    df = pd.DataFrame({'A': [23,25,28,3,12,21,4,23,27,20], 'B': [5,11,15,7,17,8,8,2,11,15], 
    'C':[5,3,9,5,5,2,10,9,2,8], 'D': [8,8,1,5,3,5,2,3,2,4]})
    transformer = {"cols": ["AA", "BB", "CC", "DD", "EE", "FF"],"generators": {"AA": {"fn": "pct_chng","args": ["A","C"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "pct_chng","args": ["D", "B"]},"DD": {"fn": "pct_chng","args": ["C", "D"]},"EE": {"fn": "shift","args": ["A", "4"]},"FF": {"fn": "pct_chng","args": ["C","B"]}}}
    

    df2 = transform_tr_set(df, transformer)
    print(df2)
'''
