#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# multiproc_sums.py
"""A program that reads integer values from a CSV file and writes out their
sums to another CSV file, using multiple processes if desired.
"""

import csv
import multiprocessing
import optparse
import sys

import nltk
import re
import string
import operator
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
from IPython.core.debugger import Tracer
import os
import glob
import pandas as pd
import sys
import getopt
import time

# Tracer()()
file_pronouns = '../Input/RequiredFiles/pronouns.txt'
#file1 = '../Input/raw_st_johns_wortMergedFinalAnn.csv'
# file1 ='../Input/EchinaceaRecords.csv'


# file1 = '../No_kava/Final_Training/NewTrainingSet_6880Without_No.csv'
# output_file = '../Output/output_new_without_no_training_6880.csv'
#output_file = '/media/matrika/Data/Dietary Supplement/Output/output_test_Ann3.csv'
file_emotions = '../Input/RequiredFiles/contentwordlist.5000.txt'

##########################################################################################
## 0 no, dont read word lists from file. Creates word list files
## 1 yes, read words lists from file. Does not create word list files

read_word_lists_from_file = 1

#########################################################################################

stemmer = PorterStemmer()

########################################################################################

from_file_all_twitter_clients = []
from_file_list_automatic_freq_no = []
from_file_list_automatic_freq_yes = []
from_file_list_user_automatic_freq_no = []
from_file_list_user_automatic_freq_yes = []

#########################################################################################
##'/home/purdueml/Desktop/twitter_nih/word_lists/'
if read_word_lists_from_file == 1:

    f_zz_auto_yes_list = open('../word_lists/auto_yes_list_file.txt','r')
    f_zz_auto_no_list = open('../word_lists/auto_no_list_file.txt','r')
    # f_zz_twitter_client_list = open('../word_lists/twitter_client_list_file.txt','r')
    f_user_auto_no_list = open('../word_lists/User_auto_no_list_file.txt','r')
    f_user_auto_yes_list = open('../word_lists/User_auto_yes_list_file.txt','r')





    for word in f_zz_auto_yes_list.readlines():
        word = word.replace('\n','')
        from_file_list_automatic_freq_yes.append(word)

    for word in f_zz_auto_no_list.readlines():
        word = word.replace('\n','')
        from_file_list_automatic_freq_no.append(word)

    # for word in f_zz_twitter_client_list.readlines():
    #     word = word.replace('\n','')
    #     from_file_all_twitter_clients.append(word)

    for word in f_user_auto_no_list.readlines():
        word = word.replace('\n','')
        from_file_list_user_automatic_freq_no.append(word)

    for word in f_user_auto_yes_list.readlines():
        word = word.replace('\n','')
        from_file_list_user_automatic_freq_yes.append(word)
          
    f_zz_auto_yes_list.close() 
    f_zz_auto_no_list.close()
    f_user_auto_no_list.close()
    f_user_auto_yes_list.close()
    # f_zz_twitter_client_list.close()
    
########################################################

def func_tags_NNP(tag_sequence):
    count_nnp = 0
    for tup in tag_sequence:
        if tup[1] == 'NNP':
            count_nnp = count_nnp + 1
    return count_nnp

##########################################################################################
def func_tags_PRP(tag_sequence):
    count_prp = 0
    for tup in tag_sequence:
        if tup[1] == 'PRP' or tup[1] == 'PRP$':
            count_prp = count_prp + 1
    return count_prp

##########################################################################################

if read_word_lists_from_file == 1:
    # all_twitter_clients = from_file_all_twitter_clients[:] 
    list_automatic_freq_no = from_file_list_automatic_freq_no[:]
    list_user_automatic_freq_no = from_file_list_user_automatic_freq_no[:]
    list_user_automatic_freq_yes = from_file_list_user_automatic_freq_yes[:]
    list_automatic_freq_yes = from_file_list_automatic_freq_yes[:]
    # print all_twitter_clients 
    # print list_automatic_freq_no
    # print list_user_automatic_freq_no
    # #x = raw_input()
    # print list_automatic_freq_yes

    #x = raw_input()


##########################################################################################

def automatic_freq_no(text):
    count_words = 0
    
    for word in text:
        word1 = stemmer.stem(word.lower())
        if word1 in list_automatic_freq_no:
            count_words = count_words + 1
    return count_words
    
########################################################################################
##########################################################################################

def user_automatic_freq_no(text):
    count_words = 0
    for word in text:
        word1 = stemmer.stem(word.lower())
        if word1 in list_user_automatic_freq_no:
            count_words = count_words + 1
    return count_words


def user_automatic_freq_yes(text):
    count_words = 0

    for word in text:
        word1 = stemmer.stem(word.lower())
        if word1 in list_user_automatic_freq_yes:
            count_words = count_words + 1
    return count_words

########################################################################################

def automatic_freq_yes(text):
    count_words = 0
    
    for word in text:
        word1 = stemmer.stem(word.lower())
        if word1 in list_automatic_freq_yes:
            count_words = count_words + 1
    return count_words


##########################################################################################

def func_No_freq_terms(text):
    count_words = 0
    no_freq_terms = ['depression', 'offers','natural','looking', 'remedies','choose','price','get','special','compare',
                     'body','recommended','save','effective','offer','sale', 'deal','ebay','stock','nutrition','selling',
                     'quality','wellness','miss','savings','active','prices','relieve','deals','calming','$','youtube',
                     'buy','pay','bionutrients','naturally', 'disorders','reddit']
    for word in text:
        if word in no_freq_terms:
            count_words = count_words + 1
    return count_words
##########################################################################################
##########################################################################################

list_common_word_username_get = open('../word_lists/list_common_word_username.txt','r')
from_file_list_common_word_username=[]
for word in list_common_word_username_get.readlines():
        word = word.replace('\n','')
        from_file_list_common_word_username.append(word)


def func_user_No_freq_terms(text):
    count_words = 0
    # no_freq_terms = ['offers','price',
    #                 'recommended','save','offer','sale', 'deal','ebay','stock','nutrition','selling',
    #                  'quality','wellness','savings','prices','deals','$','youtube',
    #                  'buy','pay','bionutrients','naturally', 'disorders','store','orgnization']
    for word in text:
        if word in from_file_list_common_word_username:
            count_words = count_words + 1
    return count_words

##########################################################################################

def func_Yes_freq_terms(text):
    count_words = 0
    yes_freq_terms = ['helpful', 'wonders','good','cat','enough','said','jesus','mood','started','thoughts','quite','they','feel',
                      'aware','idea','recommended','well','crazy', 'effect', 'helps', 'ever','react', 'effects','side','quit',
                      'might', 'placebo', 'mild', 'right','stuff', 'trying', 'meds', 'felt','happy', 'hopefully', 'worse',
                      'much', 'depressed', 'possibly', 'ago','past', 'sleep', 'pills', 'something', 'thinking','this', 'tried',
                      'helped', 'found', 'issues','talk', 'girl', 'helping', 'work', 'my', 'actually', 'seems', 'boy', 'better',
                      'relief', 'badly', 'since', 'going','took','coffee', 'lol', 'relaxation', 'little', 'hello', 'anxiety',
                      'caffeine', 'sunlight', 'root', 'thank', 'shit', 'feeling', 'worked', 'think', 'though', 'life', 'sun',
                      'stress', 'bit', 'calming' ]
    for word in text:
        if word in yes_freq_terms:
            count_words = count_words + 1
    return count_words

        
##########################################################################################
def func_first_person_PRP_terms(text):
    count_words = 0
    first_person_terms = ['I','i','we','We','WE','me','Me','ME','Us','us','US','my','My','MY','our','Our','OUR','mine','Mine','MINE','ours','Ours','OURS']
    for word in text:
        if word in first_person_terms:
            count_words = count_words + 1
    return count_words
        
##########################################################################################
def func_second_person_PRP_terms(text):
    count_words = 0
    second_person_terms = ['you','You','YOU','your','Your','YOUR','yours','Yours','YOURS']
    for word in text:
        if word in second_person_terms:
            count_words = count_words + 1
    return count_words
        
##########################################################################################
def func_third_person_PRP_terms(text):
    count_words = 0
    third_person_terms = ['he','she','it','they','him','her','them','his','her','hers','its','their','theirs',
                     'HE','SHE','IT','THEY','HIM','HER','THEM','HIS','HER','HERS','ITS','THEIR','THEIRS',
                 'He','She','It','They','Him','Her','Them','His','Her','Hers','Its','Their','Theirs']
    for word in text:
        if word in third_person_terms:
            count_words = count_words + 1
    return count_words
        

##########################################################################################
#all_twitter_clients

# def get_twitter_client(twitter_client):
#     index = 0
#     for item in all_twitter_clients:
#         if item == twitter_client:
#             return index
#         else:
#             index = index + 1

# ##########################################################################################
# #

def get_all_user_ids(user_id,all_user_ids):
    index = 0
    user_id = int(user_id)
    # print str(all_user_ids)
    for item in all_user_ids:
        if item == user_id:
            return index
        else:
            index = index + 1



def func_tags_ulr_Count(tag_sequence):
    counturl = 0
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tag_sequence)
    counturl=len(urls)

    return counturl


def get_parsed_tweet_id(file):
    with open(file,'w+') as f:
        # Tracer()()
        if os.stat(f.name).st_size == 0:
            return set()  
        else:
            df = pd.read_csv(f, sep=",",header=None)
            # Tracer()()
            return set(df[0].tolist()) 

def get_parsed_chunk_list(file):
    with open(file,'w+') as f:
        # Tracer()()
        if os.stat(f.name).st_size == 0:
            return set()  
        else:
            # df = pd.read_csv(file, sep=",",header=None)
            ls = [line.strip() for line in f.readlines()]
            # Tracer()()
            return set(sorted(ls)) 
def walk(rootdir):
    """Generate full paths to all files in a directory."""
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            yield os.path.join(dirpath, filename)         


#########################################################################################
##'/home/purdueml/Desktop/twitter_nih/word_lists/'
    
            
    
##########################################################################################
f_pronouns = open(file_pronouns, 'r')
f_emotions = open(file_emotions, 'r')
 
temp_pronouns = f_pronouns.read()
f_pronouns.close()
list_pronouns = word_tokenize(temp_pronouns)

list_emotions = []
temp_emotions = f_emotions.read()
f_emotions.close()
list_emotions_temp = word_tokenize(temp_emotions)
for item in list_emotions_temp:
    item1 = item.lower()
    list_emotions.append(stemmer.stem(item1))


# Saved the chunk that has beeb parsed in to this list


NUM_PROCS = multiprocessing.cpu_count()

def make_cli_parser():
    """
    Make the command line interface parser.
    """
    usage = "\n\n".join(["python %prog INPUT_CSV OUTPUT_CSV",
            __doc__,
            """
ARGUMENTS:
    INPUT_CSV: an input CSV file with rows of numbers
    OUTPUT_CSV: an output file that will contain the sums\
"""])
    cli_parser = optparse.OptionParser(usage)
    cli_parser.add_option('-n', '--numprocs', type='int',
            default=NUM_PROCS,
            help="Number of processes to launch [DEFAULT: %default]")
    return cli_parser

class CSVWorker(object):
    def __init__(self, numprocs, infile, outfile,all_user_ids,tweet_id_seen):
        self.numprocs = numprocs
        self.infile = open(infile)
        self.outfile = outfile
        self.in_csvfile = csv.reader(self.infile)
        self.all_user_ids = all_user_ids
        self.tweet_id_seen = tweet_id_seen
        self.inq = multiprocessing.Queue()
        self.outq = multiprocessing.Queue()

        self.pin = multiprocessing.Process(target=self.parse_input_csv, args=())
        self.pout = multiprocessing.Process(target=self.write_output_csv, args=())
        self.ps = [ multiprocessing.Process(target=self.sum_row, args=())
                        for i in range(self.numprocs)]

        self.pin.start()
        self.pout.start()
        for p in self.ps:
            p.start()

        self.pin.join()
        i = 0
        for p in self.ps:
            p.join()
            print "Done", i
            i += 1

        self.pout.join()
        self.infile.close()

    def parse_input_csv(self):
            """Parses the input CSV and yields tuples with the index of the row
            as the first element, and the integers of the row as the second
            element.

            The index is zero-index based.

            The data is then sent over inqueue for the workers to do their
            thing.  At the end the input process sends a 'STOP' message for each
            worker.
            """
            for i, row in enumerate(self.in_csvfile):
                # if tweet_id is seen before, pass it
                if row[8] in self.tweet_id_seen:
                    continue
                row = [ entry for entry in row ]
                # Tracer()()
                self.inq.put( (i, row) )

            for i in range(self.numprocs):
                self.inq.put("STOP")

    def featurize(self, temp):

        '''
            Featurize current tweet
            Parameter: row in the csv file, row must have 12 fields
            return
        '''
        row = []
        tweet_string = ' '.join(temp[11:])
       
        tweet_string = re.sub(r'[^\x00-\x7f]',r' ',tweet_string)
        # Extract username.
        
        user_name = temp[10]#.split(' - ')
        # Tracer()()

        if user_name.isspace() or user_name == None:
            usernametext = '  '
        else:
            user_namelst = re.sub(r'[^\x00-\x7f]',r' ',user_name)
            usernametext = word_tokenize(user_namelst)
         
        
        text = word_tokenize(tweet_string)
        tag_sequence = nltk.pos_tag(text)

        feature_pronouns_count = 0
        feature_emotions_count = 0
        for token in text:
            if token in list_pronouns:
                feature_pronouns_count = feature_pronouns_count + 1
            token1 = stemmer.stem(token)
            if token1 in list_emotions:
                feature_emotions_count = feature_emotions_count + 1
        
        # Add tweet_id
        row.append(str(temp[8]))
        
        # Add followers count
        row.append(str(0))

        # Add friends count
        # Tracer()()
        row.append(str(0))

        # Add hash tag count
        row.append(str(0))

        # Add pronouns count
        row.append(str(feature_pronouns_count))

        # Add emotions count
        row.append(str(feature_emotions_count))

        # Add number of  word of tweets
        row.append(str(len(text)))

        # Add number of unique word of tweets
        row.append(str(len(set(text))))

        # Add NNP_tags
        row.append(str(func_tags_NNP(tag_sequence)))

        # Add PRP_tags
        row.append(str(func_tags_PRP(tag_sequence)))

        # Add Url_count
        row.append(str(func_tags_ulr_Count(tweet_string)))
        
        # Add func_first_person_PRP_terms
        row.append(str(func_first_person_PRP_terms(text)))

        # Add second_person_PRP
        row.append(str(func_second_person_PRP_terms(text)))

        # Add third_person_PRP
        row.append(str(func_third_person_PRP_terms(text)))

        # Add No_freq_terms
        row.append(str(func_No_freq_terms(text)))

        # Add Yes_freq_terms
        row.append(str(func_Yes_freq_terms(text)))

        # Add auto_Yes_freq_terms
        row.append(str(automatic_freq_yes(text)))

        # Add auto_No_freq_terms
        row.append(str(automatic_freq_no(text)))

        # Add User_No_freq_terms
        row.append(str(func_user_No_freq_terms(usernametext)))

        # Add User_auto_No_freq_terms
        row.append(str(user_automatic_freq_no(usernametext)))

        # Add User_auto_Yes_freq_terms
        row.append(str(user_automatic_freq_yes(usernametext)))

        # Add twitter_client
        row.append(str(0))

        # Add user_id
        row.append(str(get_all_user_ids(temp[9],self.all_user_ids)))
        
        # Add class
        row.append(' ')

        return row

        
    def sum_row(self):
        """
        Workers. Consume inq and produce answers on outq
        """
        tot = 0
        for i, row in iter(self.inq.get, "STOP"):
                self.outq.put( (i, self.featurize(row)) )
        self.outq.put("STOP")

    
    def write_output_csv(self):
        """
        Open outgoing csv file then start reading outq for answers
        Since I chose to make sure output was synchronized to the input there
        is some extra goodies to do that.

        Obviously your input has the original row number so this is not
        required.
        """
        cur = 0
        stop = 0
        buffer = {}
        # For some reason csv.writer works badly across processes so open/close
        # and use it all in the same process or else you'll have the last
        # several rows missing
        outfile = open(self.outfile, "r+")
        self.out_csvfile = csv.writer(outfile)

        #Keep running until we see numprocs STOP messages
        for works in range(self.numprocs):
            for i, val in iter(self.outq.get, "STOP"):
                # verify rows are in order, if not save in buffer
                if i != cur:
                    buffer[i] = val
                else:
                    #if yes are write it out and make sure no waiting rows exist
                    self.out_csvfile.writerow(val)
                    cur += 1
                    while cur in buffer:
                        self.out_csvfile.writerow(buffer[cur])
                        del buffer[cur]
                        cur += 1

        outfile.close()

def main(argv):
    cli_parser = make_cli_parser()
    opts, args = cli_parser.parse_args(argv)
    if len(args) != 2:
        cli_parser.error("Please provide an input file and output file.")
    df = pd.read_csv(args[0], sep=',', header=None)
    all_user_ids = set(df[9].tolist())
    tweet_id_seen = get_parsed_tweet_id(args[1])
    # print len(all_user_ids)
    # Tracer()()

    c = CSVWorker(opts.numprocs, args[0], args[1],all_user_ids,tweet_id_seen)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv[1:])
    print("---preprocess  %s seconds ---" % (time.time() - start_time))