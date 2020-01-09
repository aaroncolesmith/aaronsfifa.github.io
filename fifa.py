import streamlit as st
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
import plotly_express as px
import os

#uploaded_file = st.file_uploader("Choose a HAR...", type="har")
#if uploaded_file is not None:
#    file = uploaded_file

def fifa_har(file, player_file):
    with open(file) as data_file:
        d = json.load(data_file)
    df=pd.DataFrame()
    x=0
    a=d['log']['entries']
    for i in a:
        s=a[x]
        try:
            t=s['response']['content']['text']
        except:
            print('Line ' + str(x) + ' failed')
            pass
        if t[:10] == '{"itemData':
            temp_df=pd.read_json(t)
            df=df.append(json_normalize(temp_df['itemData']),sort=False)
        x += 1

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace(')', '')

    with open(player_file) as data_file:
        data = json.load(data_file)
    df_p=pd.io.json.json_normalize(data['Players'])

    df_l=pd.io.json.json_normalize(data['LegendsPlayers'])

    df_player=df_p.append(df_l,sort=False)
    df_player.columns = df_player.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace(')', '')

    df=pd.merge(df,df_player,how='inner',left_on='assetid',right_on='id')
    df[['pace','sho','pass','dri','def','phy']] = pd.DataFrame(df.attributearray.values.tolist(), index=df.index)
    df[['games','goals','yellows','reds','tbd']] = pd.DataFrame(df.statsarray.values.tolist(), index= df.index)
    df['points'] = df['goals'] + df['assists']
    df['ppg'] = df['points'] / df['games']
    df['ppg']=df['ppg'].fillna(0)
    df['player_name'] = df['f'] + ' ' + df['l']
    df=df[['player_name','preferredposition','rating','pace','sho','pass','dri','def','phy','games','goals','assists','yellows','points','ppg','formation','untradeable','owners','cardsubtypeid','lastsaleprice','fitness','teamid','leagueid','nation','rareflag','playstyle','loyaltybonus','pile','skillmoves','weakfootabilitytypecode','attackingworkrate','defensiveworkrate','trait1','trait2','groups']]
    return df



player_file='fifa_players.json'
file = st.text_input('Enter a file path:')
try:
    with open(file) as input:
        st.text(input.read())
        df=fifa_har(file,player_file)
        st.write(df)
except FileNotFoundError:
    st.error('File not found.')


#file='www.easports.com_my_club_transfer_list.har'
#file = 'Desktop/01_08.har'



#clubs = st.multiselect('Show Player for clubs?', df['Tm'].unique())

#years = st.multiselect('Show Player for years?', df['YEAR'].unique())

# Filter dataframe
#new_df = df[(df['Tm'].isin(clubs)) & (df['YEAR'].isin(years))]

# write dataframe to screen
