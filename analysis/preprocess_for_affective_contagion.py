import numpy as np
import pickle
import pandas as pd
import csv
from scipy.stats import ttest_ind
from scipy.stats.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import chi2_contingency
import sys


def clean_data(us_path, jp_path):
  '''
  Clean pkl input files to csv dataframes to be fed into save_dataframe_for_between_culture_comparison 
  or save_dataframe_for_within_culture_comparison

  Input:
    us_path: file path to US .pkl file to analyze (string)
    jp_path: file path to JP .pkl file to analyze (string)
  Output:
    dfUS: cleaned dataframe for US data
    dfJP: cleaned dataframe for JP data
  '''

  # Read in data
  data_us = pd.read_pickle(us_path)
  data_jp = pd.read_pickle(jp_path)


  ############################### Processing ##################################################

  # Store number of tweets per user into a list
  ussubLen = np.array([len(i) for i in data_us['numFriends']])
  jpsubLen = np.array([len(i) for i in data_jp['numFriends']])


  # Flatten data
  usnumFriendsFlat = sum(data_us['numFriends'],[])
  usUsableFriendsFlat = sum(data_us['usableFriends'],[])
  usYDatesFlat = sum(data_us['dates'],[])
  usYHAPFlat = sum(data_us['HAP'],[])
  usYLAPFlat = sum(data_us['LAP'],[])
  usYHANFlat = sum(data_us['HAN'],[])
  usYLANFlat = sum(data_us['LAN'],[])
  usYNEUFlat = sum(data_us['NEU'],[])
  usFriendHAPPropFlat = sum(data_us['friendHAP'],[])
  usFriendLAPPropFlat = sum(data_us['friendLAP'],[])
  usFriendHANPropFlat = sum(data_us['friendHAN'],[])
  usFriendLANPropFlat = sum(data_us['friendLAN'],[])
  usFriendNEUPropFlat = sum(data_us['friendNEU'],[])
  usFriendHAPCountsFlat = sum(data_us['friendHAPCounts'],[])
  usFriendLAPCountsFlat = sum(data_us['friendLAPCounts'],[])
  usFriendHANCountsFlat = sum(data_us['friendHANCounts'],[])
  usFriendLANCountsFlat = sum(data_us['friendLANCounts'],[])
  usFriendNEUCountsFlat = sum(data_us['friendNEUCounts'],[])       
  usFriendHAPPropFlatPerc = np.array(usFriendHAPPropFlat)*100
  usFriendLAPPropFlatPerc = np.array(usFriendLAPPropFlat)*100
  usFriendHANPropFlatPerc = np.array(usFriendHANPropFlat)*100
  usFriendLANPropFlatPerc = np.array(usFriendLANPropFlat)*100
  usFriendNEUPropFlatPerc = np.array(usFriendNEUPropFlat)*100


  jpnumFriendsFlat = sum(data_jp['numFriends'],[])
  jpUsableFriendsFlat = sum(data_jp['usableFriends'],[])
  jpYDatesFlat = sum(data_jp['dates'],[])
  jpYHAPFlat = sum(data_jp['HAP'],[])
  jpYLAPFlat = sum(data_jp['LAP'],[])
  jpYHANFlat = sum(data_jp['HAN'],[])
  jpYLANFlat = sum(data_jp['LAN'],[])
  jpYNEUFlat = sum(data_jp['NEU'],[])
  jpFriendHAPPropFlat = sum(data_jp['friendHAP'],[])
  jpFriendLAPPropFlat = sum(data_jp['friendLAP'],[])
  jpFriendHANPropFlat = sum(data_jp['friendHAN'],[])
  jpFriendLANPropFlat = sum(data_jp['friendLAN'],[])
  jpFriendNEUPropFlat = sum(data_jp['friendNEU'],[])
  jpFriendHAPCountsFlat = sum(data_jp['friendHAPCounts'],[])
  jpFriendLAPCountsFlat = sum(data_jp['friendLAPCounts'],[])
  jpFriendHANCountsFlat = sum(data_jp['friendHANCounts'],[])
  jpFriendLANCountsFlat = sum(data_jp['friendLANCounts'],[])
  jpFriendNEUCountsFlat = sum(data_jp['friendNEUCounts'],[])
  jpFriendHAPPropFlatPerc = np.array(jpFriendHAPPropFlat)*100
  jpFriendLAPPropFlatPerc = np.array(jpFriendLAPPropFlat)*100
  jpFriendHANPropFlatPerc = np.array(jpFriendHANPropFlat)*100
  jpFriendLANPropFlatPerc = np.array(jpFriendLANPropFlat)*100
  jpFriendNEUPropFlatPerc = np.array(jpFriendNEUPropFlat)*100



  ############################### Clean processed data into dataframes ##################################################
  usSub = []
  for sub in range(len(ussubLen)):
      for i in range(len(data_us['numFriends'][sub])):
          usSub.append(sub)

  jpSub = []
  for sub in range(len(jpsubLen)):
      for i in range(len(data_jp['numFriends'][sub])):
          jpSub.append(len(set(usSub))+sub)


  # Store number of tweets and number of users
  usnumTweets = len(usFriendHAPPropFlat)
  jpnumTweets = len(jpFriendHAPPropFlat)
  usnumSubs = len(set(usSub))
  jpnumSubs = len(set(jpSub))


  combine = [usYHAPFlat, 
             usYLAPFlat, 
             usYHANFlat, 
             usYLANFlat, 
             usYNEUFlat, 
             usFriendHAPPropFlatPerc, 
             usFriendLAPPropFlatPerc, 
             usFriendHANPropFlatPerc, 
             usFriendLANPropFlatPerc, 
             usFriendNEUPropFlatPerc, 
             usSub]

  dfUS = pd.DataFrame(np.array([combine[0], combine[1], combine[2], combine[3], combine[4], combine[5],combine[6], combine[7], combine[8], combine[9], combine[10]]).T,
                      columns=['HAP', 'LAP', 'HAN', 'LAN', 'NEU', 'friendHAP', 'friendLAP', 'friendHAN', 'friendLAN', 'friendNEU', 'subID'])

  combine = [jpYHAPFlat, 
             jpYLAPFlat, 
             jpYHANFlat, 
             jpYLANFlat, 
             jpYNEUFlat, 
             jpFriendHAPPropFlatPerc, 
             jpFriendLAPPropFlatPerc, 
             jpFriendHANPropFlatPerc, 
             jpFriendLANPropFlatPerc, 
             jpFriendNEUPropFlatPerc, 
             jpSub]

  dfJP = pd.DataFrame(np.array([combine[0], combine[1], combine[2], combine[3], combine[4], combine[5],combine[6], combine[7], combine[8], combine[9], combine[10]]).T,
                      columns=['HAP', 'LAP', 'HAN', 'LAN', 'NEU', 'friendHAP', 'friendLAP', 'friendHAN', 'friendLAN', 'friendNEU', 'subID'])


  return dfUS, dfJP




def save_dataframe_for_between_culture_comparison(dfUS, dfJP, output_path):
  '''
  Input:
    dfUS: dataframe with US data (output of clean_data)
    dfJP: dataframe with JP data (output of clean_data)
    output_path: path to output dataframe (REQUIRES .csv)
  Output:
    dfAll: dataframe with data from both countries, ready for between culture comparison analyses
  '''

  # Store number of tweets per user into a list

  culture = ['US']*len(dfUS['subID']) + ['JP']*len(dfJP['subID'])

  combine = [list(dfUS['HAP'])+list(dfJP['HAP']),
            list(dfUS['LAP'])+list(dfJP['LAP']),
            list(dfUS['HAN'])+list(dfJP['HAN']),
            list(dfUS['LAN'])+list(dfJP['LAN']),
            list(dfUS['NEU'])+list(dfJP['NEU']),
            list(dfUS['friendHAP'])+list(dfJP['friendHAP']),
            list(dfUS['friendLAP'])+list(dfJP['friendLAP']),
            list(dfUS['friendHAN'])+list(dfJP['friendHAN']),
            list(dfUS['friendLAN'])+list(dfJP['friendLAN']),
            list(dfUS['friendNEU'])+list(dfJP['friendNEU']),
            list(dfUS['subID'])+list(dfJP['subID']),
            culture]

  dfAll = pd.DataFrame(np.array([combine[0], combine[1], combine[2], combine[3], combine[4], combine[5],combine[6], combine[7], combine[8], combine[9], combine[10], combine[11]]).T,
                      columns=['HAP', 'LAP', 'HAN', 'LAN', 'NEU', 'friendHAP', 'friendLAP', 'friendHAN', 'friendLAN', 'friendNEU', 'subID', 'culture'])

  dfAll.to_csv(output_path, index=False)

  return dfAll



def save_dataframe_for_within_culture_comparison(dfInput, output_path):
  '''
  Input:
    dfInput: dataframe with data (output of clean_data)
    output_path: path to output dataframe (REQUIRES .csv)
  Output:
    dfAll: dataframe with data from both countries, ready for between culture comparison analyses
  '''

  n = len(dfInput['subID'])

  Y = list(dfInput['HAP']) + list(dfInput['LAP']) + list(dfInput['HAN']) + list(dfInput['LAN']) + list(dfInput['NEU'])
  dhap = [1]*1*n + [0]*4*n
  dlap = [0]*1*n + [1]*n + [0]*3*n
  dhan = [0]*2*n + [1]*n + [0]*2*n
  dlan = [0]*3*n + [1]*n + [0]*1*n
  dneu = [0]*4*n + [1]*1*n
  xfriendHAP = list(dfInput['friendHAP'])*5
  xfriendLAP = list(dfInput['friendLAP'])*5
  xfriendHAN = list(dfInput['friendHAN'])*5
  xfriendLAN = list(dfInput['friendLAN'])*5
  xfriendNEU = list(dfInput['friendNEU'])*5
  subID = list(dfInput['subID'])*5


  dfAlldict = {'Y':Y, 'dhap':dhap, 'dlap':dlap, 'dhan':dhan, 'dlan':dlan, 'dneu':dneu,
                 'xfriendHAP':xfriendHAP, 'xfriendLAP':xfriendLAP, 'xfriendHAN':xfriendHAN, 
                  'xfriendLAN':xfriendLAN, 'xfriendNEU':xfriendNEU,
                 'subID':subID}

  dfAll = pd.DataFrame(data=dfAlldict)
  
  dfAll.to_csv(output_path, index=False)

  return dfAll



if __name__ == '__main__':
  us_path = sys.argv[1]
  jp_path = sys.argv[2]
  dataframe_between_culture_path = sys.argv[3]
  dataframe_US_within_culture_path = sys.argv[4]
  dataframe_JP_within_culture_path = sys.argv[5]

  dfUS, dfJP = clean_data(us_path, jp_path)
  dfAll = save_dataframe_for_between_culture_comparison(dfUS, dfJP, dataframe_between_culture_path)
  dfAll = save_dataframe_for_within_culture_comparison(dfUS, dataframe_US_within_culture_path)
  dfAll = save_dataframe_for_within_culture_comparison(dfJP, dataframe_JP_within_culture_path)

