import numpy as np
import pandas as pd
import csv


def process_sentistrength_results(input_path, output_path, tweet_type):    
    '''
    Process SentiStrength results into five affective categories (HAP, LAP, HAN, LAN, NEU).
    
    Input:
        input_path: file path containing SentiStrength output (REQUIRES .txt)
        output_path: file path to which results are saved (REQUIRES .csv) 
        tweet_type: "user" or "friend"
    Output:
        None
    ''' 

    with open(input_path,'r') as f:
        f.readline()
        for line in f:
            posList.append(int(line[0:1]))
            negList.append(int(line[2:4]))
    f.close()

    numStatuses = len(posList)


    # Categorize into HAP, LAP, HAN, LAN, NEU categories
    HAPList = [0]*numStatuses
    LAPList = [0]*numStatuses
    HANList = [0]*numStatuses
    LANList = [0]*numStatuses
    NEUList = [0]*numStatuses
    for i in range(0,numStatuses):
        if posList[i] == 1 and negList[i] == -1:
            NEUList[i] = 1
        else:
            if posList[i] > 1 and posList[i] < 3:
                LAPList[i] = 1
            if posList[i] >= 3:
                HAPList[i] = 1
            if negList[i] < -1 and negList[i] > -3:
                LANList[i] = 1
            if negList[i] <= -3:
                HANList[i] = 1 

    dfGNew = dfG.copy()
    dfGNew['pos'] = posList
    dfGNew['neg'] = negList
    dfGNew['HAP'] = HAPList
    dfGNew['LAP'] = LAPList
    dfGNew['HAN'] = HANList
    dfGNew['LAN'] = LANList
    dfGNew['NEU'] = NEUList



    # Create new dataframe with the necessary informatioon
    if tweet_type == 'friend':
        dfGNewC = dfGNew[['friendid', 'userid', 'updated_time','pos','neg','HAP','LAP','HAN','LAN','NEU']]
    else:
        dfGNewC = dfGNew[['userid','updated_time','pos','neg','HAP','LAP','HAN','LAN','NEU']]


    # Save dataframe
    dfGNewC.to_csv(output_path)


