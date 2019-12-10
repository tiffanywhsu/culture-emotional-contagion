## FOR CHANGE
import numpy as np
import pickle
import pandas as pd
import csv
from constants import *


def aggregate_across_samples(pkl_files, output_path):
    '''
    Aggregate all .pkl files (saved output files from calculate_exposure) into one for analysis.
    
    Input:
        pkl_path_list: file paths of .pkl files that you want to aggregate (list) 
        output_path: file path to which results are saved (REQUIRES .pkl) 
    Output:
        None
    '''

    numFriendsList = []
    UsableFriendsList = []
    YDatesList = []
    YHAPList = []
    YLAPList = []
    YHANList = []
    YLANList = []
    YNEUList = []
    FriendHAPPropList = []
    FriendLAPPropList = []
    FriendHANPropList = []
    FriendLANPropList = []
    FriendNEUPropList = []
    FriendHAPCountsList = []
    FriendLAPCountsList = []
    FriendHANCountsList = []
    FriendLANCountsList = []
    FriendNEUCountsList = []

    for f in pkl_path_list:
        [numFriends, UsableFriends, YDates, YHAP, YLAP, YHAN, YLAN, YNEU, 
         FriendHAPProp, FriendLAPProp, FriendHANProp, FriendLANProp, FriendNEUProp, 
         FriendHAPCounts, FriendLAPCounts, FriendHANCounts, FriendLANCounts, FriendNEUCounts] = pd.read_pickle(f)

        numFriendsList = numFriendsList + numFriends
        UsableFriendsList = UsableFriendsList + UsableFriends
        YDatesList = YDatesList + YDates
        YHAPList = YHAPList + YHAP
        YLAPList = YLAPList + YLAP
        YHANList = YHANList + YHAN
        YLANList = YLANList + YLAN
        YNEUList = YNEUList + YNEU
        FriendHAPPropList = FriendHAPPropList + FriendHAPProp
        FriendLAPPropList = FriendLAPPropList + FriendLAPProp
        FriendHANPropList = FriendHANPropList + FriendHANProp
        FriendLANPropList = FriendLANPropList + FriendLANProp
        FriendNEUPropList = FriendNEUPropList + FriendNEUProp
        FriendHAPCountsList = FriendHAPCountsList + FriendHAPCounts
        FriendLAPCountsList = FriendLAPCountsList + FriendLAPCounts
        FriendHANCountsList = FriendHANCountsList + FriendHANCounts
        FriendLANCountsList = FriendLANCountsList + FriendLANCounts
        FriendNEUCountsList = FriendNEUCountsList + FriendNEUCounts

    with open(output_path, 'w') as f:
        pickle.dump(
            [numFriendsList, UsableFriendsList, YDatesList, 
            YHAPList, YLAPList, YHANList, YLANList, YNEUList, 
            FriendHAPPropList, FriendLAPPropList, FriendHANPropList, FriendLANPropList, FriendNEUPropList, 
            FriendHAPCountsList, FriendLAPCountsList, FriendHANCountsList, FriendLANCountsList, FriendNEUCountsList], 
            f)

