
import transformer_class as tc
import operation as op
import pandas as pd
import logging

logger = logging.getLogger("transformer_log")

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
    op.drop_nan_rows(output_df)
    return output_df