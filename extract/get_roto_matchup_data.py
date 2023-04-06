import get_roto_player_id
import http.client
import os 
import time
import json
import pandas as pd
import csv

"""
This class scrapes website. Returns data for each hitter on the specified team from 'get_roto_player_id.py'. 
Data includes career statistics vs all pitchers faced with more than 7 AB's.
Data is written to a json file named "Firstname_Lastname.json" for each hitter on specified team
"""

class fetch_data():
    
    ########## ------------ Class Dataframe  -------------------######### 
    team_df = get_roto_player_id.laa_df  

    ########## ------------ Path Variables  -------------------######### 
    base_path = os.path.abspath(__file__ + "/../../")
    team_path = f"{base_path}/teams/"
    player_stat_path = ""

    ########## ------------ Conn Variables  -------------------######### 
    conn = http.client.HTTPSConnection("www.rotowire.com")

    base_url = '/baseball/tables/vs-pitcher.php?playerID='
    suffix_url = '&minatbats=7'

    payload = ""
    headers = {
        'authority': "www.rotowire.com",
        'accept': "*/*",
        'accept-language': "en-US,en;q=0.9",
        'cookie': "PHPSESSID=e7f6bc63743006a6f9dd8d659b9be2d4; continent_code_found=unknown; g_uuid=43a0a5f0-718c-49db-8de5-8eb710de0787; cohort_id=3; g_sid=1679723310918.ehii24ni",
        'referer': "https://www.rotowire.com/baseball/stats-bvp.php",
        # 'referer': "https://www.rotowire.com/baseball/player-vs-pitcher.php?id=10956",
        'sec-ch-ua': "^\^Google",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "^\^Windows^^",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
    

    # /------------- Create folders with path argument -----------------
    # def create_folder_if_not_exists(path):
    #     """
    #     Create a new folder if it doesn't exist
    #     """
    #     os.makedirs(os.path.dirname(path), exist_ok=True)
    # ------------------------------------------------------------------/


    

    # 25 hitters 
    j = 0
    team_df['table_link'] = team_df.apply(lambda _: '', axis = 1)
    
    for id in team_df['ROTOWIREID']:
        matchups_link = f"{base_url}{id}{suffix_url}"
        team_df[j,7] = matchups_link
        conn.request("GET", matchups_link, payload, headers)
        res = conn.getresponse()
        data = res.read()
        dec = data.decode("utf-8")
        # data = res.read()
        # dec = data.decode("utf-8")

        # pretty_data = json.loads(data)
        # dec = data.decode("utf-8")
        # change this to write to desired directory / folder
        with open(f"{team_df.iloc[j,0]}_{team_df.iloc[j,1]}.json", "w") as outfile:
            json.dump(dec, outfile)
            # df = pd.DataFrame.from_records(dec)
            print(f"{team_df.iloc[j,0]}_{team_df.iloc[j,1]}'s json file was dumped")

        time.sleep(30)

        j +=1
    # -------------------------------------------------------------------/