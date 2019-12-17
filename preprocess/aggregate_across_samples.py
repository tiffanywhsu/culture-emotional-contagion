## FOR CHANGE
import numpy as np
import pickle
import pandas as pd
import csv
import sys


def aggregate_across_samples(pkl_files, output_path):
    '''
    Aggregate all .pkl files (saved output files from calculate_exposure) into one for analysis.
    
    Input:
        pkl_files: file path to a list of .pkl files that you want to aggregate, with no space to between each file (REQUIRED FORMAT: "[file1,file2,...]")
        output_path: file path to which results are saved (REQUIRES .pkl) 
    Output:
        None
    '''

    data_all = {
        "numFriends": [],
        "usableFriends": [],
        "dates": [],
        "HAP": [],
        "LAP": [],
        "HAN": [],
        "LAN": [],
        "NEU": [],
        "friendHAP": [],
        "friendLAP": [],
        "friendHAN": [],
        "friendLAN": [],
        "friendNEU": [],
        "friendHAPCounts": [],
        "friendLAPCounts": [],
        "friendHANCounts": [],
        "friendLANCounts": [],
        "friendNEUCounts": []
    }


    for f in pkl_files:
        data_current = pd.read_pickle(f)

        data_all['numFriends'] = data_all['numFriends'] + data_current['numFriends']
        data_all['usableFriends'] = data_all['usableFriends'] + data_current['usableFriends']
        data_all['dates'] = data_all['dates'] + data_current['dates']
        data_all['HAP'] = data_all['HAP'] + data_current['HAP']
        data_all['LAP'] = data_all['LAP'] + data_current['LAP']
        data_all['HAN'] = data_all['HAN'] + data_current['HAN']
        data_all['LAN'] = data_all['LAN'] + data_current['LAN']
        data_all['NEU'] = data_all['NEU'] + data_current['NEU']
        data_all['friendHAP'] = data_all['friendHAP'] + data_current['friendHAP']
        data_all['friendLAP'] = data_all['friendLAP'] + data_current['friendLAP']
        data_all['friendHAN'] = data_all['friendHAN'] + data_current['friendHAN']
        data_all['friendLAN'] = data_all['friendLAN'] + data_current['friendLAN']
        data_all['friendNEU'] = data_all['friendNEU'] + data_current['friendNEU']
        data_all['friendHAPCounts'] = data_all['friendHAPCounts'] + data_current['friendHAPCounts']
        data_all['friendLAPCounts'] = data_all['friendLAPCounts'] + data_current['friendLAPCounts']
        data_all['friendHANCounts'] = data_all['friendHANCounts'] + data_current['friendHANCounts']
        data_all['friendLANCounts'] = data_all['friendLANCounts'] + data_current['friendLANCounts']
        data_all['friendNEUCounts'] = data_all['friendNEUCounts'] + data_current['friendNEUCounts']


    with open(output_path, 'w') as f:
        pickle.dump(data_all, f)


if __name__ == '__main__':
    aggregate_across_samples(sys.argv[1].strip('[]').split(','), sys.argv[2])

