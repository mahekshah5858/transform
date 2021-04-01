import pytest
import pandas as pd
import main as main

test_cases = [(pd.DataFrame({'A': [10,6,10,10,10], 'B': [20,30,12,15,8], 'C':[1,2,3,4,5], 'D': [9,2,3,4,8]}),
     {"cols": ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH"],"generators": {        "AA": {"fn": "idemp","args": ["A"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "pct_chng","args": ["C", "A"]},"DD": {"fn": "pct_chng","args": ["D", "A"]},"EE": {"fn": "shift","args": ["D", "1"]},"FF": {"fn": "shift","args": ["D", "2"]},"GG": {"fn": "shift","args": ["D", "3"]},"HH": {"fn": "pct_chng","args": ["D", "EE"]}}},
     pd.DataFrame({"AA":[10,6],"BB":[100,400],"CC":[-90,-66.67], "DD":[-10, -66.67],
    "EE":[2,3],"FF":[3,4],"GG":[4,8],"HH":[350, -33.33]})),
    (pd.DataFrame({'A': [10,6,10,10,10], 'B': [20,30,12,15,8], 'C':[1,2,3,4,5], 'D': [9,2,3,4,8]}),
     {"cols": ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH"],"generators": {        "AA": {"fn": "idemp","args": ["A"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "pct_chng","args": ["C", "A"]},"DD": {"fn": "pct_chng","args": ["D", "A"]},"EE": {"fn": "shift","args": ["D", "1"]},"FF": {"fn": "shift","args": ["D", "2"]},"GG": {"fn": "shift","args": ["D", "4"]},"HH": {"fn": "pct_chng","args": ["D", "EE"]}}},
    pd.DataFrame({"AA":[10],"BB":[100],"CC":[-90], "DD":[-10],
    "EE":[2],"FF":[3],"GG":[8],"HH":[350]})),
    (pd.DataFrame({'A': [18,13,14,30,23], 'B': [2,4,2,4,5], 'C':[6,9,2,1,3], 'D': [6,9,6,6,7]}),
    {"cols": ["AA", "BB", "CC", "DD", "EE", "FF"],"generators": {        "AA": {"fn": "idemp","args": ["B"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "shift","args": ["D", "3"]},"DD": {"fn": "pct_chng","args": ["C", "D"]},"EE": {"fn": "shift","args": ["A", "4"]},"FF": {"fn": "idemp","args": ["C"]}}},
    pd.DataFrame({"AA":[2],"BB":[-88.89],"CC":[6], "DD":[0],
    "EE":[23],"FF":[6]})),
    (pd.DataFrame({'A': [0,13,14,30,23], 'B': [10,4,2,4,5], 'C':[6,9,2,1,3], 'D': [6,9,6,6,7]}),
    {"cols": ["AA", "BB", "CC", "DD", "EE", "FF"],"generators": {        "AA": {"fn": "idemp","args": ["B"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "shift","args": ["D", "3"]},"DD": {"fn": "pct_chng","args": ["C", "D"]},"EE": {"fn": "shift","args": ["A", "4"]},"FF": {"fn": "idemp","args": ["C"]}}},
    None),
    (pd.DataFrame({'A': [10,13,14,30,23], 'B': [10,4,2,4,5], 'C':[6,9,2,1,3], 'D': [6,9,6,6,7]}),
    {"cols": ["AA", "BB", "CC", "DD", "EE", "FF"],"generators": {        "AA": {"fn": "idemp","args": ["B"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "shift","args": ["D", "6"]},"DD": {"fn": "pct_chng","args": ["C", "D"]},"EE": {"fn": "shift","args": ["A", "4"]},"FF": {"fn": "idemp","args": ["C"]}}},
    None),
    (pd.DataFrame({'A': [23,25,28,3,12,21,4,23,27,20], 'B': [5,11,15,7,17,8,8,2,11,15], 
    'C':[5,3,9,5,5,2,10,9,2,8], 'D': [8,8,1,5,3,5,2,3,2,4]}),
    {"cols": ["AA", "BB", "CC", "DD", "EE", "FF"],"generators": {"AA": {"fn": "pct_chng","args": ["A","C"]},"BB": {"fn": "pct_chng","args": ["B", "A"]},"CC": {"fn": "pct_chng","args": ["D", "B"]},"DD": {"fn": "pct_chng","args": ["C", "D"]},"EE": {"fn": "shift","args": ["A", "4"]},"FF": {"fn": "pct_chng","args": ["C","B"]}}},
    pd.DataFrame({"AA":[360,733.33,211.11,-40,140,950],"BB":[-78.26,-56,-46.43,133.33,41.67,-61.90],"CC":[60,-27.27,-93.33,-28.57,-82.35,-37.5], "DD":[-37.5,-62.5,800,0,66.67,-60],
    "EE":[12,21,4,23,27,20],"FF":[0,-72.73,-40,-28.57,-70.59,-75]}))
    ]


def convert_to_float(df):
    for i in df.columns:
        df[i] = df[i].astype(float)
    return df

def post_process_output(df):
    if type(df) == type(None):
        return df
    df = convert_to_float(df)
    df = df.round(2)
    return df

@pytest.mark.parametrize("test_input,transformer, expected", test_cases)
def test_eval(test_input,transformer, expected):

    op_result = main.transformer_output(test_input, transformer)
    op_result = post_process_output(op_result)
    op = post_process_output(expected)
    if type(op) == type(None):
        assert type(op) == type(op_result)
    else:
        assert op.equals(op_result) == True
    