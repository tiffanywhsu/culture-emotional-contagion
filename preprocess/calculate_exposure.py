from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm
import sys



def calculate_exposure(users_path, friends_path, collection_time, output_path, timesamples=50, timelapse=1, verbose=False):
    """
    Read and join users and friends tweet csv.
    Requires both csv to be sorted by userid/friendid and date.
    
    Input:
        users_path: path of users tweet csv (posixPath)
        friends_path: path of friends tweet csv (posixPath)
        collection_time: time when tweets were collected (string, in format 'YYYY-MM-DD HH:MM:SS')
        output_path: file path to which results are saved (REQUIRES .pkl) 
        timesamples: the number of data points to take per user (default 50)
        timelapse: the number of hours prior to user tweet to take corresponding friends tweets (default 1)
        verbose: print out progress or not (default False)
    Output:
        data: dictionary of nested lists
    """
    df_users = pd.read_csv(users_path)
    df_friends = pd.read_csv(friends_path)

    # get unique users and friends lists    
    users = list(set(df_users['userid'].unique()))
    friends = list(set(df_friends['friendid'].unique()))
    if verbose:
        print("Number of users: ", len(users))
        print("Number of friends: ", len(friends))

    n = len(users)


    # convert collection_time to datetime
    collection_time = pd.to_datetime(collection_time, format="%Y-%m-%d %H:%M:%S")
    
    # convert time into datetime series
    df_users['updated_time'] = pd.to_datetime(df_users['updated_time'], format="%Y-%m-%d %H:%M:%S")
    df_friends['updated_time'] = pd.to_datetime(df_friends['updated_time'], format="%Y-%m-%d %H:%M:%S")

    # subset data collected from 1 week prior of collection date
    df_friends = df_friends[df_friends['updated_time'] >= (collection_time - timedelta(weeks=1))]
    df_users = df_users[(df_users['updated_time'] - timedelta(hours=timelapse)) >= (collection_time - timedelta(weeks=1))]

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
            if len(usableFriends[s]) == timesamples:
                break

            # subset friend tweets within 1 hr prior of users tweet
            t1 = subG['updated_time'].values[i]
            t2 = t1 - np.timedelta64(1, 'h')

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

    with open(output_path, 'w') as f:
        pickle.dump(data, f)

    return data


if __name__ == '__main__':
    if len(sys.argv) == 5:
        calculate_exposure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 6:
        calculate_exposure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif len(sys.argv) == 7:
        calculate_exposure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        calculate_exposure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
