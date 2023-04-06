import pandas as pd
import numpy 
import time
import json 
import os

"""
This class player map reads all data from the player id map
    - pass team abbreviation as argument
    - filter_clean() : 
        - filters for abbreviated team name and pulls all data for active hitters on that team
        - cleans missing values and converts rotowireid to int 
"""

class PlayerMap:

    # CSV with all id data
    read_player_map = pd.read_csv('SFBB Player ID Map - PLAYERIDMAP.csv')
    
    # Hitter vs Pitcher matchup url, must add player id as suffix
    vs_pitcher_url = "www.rotowire.com/baseball/tables/vs-pitcher.php?playerID="

    def __init__(self, abbrev):
        self.abbrev = abbrev 
    

    def filter_clean(self):

        j = 0   # incrementer
        
        roto_cols = ['FIRSTNAME','LASTNAME', 'ROTOWIREID', 'TEAM', 'ACTIVE', 'POS']
        
        rotto_hitter = PlayerMap.read_player_map

        rotto_hitter = rotto_hitter[roto_cols].loc[(rotto_hitter['TEAM'] == self.abbrev) & (rotto_hitter['ACTIVE'] == 'Y') & (rotto_hitter['POS'] != 'P')]
        rotto_hitter = rotto_hitter.dropna()
        rotto_hitter = rotto_hitter.astype({"ROTOWIREID": "int32"})

        rotto_hitter['TABLE_URL'] = rotto_hitter.apply(lambda _: '', axis = 1)
        

        for i in rotto_hitter['ROTOWIREID']:
            vs_pitcher_table = f"{PlayerMap.vs_pitcher_url}{i}"
            rotto_hitter.iloc[j, 6] = vs_pitcher_table

            j +=1
        
        return rotto_hitter


     
    

t1 = PlayerMap("LAA")

laa_df = t1.filter_clean() 