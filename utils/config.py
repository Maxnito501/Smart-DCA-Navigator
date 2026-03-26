import os 
from dotenv import load_dotenv 
import streamlit as st 
 
load_dotenv() 
 
def get_line_config(): 
    try: 
        if "line" in st.secrets: 
            return { 
                "access_token": st.secrets["line"]["channel_access_token"], 
                "channel_secret": st.secrets["line"]["channel_secret"], 
                "user_id": st.secrets["line"].get("user_id") 
            } 
    except: 
        pass 
 
    return { 
        "access_token": os.getenv("LINE_CHANNEL_ACCESS_TOKEN"), 
        "channel_secret": os.getenv("LINE_CHANNEL_SECRET"), 
        "user_id": os.getenv("LINE_USER_ID") 
    } 
 
def get_watchlist(): 
    core_stocks = [ 
        "PTT", "SCB", "TISCO", "AP", "CPALL", 
        "ADVANC", "GULF", "BDMS", "WHA", "GPSC" 
    ] 
    satellite_stocks = [ 
        "TRUE", "BH", "AOT", "SIRI", "HMPRO", 
        "CPAXT", "LH", "KTC", "DELTA", "SCBSEMI" 
    ] 
    us_etfs = ["SCHD", "VIG", "DGRO", "VYM", "DGRW"] 
    return { 
        "core": core_stocks, 
        "satellite": satellite_stocks, 
        "us_etfs": us_etfs 
    } 
