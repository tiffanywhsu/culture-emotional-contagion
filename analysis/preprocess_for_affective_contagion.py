import numpy as np
import pickle
import pandas as pd
import csv
from scipy.stats import ttest_ind
from scipy.stats.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import chi2_contingency


def clean_data(us_path, jp_path, overall_plot_path, separated_plot_path):
  '''
  Clean pkl input files to csv dataframes to be fed into save_dataframe_for_between_culture_comparison 
  or save_dataframe_for_within_culture_comparison

  Input:
    us_path: file path to US .pkl file to analyze (string)
    jp_path: file path to JP .pkl file to analyze (string)
    overall_plot_path: file path to save bar plot of overall affective content (string; REQUIRE .pdf extension)
    separated_plot_path: file path to save bar plot of separated (pure and mixed) affective content (string; REQUIRE .pdf extension)
  Output:
    dfUS: cleaned dataframe for US data
    dfJP: cleaned dataframe for JP data
  '''

  # Read in data
  [usnumFriends, usUsableFriends, usYDates, usYHAP, usYLAP, usYHAN, usYLAN, usYNEU, 
  usFriendHAPProp, usFriendLAPProp, usFriendHANProp, usFriendLANProp, usFriendNEUProp, 
  usFriendHAPCounts, usFriendLAPCounts, usFriendHANCounts, usFriendLANCounts, usFriendNEUCounts] = pd.read_pickle(us_path)

  [jpnumFriends, jpUsableFriends, jpYDates, jpYHAP, jpYLAP, jpYHAN, jpYLAN, jpYNEU, 
  jpFriendHAPProp, jpFriendLAPProp, jpFriendHANProp, jpFriendLANProp, jpFriendNEUProp, 
  jpFriendHAPCounts, jpFriendLAPCounts, jpFriendHANCounts, jpFriendLANCounts, jpFriendNEUCounts] = pd.read_pickle(jp_path)


  ############################### Processing ##################################################

  # Store number of tweets per user into a list
  ussubLen = np.array([len(i) for i in usnumFriends])
  jpsubLen = np.array([len(i) for i in jpnumFriends])


  # Flatten data
  usnumFriendsFlat = sum(usnumFriends,[])
  usUsableFriendsFlat = sum(usUsableFriends,[])
  usYDatesFlat = sum(usYDates,[])
  usYHAPFlat = sum(usYHAP,[])
  usYLAPFlat = sum(usYLAP,[])
  usYHANFlat = sum(usYHAN,[])
  usYLANFlat = sum(usYLAN,[])
  usYNEUFlat = sum(usYNEU,[])
  usFriendHAPPropFlat = sum(usFriendHAPProp,[])
  usFriendLAPPropFlat = sum(usFriendLAPProp,[])
  usFriendHANPropFlat = sum(usFriendHANProp,[])
  usFriendLANPropFlat = sum(usFriendLANProp,[])
  usFriendNEUPropFlat = sum(usFriendNEUProp,[])
  usFriendHAPCountsFlat = sum(usFriendHAPCounts,[])
  usFriendLAPCountsFlat = sum(usFriendLAPCounts,[])
  usFriendHANCountsFlat = sum(usFriendHANCounts,[])
  usFriendLANCountsFlat = sum(usFriendLANCounts,[])
  usFriendNEUCountsFlat = sum(usFriendNEUCounts,[])       
  usFriendHAPPropFlatPerc = np.array(usFriendHAPPropFlat)*100
  usFriendLAPPropFlatPerc = np.array(usFriendLAPPropFlat)*100
  usFriendHANPropFlatPerc = np.array(usFriendHANPropFlat)*100
  usFriendLANPropFlatPerc = np.array(usFriendLANPropFlat)*100
  usFriendNEUPropFlatPerc = np.array(usFriendNEUPropFlat)*100


  jpnumFriendsFlat = sum(jpnumFriends,[])
  jpUsableFriendsFlat = sum(jpUsableFriends,[])
  jpYDatesFlat = sum(jpYDates,[])
  jpYHAPFlat = sum(jpYHAP,[])
  jpYLAPFlat = sum(jpYLAP,[])
  jpYHANFlat = sum(jpYHAN,[])
  jpYLANFlat = sum(jpYLAN,[])
  jpYNEUFlat = sum(jpYNEU,[])
  jpFriendHAPPropFlat = sum(jpFriendHAPProp,[])
  jpFriendLAPPropFlat = sum(jpFriendLAPProp,[])
  jpFriendHANPropFlat = sum(jpFriendHANProp,[])
  jpFriendLANPropFlat = sum(jpFriendLANProp,[])
  jpFriendNEUPropFlat = sum(jpFriendNEUProp,[])
  jpFriendHAPCountsFlat = sum(jpFriendHAPCounts,[])
  jpFriendLAPCountsFlat = sum(jpFriendLAPCounts,[])
  jpFriendHANCountsFlat = sum(jpFriendHANCounts,[])
  jpFriendLANCountsFlat = sum(jpFriendLANCounts,[])
  jpFriendNEUCountsFlat = sum(jpFriendNEUCounts,[])
  jpFriendHAPPropFlatPerc = np.array(jpFriendHAPPropFlat)*100
  jpFriendLAPPropFlatPerc = np.array(jpFriendLAPPropFlat)*100
  jpFriendHANPropFlatPerc = np.array(jpFriendHANPropFlat)*100
  jpFriendLANPropFlatPerc = np.array(jpFriendLANPropFlat)*100
  jpFriendNEUPropFlatPerc = np.array(jpFriendNEUPropFlat)*100



  # Store number of tweets and number of users
  usnumTweets = len(usFriendHAPPropFlat)
  jpnumTweets = len(jpFriendHAPPropFlat)
  usnumSubs = len(set(usSub))
  jpnumSubs = len(set(jpSub))


  ############################### Clean processed data into dataframes ##################################################
  usSub = []
  for sub in range(len(ussubLen)):
      for i in range(len(usnumFriends[sub])):
          usSub.append(sub)

  jpSub = []
  for sub in range(len(jpsubLen)):
      for i in range(len(jpnumFriends[sub])):
          jpSub.append(len(set(usSub))+sub)



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

  culture = ['US']*len(usSub) + ['JP']*len(jpSub)

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
            usSub+jpSub,
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


