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


########################## Statistics used in paper ###############################################
def cohensh(p1,p2):
  '''
  Given two proportions, calculates Cohen's h.
  Input:
    p1: proportion 1
    p2: proportion 2
  Output:
    Cohen's h
  '''
  h = 2*(np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
  return abs(h)



def chisquare(count1, count2, total1, total2):
  '''
  Given two counts of incidences and total counts, determine chi-squre statistic.
  Input:
    count1: count of incidences in pool1
    count2: count of incidences in pool2
    total1: total nunber of data points in poo1
    total2: total nunber of data points in pool2
  Output:
    stat: chi-square statistic
    p: p-value
    dof: degrees of freedom
    expected: matrix of expected counts
  '''
  p1_nones = count1
  p2_nones = count2
  p1_nzeros = total1-count1
  p2_nzeros = total2-count2
  obs = np.array([[p1_nones, p1_nzeros], [p2_nones, p2_nzeros]])
  stat, p, dof, expected = chi2_contingency(obs)
  return stat, p, dof, expected

#####################################################################################################


def preprocess_for_affective_content(us_path, jp_path, output_file_path):
  '''
  Analyze affective content of US and JP user tweets.
  Save bar plot of overall affective content and bar plot of separated (pure and mixed) affective content.

  Input:
    us_path: file path to US .pkl file to analyze (string)
    jp_path: file path to JP .pkl file to analyze (string)
    output_file_path: file path to output file (string; REQUIRE .csv)
  Output:
    None
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



  # Store number of tweets
  usnumTweets = len(usFriendHAPPropFlat)
  jpnumTweets = len(jpFriendHAPPropFlat)


  ######################### Users affective content: Overall ##################################################
  # Calculate percentages of each
  USHAPmean = np.mean(usYHAPFlat)*100
  USLAPmean = np.mean(usYLAPFlat)*100
  USHANmean = np.mean(usYHANFlat)*100
  USLANmean = np.mean(usYLANFlat)*100
  USNEUmean = np.mean(usYNEUFlat)*100
  ASHAPmean = np.mean(jpYHAPFlat)*100
  ASLAPmean = np.mean(jpYLAPFlat)*100
  ASHANmean = np.mean(jpYHANFlat)*100
  ASLANmean = np.mean(jpYLANFlat)*100
  ASNEUmean = np.mean(jpYNEUFlat)*100


  ######################### Users affective content: Separated (Pure and Mixed) ##########################################

  # Calculate percentages of each
  usHAPsum = 0
  usLAPsum = 0
  usHANsum = 0
  usLANsum = 0
  usNEUsum = 0
  usHAPHANsum = 0
  usHAPLANsum = 0
  usLAPHANsum = 0
  usLAPLANsum = 0

  for i in range(usnumTweets):
      if usYHAPFlat[i]:
          if usYHANFlat[i]:
              usHAPHANsum += 1
          elif usYLANFlat[i]:
              usHAPLANsum += 1
          else:
              usHAPsum += 1
      elif usYLAPFlat[i]:
          if usYHANFlat[i]:
              usLAPHANsum += 1
          elif usYLANFlat[i]:
              usLAPLANsum += 1
          else:
              usLAPsum += 1
      elif usYHANFlat[i]:
          usHANsum += 1
      elif usYLANFlat[i]:
          usLANsum += 1
      else:
          usNEUsum += 1
          
  usHAPmean = usHAPsum*100.0/usnumTweets
  usLAPmean = usLAPsum*100.0/usnumTweets
  usHANmean = usHANsum*100.0/usnumTweets
  usLANmean = usLANsum*100.0/usnumTweets
  usNEUmean = usNEUsum*100.0/usnumTweets
  usHAPHANmean = usHAPHANsum*100.0/usnumTweets
  usHAPLANmean = usHAPLANsum*100.0/usnumTweets
  usLAPHANmean = usLAPHANsum*100.0/usnumTweets
  usLAPLANmean = usLAPLANsum*100.0/usnumTweets



  jpHAPsum = 0
  jpLAPsum = 0
  jpHANsum = 0
  jpLANsum = 0
  jpNEUsum = 0
  jpHAPHANsum = 0
  jpHAPLANsum = 0
  jpLAPHANsum = 0
  jpLAPLANsum = 0

  for i in range(jpnumTweets):
      if jpYHAPFlat[i]:
          if jpYHANFlat[i]:
              jpHAPHANsum += 1
          elif jpYLANFlat[i]:
              jpHAPLANsum += 1
          else:
              jpHAPsum += 1
      elif jpYLAPFlat[i]:
          if jpYHANFlat[i]:
              jpLAPHANsum += 1
          elif jpYLANFlat[i]:
              jpLAPLANsum += 1
          else:
              jpLAPsum += 1
      elif jpYHANFlat[i]:
          jpHANsum += 1
      elif jpYLANFlat[i]:
          jpLANsum += 1
      else:
          jpNEUsum += 1
          
  jpHAPmean = jpHAPsum*100.0/jpnumTweets
  jpLAPmean = jpLAPsum*100.0/jpnumTweets
  jpHANmean = jpHANsum*100.0/jpnumTweets
  jpLANmean = jpLANsum*100.0/jpnumTweets
  jpNEUmean = jpNEUsum*100.0/jpnumTweets
  jpHAPHANmean = jpHAPHANsum*100.0/jpnumTweets
  jpHAPLANmean = jpHAPLANsum*100.0/jpnumTweets
  jpLAPHANmean = jpLAPHANsum*100.0/jpnumTweets
  jpLAPLANmean = jpLAPLANsum*100.0/jpnumTweets


  ######################### Save ##########################################
  affect = ['HAP', 'LAP', 'HAN', 'LAN', 
          'HAP', 'LAP', 'HAN', 'LAN', 
          'HAPHAN', 'HAPLAN', 'LAPHAN', 'LAPLAN',  
          'HAP', 'LAP', 'HAN', 'LAN', 
          'HAP', 'LAP', 'HAN', 'LAN', 
          'HAPHAN', 'HAPLAN', 'LAPHAN', 'LAPLAN']
  culture = ['US', 'US', 'US', 'US',
             'US', 'US', 'US', 'US',
             'US', 'US', 'US', 'US',
             'JP', 'JP', 'JP', 'JP',
             'JP', 'JP', 'JP', 'JP',
             'JP', 'JP', 'JP', 'JP']
  affecttype = ['All', 'All', 'All', 'All',
               'Pure', 'Pure', 'Pure', 'Pure',
               'Mixed', 'Mixed', 'Mixed', 'Mixed',
               'All', 'All', 'All', 'All',
               'Pure', 'Pure', 'Pure', 'Pure',
               'Mixed', 'Mixed', 'Mixed', 'Mixed']
  value = [USHAPmean, USLAPmean, USHANmean, USLANmean,
           usHAPmean, usLAPmean, usHANmean, usLANmean, 
           usHAPHANmean, usHAPLANmean, usLAPHANmean, usLAPLANmean,
           ASHAPmean, ASLAPmean, ASHANmean, ASLANmean,
           jpHAPmean, jpLAPmean, jpHANmean, jpLANmean, 
           jpHAPHANmean, jpHAPLANmean, jpLAPHANmean, jpLAPLANmean,]

  dfAll = pd.DataFrame(np.array([affect, culture, affecttype, value]).T,
                      columns = ['affect', 'culture', 'type', 'value'])

  dfAll.to_csv(output_file_path)



if __name__ == '__main__':
    preprocess_for_affective_content(sys.argv[1], sys.argv[2], sys.argv[3])

