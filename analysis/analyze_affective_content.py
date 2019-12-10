import numpy as np
import pickle
import pandas as pd
import csv
from scipy.stats import ttest_ind
from scipy.stats.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import chi2_contingency


def analyze_affective_content(us_path, jp_path, overall_plot_path, separated_plot_path):
  '''
  Analyze affective content of US and JP user tweets.
  Save bar plot of overall affective content and bar plot of separated (pure and mixed) affective content.

  Input:
    us_path: file path to US .pkl file to analyze (string)
    jp_path: file path to JP .pkl file to analyze (string)
    overall_plot_path: file path to save bar plot of overall affective content (string; REQUIRE .pdf extension)
    separated_plot_path: file path to save bar plot of separated (pure and mixed) affective content (string; REQUIRE .pdf extension)
  Output:
    None
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

  # Plot
  means_US = (USHAPmean, USLAPmean, USLANmean, USHANmean)
  means_AS = (ASHAPmean, ASLAPmean, ASLANmean, ASHANmean)

  plot2 = plt.figure()
  n_groups = 4
  fig, ax = plt.subplots(figsize=(10, 4))
  index = np.arange(n_groups)
  bar_width = 0.35
  opacity = 0.7
   
  rects1 = plt.bar(index, means_US, bar_width,
                   alpha=opacity,
                   color = 'black',
                   label='United States',
                  )
                   
   
  rects2 = plt.bar(index + bar_width, means_AS, bar_width,
                   alpha=opacity,
                   color="lightgrey",
                   edgecolor = "black",
                   label='Japan',
                  )
  ax.set_ylim(bottom=0, top=50)  # return the current ylim
  plt.xlabel('Overall', size='16', labelpad=10)
  plt.ylabel('Percentage of original tweets', size='16', labelpad=10)
  plt.xticks(index + bar_width, ('HAP','LAP','LAN','HAN'), size='14')
  plt.yticks(size='14')
  plt.legend(prop={'size': 12}, loc='upper left')
  plt.tight_layout()

  plt.savefig(overall_plot_path, bbox_inches='tight', pad_inches=0.1)
  plt.show()


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

  for i in range(len(usSub)):
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
          
  usHAPmean = usHAPsum*100.0/len(usSub)
  usLAPmean = usLAPsum*100.0/len(usSub)
  usHANmean = usHANsum*100.0/len(usSub)
  usLANmean = usLANsum*100.0/len(usSub)
  usNEUmean = usNEUsum*100.0/len(usSub)
  usHAPHANmean = usHAPHANsum*100.0/len(usSub)
  usHAPLANmean = usHAPLANsum*100.0/len(usSub)
  usLAPHANmean = usLAPHANsum*100.0/len(usSub)
  usLAPLANmean = usLAPLANsum*100.0/len(usSub)



  jpHAPsum = 0
  jpLAPsum = 0
  jpHANsum = 0
  jpLANsum = 0
  jpNEUsum = 0
  jpHAPHANsum = 0
  jpHAPLANsum = 0
  jpLAPHANsum = 0
  jpLAPLANsum = 0

  for i in range(len(jpSub)):
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
          
  jpHAPmean = jpHAPsum*100.0/len(jpSub)
  jpLAPmean = jpLAPsum*100.0/len(jpSub)
  jpHANmean = jpHANsum*100.0/len(jpSub)
  jpLANmean = jpLANsum*100.0/len(jpSub)
  jpNEUmean = jpNEUsum*100.0/len(jpSub)
  jpHAPHANmean = jpHAPHANsum*100.0/len(jpSub)
  jpHAPLANmean = jpHAPLANsum*100.0/len(jpSub)
  jpLAPHANmean = jpLAPHANsum*100.0/len(jpSub)
  jpLAPLANmean = jpLAPLANsum*100.0/len(jpSub)


  # Plot
  means_US = (usHAPmean, usLAPmean, usLANmean, usHANmean, usHAPLANmean, usHAPHANmean, usLAPLANmean, usLAPHANmean)
  means_AS = (jpHAPmean, jpLAPmean, jpLANmean, jpHANmean, jpHAPLANmean, jpHAPHANmean, jpLAPLANmean, jpLAPHANmean)

  plot2 = plt.figure()
  n_groups = 8
  fig, ax = plt.subplots(figsize=(10, 4))
  index = np.arange(n_groups)
  bar_width = 0.35
  opacity = 0.7
   
  rects1 = plt.bar(index, means_US, bar_width,
                   alpha=opacity,
                   color = 'black',
                   label='United States',
                  )
                   
   
  rects2 = plt.bar(index + bar_width, means_AS, bar_width,
                   alpha=opacity,
                   color = 'lightgrey',
                   edgecolor = 'black',
                   label='Japan',
                  )
   
  ax.set_ylim(bottom=0, top=50)  # return the current ylim
  plt.xlabel('Pure                                                      Mixed', size='16',labelpad=10)
  plt.ylabel('Percentage of original tweets', size='16', labelpad=10)
  plt.xticks(index + bar_width, ('HAP','LAP','LAN','HAN',
                                 'HAP-LAN', 'HAP-HAN', 'LAP-LAN', 'LAP-HAN'), 
             size='14')
  plt.legend(prop={'size': 12}, loc='upper left')
  plt.yticks(size='14')
  plt.tight_layout()

  plt.savefig(separated_plot_path, bbox_inches='tight', pad_inches=0.1)
  plt.show()




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

