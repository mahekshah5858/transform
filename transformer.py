
import transformer_class as tc
import operation as op
import pandas as pd
import logging
import numpy as np
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger("transformer_log")

'''
Convert the column to float
'''
def convert_to_float(df):
    for i in df.columns:
        if df[i].dtype != np.int64:
            df[i] = df[i].astype(float)
    return df

'''
Use python round function to round till 2 decimal points
'''
def rounded_two_decimal(df):
    if type(df) == type(None):
        return df
    df = convert_to_float(df)
    df = df.round(2)
    return df

'''
Remove intermediate operation columns
'''
def filter_columns(df, tr):
    if type(df) == type(None):
        return df
    df = df[tr.columns]
    return df
'''
Arguments:
    input_df : Input DataFrame
    json_data : Transformer Data
Return:
    output_df : Output dataframe
'''
def create_transformer_output(input_df, json_data):
    tr = tc.TransFormer(json_data)
    if tr.error:
        return None

    output_df = pd.DataFrame([], columns = tr.columns)
    logger.info("Started processing of individual generator")
    for generator in tr.generator_list:
        operation_obj = op.Operation(generator, input_df, output_df)
        if not operation_obj.valid_flag:
            return None
    logger.info("Operations performed")
    output_df = filter_columns(output_df, tr)
    op.drop_nan_rows(output_df)
    output_df = rounded_two_decimal(output_df)
    
    return output_df
