# Load libraries
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests


BASE_URL = "https://understat.com"
# Get matches' data
def get_data(path, id, base_url=BASE_URL):
    
    res = requests.get(f"{base_url}/{path}/{id}")
    soup = BeautifulSoup(res.content, 'html.parser')
    string = soup.find_all('script')[4].string
    start_idx = string.index("('")
    stop_idx = string.index("')")
    string = string[start_idx+2:stop_idx]
    data = string.encode('utf8').decode('unicode_escape')
    json_data = json.loads(data)
    
    return pd.DataFrame(json_data)

# Transform data
def transform_data(df):
    new_df = df.copy()
    for col in new_df.columns:
        if col in ['position', 'h_team', 'a_team']:
            new_df[col] = new_df[col].astype(str)
        elif col in ['goals', 'shots', 'time', 'h_goals', 'a_goals', 'assists', 'key_passes', 'npg', 'season']:
            new_df[col] = new_df[col].astype(int)
        elif col in ['xG', 'xA', 'npxG', 'xGChain', 'xGBuildup']:
            new_df[col] = new_df[col].astype(float).round(2)
        elif col in 'date':
            new_df[col] = pd.to_datetime(new_df[col])
    
    new_df.drop(['id', 'roster_id', 'position'], axis=1, inplace=True)
    new_df.columns = ['Goals', 'Shots', 'XG', 'Minutes Played', 'Home Team', 'Away Team', 'Home Goals','Away Goals', 'Date', 'Season', 'XA','Assists', 'Key Passes', 'NPG', 'NPXG', 'XGChain', 'XGBuildup']
    
    return new_df

data = get_data("player", 2370)

data = transform_data(data)

data.to_csv("kb9_match_stats_2014_2021.csv", index=False)