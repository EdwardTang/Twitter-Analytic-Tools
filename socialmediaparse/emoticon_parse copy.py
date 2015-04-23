import os
import pandas as pd

class EmoticonDict(object):

    def __init__(self):
    
        #calls the emoticon table in the data folder in the package
        file_path = os.path.dirname(os.path.abspath(__file__))
        emoticon_key = pd.read_csv(file_path + '/data/' + 'emoticon_table.csv', encoding='utf-8', index_col=0)
        
        #intialize emoticon count
        emoticon_key['count'] = 0
        emoticon_dict = emoticon_key['count'].to_dict()
        emoticon_dict_total = emoticon_key['count'].to_dict()
        
        self.dict = emoticon_dict
        self.dict_total = emoticon_dict_total
        self.emoticon_list = emoticon_dict.keys()
        self.baskets = []
    
    def add_emoticon_count(self, text):
    
        #increments a count if an emoticon as present
        emoticon_basket = []
        for emoticon in self.emoticon_list:
  
            if emoticon in text:
                self.dict[emoticon] += 1
                emoticon_basket.append(emoticon)
            
            self.dict_total[emoticon]  += text.count(emoticon)
        self.baskets.append(emoticon_basket)
        
        return
    
    
    def create_csv(self, file='emoticon_out.csv', total=False):
    
    
        emoticon_df_total = self.dict_total.items()
        emoticon_df_unique = self.dict.items()
        
        
        
        
        emoticon_count = pd.DataFrame(emoticon_df_total, columns=['emoticon', 'total'])
        emoticon_unique = pd.DataFrame(emoticon_df_unique, columns=['emoticon', 'unique'])
        
        #emoticon_count.set_index('emoticon')
        #emoticon_unique.set_index('emoticon')
        
        emoticon_df = pd.merge(left=emoticon_count, right=emoticon_unique, on=['emoticon'])
        
        emoticon_df.sort("unique", ascending=False)
        
        #writes output file
        #possible rewrite this so it doesn't use pandas
        with open(file, 'w') as f:
            emoticon_df.to_csv(f, sep=',', index = False, encoding='utf-8')
        return
    
    
    def clear(self):
    
        for emoticon in self.dict.keys():
            self.dict[emoticon] = 0
        return
    
    
    def __str__(self):
        return str(self.dict)