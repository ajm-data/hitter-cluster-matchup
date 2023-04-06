import json 
from pprint import pprint
import pandas as pd
import numpy as np
import ast

# Read Hitter data
def read_hitter():
    with open('Mike_Trout.json') as f:
        data_str = f.read()


    data = json.loads(data_str)
    first_elem = data[0]


    # if df is a list of dicts then ->
    df = pd.DataFrame(data)


    cols = ['pitcher', 'pitcherFirstName',
        'pitcherLastName',
        'ab', 'h', '2b', '3b', 'hr', 'rbi',
        'bb', 'so', 'sb', 'cs', 'avg', 'obp', 'slg', 'ops']

    df = df[cols]

    return df

