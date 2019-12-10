from datetime import timedelta
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm
from constants import *
from utils import convert_time

def calculate_exposure(country, users_path, friends_path, collection_time, output_path, verbose=False):
    """
    Read and join users and friends tweet csv.
    Requires both csv to be sorted by userid/friendid and date.
    
    Input:
        users_path: path of users tweet csv (posixPath)
        friends_path: path of friends tweet csv (posixPath)
        collection_time: time when tweets were collected (string, in format 'YYYY-MM-DD HH:MM:SS')
        output_path: file path to which results are saved (REQUIRES .pkl) 
    Output:
        data: dictionary of nested lists
    """
    df_users = pd.read_csv(users_path)
    df_friends = pd.read_csv(friends_path)

    # get unique users and friends lists    
    users = list(set(df_users['userid'].unique()))
    friends = list(set(df_friends['friendid'].unique()))
    if verbose:
        print("Number of {} users: {}".format(country, len(users)))
        print("Number of {} friends: {}".format(country, len(friends)))

    n = len(users)

    collection_time = convert_time(collection_time)
    
    """
    # cache user row index range
    users_rows = {}
    for user in users:
        idxs = df_users.index[df_users['userid'] == user] 
        # add 1 because python indexing is noninclusive end
        users_rows[user] = [min(idxs), max(idxs)+1]

    friends_rows = {}
    for user in list(set(df_friends['userid'].unique())):
        idxs = df_friends.index[df_friends['userid'] == user]
        friends_rows[user] = [min(idxs), max(idxs)+1]
    """
    
    # convert time into datetime series
    df_users['updated_time'] = pd.to_datetime(df_users['updated_time'], format="%Y-%m-%d %H:%M:%S")
    df_friends['updated_time'] = pd.to_datetime(df_friends['updated_time'], format="%Y-%m-%d %H:%M:%S")

    # subset data collected from 1 week prior of collection date
    df_friends = df_friends[df_friends['updated_time'] >= (collection_time - np.timedelta64(1, 'W'))]
    df_users = df_users[(df_users['updated_time'] - TIMELAPSE) >= (collection_time - np.timedelta64(1, 'W'))]

    # define empty cols
    yHAP = [[] for i in range(n)]
    yLAP = [[] for i in range(n)]
    yHAN = [[] for i in range(n)]
    yLAN = [[] for i in range(n)]
    yNEU = [[] for i in range(n)]
    friendsHAPCounts = [[] for i in range(n)]
    friendsLAPCounts = [[] for i in range(n)]
    friendsHANCounts = [[] for i in range(n)]
    friendsLANCounts = [[] for i in range(n)]
    friendsNEUCounts = [[] for i in range(n)]
    friendsHAPProp = [[] for i in range(n)]
    friendsLAPProp = [[] for i in range(n)]
    friendsHANProp = [[] for i in range(n)]
    friendsLANProp = [[] for i in range(n)]
    friendsNEUProp = [[] for i in range(n)]
    yDates = [[] for i in range(n)]
    numFriends = [[] for i in range(n)]
    usableFriends = [[] for i in range(n)]

    # merge
    userid_df_friends = list(set(df_friends['userid'].unique()))
    users.sort()
    for s, user in tqdm(enumerate(users)):
        if user not in userid_df_friends:
            continue
      
        # subset on userid
        subG = df_users[df_users['userid'] == user]
        allfG = df_friends[df_friends['userid'] == user]

        # loop over user tweets
        for i in range(len(subG)):
            # only sample at max 50
            if len(usableFriends[s]) == TIMESAMPLES:
                break

            # subset friend tweets within 1 hr prior of users tweet
            t1 = subG['updated_time'].values[i]
            t2 = t1 - TIMELAPSE
            usablefG = allfG[(allfG['updated_time'] >= t2) & 
                             (allfG['updated_time'] < t1)]

            # only take user tweets that have at least 20 corresponding friend tweets
            if len(usablefG) < 20:
                continue

            # append data
            numFriends[s].append(len(allfG))
            usableFriends[s].append(len(usablefG))
            yDates[s].append(t1)

            HAPCounts = sum(usablefG['HAP'])*1.0
            LAPCounts = sum(usablefG['LAP'])*1.0
            HANCounts = sum(usablefG['HAN'])*1.0
            LANCounts = sum(usablefG['LAN'])*1.0
            NEUCounts = sum(usablefG['NEU'])*1.0

            friendsHAPCounts[s].append(HAPCounts)
            friendsLAPCounts[s].append(LAPCounts) 
            friendsHANCounts[s].append(HANCounts)
            friendsLANCounts[s].append(LANCounts) 
            friendsNEUCounts[s].append(NEUCounts)
            
            yHAP[s].append(subG['HAP'].values[i])
            yLAP[s].append(subG['LAP'].values[i])
            yHAN[s].append(subG['HAN'].values[i])
            yLAN[s].append(subG['LAN'].values[i])
            yNEU[s].append(subG['NEU'].values[i])
                
            friends_tote = len(usablefG)

            friendsHAPProp[s].append(HAPCounts / friends_tote)
            friendsLAPProp[s].append(LAPCounts / friends_tote)
            friendsHANProp[s].append(HANCounts / friends_tote)
            friendsLANProp[s].append(LANCounts / friends_tote)
            friendsNEUProp[s].append(NEUCounts / friends_tote)

    save_path = PROCESSED_DATA_DIR / (output_filename + ".pkl")
    data = {
        "numFriends": numFriends,
        "usableFriends": usableFriends,
        "dates": yDates,
        "HAP": yHAP,
        "LAP": yLAP,
        "HAN": yHAN,
        "LAN": yLAN,
        "NEU": yNEU,
        "friendHAP": friendsHAPProp,
        "friendLAP": friendsLAPProp,
        "friendHAN": friendsHANProp,
        "friendLAN": friendsLANProp,
        "friendNEU": friendsNEUProp,
        "friendHAPCounts": friendsHAPCounts,
        "friendLAPCounts": friendsLAPCounts,
        "friendHANCounts": friendsHANCounts,
        "friendLANCounts": friendsLANCounts,
        "friendNEUCounts": friendsNEUCounts
    }

    return data

