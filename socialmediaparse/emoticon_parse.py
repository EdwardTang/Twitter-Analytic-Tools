__author__ = 'seandolinar'
__version__ = '0.0.0'

import os
import pandas as pd

class EmoticonDict(object):

    def __init__(self):

        #calls the emoticon table in the data folder in the package
        file_path = os.path.dirname(os.path.abspath(__file__))
        emoticon_key = pd.read_csv(file_path + '/data/' + 'emoticon_table.txt', encoding='utf-8', index_col=0)
        
        #intialize emoticon count
        emoticon_key['count'] = 0
        emoticon_dict = emoticon_key['count'].to_dict()
        emoticon_dict_total = emoticon_key['count'].to_dict()

        self.dict = emoticon_dict
        self.dict_total = emoticon_dict_total
        self.emoticon_list = emoticon_dict.keys()
        self.baskets = []
    
    def add_emoticon_count(self,text):
        #increments a count if an emoticon as present
        emoticon_basket = []
        for emoticon in self.emoticon_list:
            #if emoticon in text:
            if text.find(emoticon):
                self.dict[emoticon] +=1
                emoticon_basket.append(emoticon)
            
            self.dic_total[emoticon] += text.count(emoticon)
        self.baskets.append(emoticon_basket)
        
        return
        