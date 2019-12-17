from datetime import datetime
import pandas as pd
from pathlib import Path
from constants import *


def convert_time(x):
    """Convert str into datetime object"""
    try:
        xr = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    except:
        xr = None
        pass
    return xr


def convert_12_to_24(s):
    time = int(s[:-2])
    period = s[-2:]
    if period == 'pm':
        time += 12
    elif time == 12:
        time = 0

    return time


def flatten(data):
    """Flatten dict values (list of lists)"""
    for k,v in data.items():
        flattened = sum(v, [])
        data[k] = flattened

    return data


def to_dataframe(country, data, save=False, verbose=False):
    data = flatten(data)
    df = pd.DataFrame(data)
    if country=='USA':
        df['country'] = 0
    elif country=='japan':
        df['country'] = 1
    else:
        raise ValueError("Invalid country")

    if save:
        save_path = DATA_DIR / (country + ".csv")
        df.to_csv(save_path, index=False)
        if verbose:
            print("Saved {} dataframe to {}".format(country, save_path))

    return df
