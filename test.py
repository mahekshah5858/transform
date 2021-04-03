import yaml
import json
import pandas as pd

from main import transform_tr_set

import traceback

g_tc_dir = 'tests'
g_tc_inputs_dir = 'tests/data/inputs/'
g_tc_outputs_dir = 'tests/data/outputs/'
g_ts_filename = 'ts.yaml'

g_tc_exec_results = {}

def exec_and_eval_transform_tr_set(args, out):
    if len(args) != 2:
        print('Number of arguments: ' + str(len(args)) + ' != 2')
        return 'NE_INVALID_INPUTS'
    if len(out) != 1:
        print('Number of return vals: ' + str(len(out)) + ' != 1')
        return 'NE_INVALID_OUTPUTS'

    input_csv = g_tc_inputs_dir + args[0]
    try:
        if input_csv == 'NULL':
            in_df = None
        elif input_csv == 'EMPTY':
            in_df = pd.DataFrame()
        else:
            in_df = pd.read_csv(input_csv)
    except:
        print('Error in reading input CSV ' + args[0] + ' file')
        return 'NE_INVALID_INPUTS'

    transformer_file = g_tc_inputs_dir + args[1]
    try:
        if transformer_file == 'NULL':
            transformer = None
        else:
            with open(transformer_file) as tr_file:
                transformer = json.load(tr_file)
    except:
        print('Error in reading input JSON ' + args[1] + ' file')
        return 'NE_INVALID_INPUTS'

    output_csv = g_tc_outputs_dir + out[0]
    try:
        expec_out_df = pd.read_csv(output_csv)
    except:
        print('Error in reading output CSV ' + out + ' file')
        return 'NE_INVALID_OUTPUT'

    try:
        out_df = transform_tr_set(in_df, transformer)
    except:
        print('Exception occurred in transform_tr_set\n')
        traceback.print_exc()

        return 'EXCEPTION_OCCURRED'

    if out_df.equals(expec_out_df) == True:
        return 'PASS'
    else:
        return 'FAIL'


def exec_and_eval_delete_r_nan(args, out):
    if len(args) != 1:
        print('Number of arguments: ' + str(len(args)) + ' != 1')
        return 'NE_INVALID_INPUTS'
    if len(out) != 1:
        print('Number of return vals: ' + str(len(out)) + ' != 1')
        return 'NE_INVALID_OUTPUTS'

    return 'FAIL'


def exec_tc(tc):
    result = 'FAIL'

    print(tc)

    if tc['fn'] == 'transform_tr_set':
        result = exec_and_eval_transform_tr_set(tc['args'], tc['out'])
    elif tc['fn'] == 'delete_r_nan':
        result = exec_and_eval_delete_r_nan(tc['args'], tc['out'])
    else:
        print('Unable to test ' + tc['fn'] + ' because it is not defined for me')

    return result    

def run():
    print('\nReading Test Suite')

    with open(g_tc_dir + '/' + g_ts_filename) as ts_file:
        tc_list = yaml.load(ts_file, Loader=yaml.FullLoader)

    print('Going to execute following tests: \n', tc_list)

    for tc_name in tc_list[g_tc_dir]:
        tc_filename = g_tc_dir + '/' + tc_name + '.yaml'
        tc_filename = tc_filename.lower()
        try:
            with open(tc_filename) as tc_file:
                tc = yaml.load(tc_file, Loader=yaml.FullLoader)

            print('\n--- Executing TC: ' + tc_name + ', TC File: ' + tc_filename)
            result = exec_tc(tc)

            g_tc_exec_results[tc_name] = result
        except FileNotFoundError:
            print('\n--- Skipping TC: ' + tc_name + ' because TC File: ' + tc_filename + ' Not Found')
            g_tc_exec_results[tc_name] = 'SKIPPED'

    print('\n=== Final Results:')
    print(g_tc_exec_results)
                
if __name__ == '__main__':
    run()
