# coding: utf-8
import numpy as np
import pandas as pd
import csv
import emoji
import re
import subprocess
import shlex
import os.path
import sys

def run_jp_sentistrength(input_file_path, output_folder_path, sentistrength_path, sentistrength_dictionary_path):
    '''
    Uses English SentiStrength to tag texts for sentiment.
    Output file will be saved under [processed_path]0.txt.
    If number of texts is larger, wait a little for program to complete.

    Input:
        input_file_path: file path to the file with raw text (REQUIRES ending with '.csv')
        output_folder_path: file path to folder where you want to save your processed text file (REQUIRES ending with '/')
        sentistrength_path: file path to the Japanese SentiStrength program
        sentistrength_dictionary_path: file path to the folder of the Japanese SentiStrength dictionary files
    Output:
        None
    '''

    ## Load tweets dataframe
    dfG = pd.read_csv(input_file_path)


    ################ PROCESSING APPLICABLE TO EN SENTISTRENGTH ################################################
    
    # Process each tweet
    dfMessages = dfG['message']
    with open(output_folder_path + "output_messages.txt", 'w') as f:
        for m in dfMessages:
            if not isinstance(m,str):
                m = str(m)
            linewritelist = re.findall(u'(?:[\ud800-\udbff][\udc00-\udfff])|.', m.decode('utf-8','replace'))
            linewrite = ''.join('\t'+c+'\t' if c in emoji.UNICODE_EMOJI else c for c in linewritelist)
            linewrite = linewrite.replace('\n',' ').replace('\r',' ').replace('\t',' ')
            linewrite.rstrip()
    #         linewrite = linewrite.replace(' ','+')
            linewrite = linewrite+'\n'
            f.write(linewrite.encode('utf-8'))
    f.close()


    ######################## APPLY SENTISTRENGTH to each status ####################################
    ## Modified from: http://sentistrength.wlv.ac.uk/jkpop/ClassifyCommentSentiment.py
    FileToClassify = output_folder_path + "output_messages.txt"

    #Test file locations and quit if anything not found
    if not os.path.isfile(sentistrength_path):
        print("SentiStrength not found at: ", sentistrength_path)
        sys.exit()
    if not os.path.isdir(sentistrength_dictionary_path):
        print("SentiStrength langauge files folder not found at: ", sentistrength_dictionary_path)
        sys.exit()
    if not os.path.isfile(FileToClassify):
        print("File to classify not found at: ", FileToClassify)

    print("Running SentiStrength on file " + FileToClassify + " with command:")
    cmd = 'java -jar "' + sentistrength_path + '" sentidata "' + sentistrength_dictionary_path + '" input "' + FileToClassify + '" utf8'
    print(cmd)
    p = subprocess.Popen(shlex.split(cmd),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    classifiedSentimentFile = os.path.splitext(FileToClassify)[0] + "_out.txt"
    print("Finished! The results will be in:\n" + classifiedSentimentFile)


if __name__ == '__main__':
    run_jp_sentistrength(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
