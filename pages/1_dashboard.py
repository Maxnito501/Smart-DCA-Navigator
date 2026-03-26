import streamlit as st 
import pandas as pd 
import sys 
import os 
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from utils.config import get_watchlist 
 
st.set_page_config(layout="wide") 
 
st.title("📊 แดชบอร์ดรวม") 
st.markdown("ภาพรวมพอร์ต Core + Satellite + กองทุน RMF + กองทุนต่างประเทศ") 
 
@st.cache_data 
def load_data(): 
    core = pd.read_csv("data/watchlist_core.csv") 
    satellite = pd.read_csv("data/watchlist_satellite.csv") 
    funds = pd.read_csv("data/funds_rmf.csv") 
    return core, satellite, funds 
 
core, satellite, funds = load_data() 
watchlist = get_watchlist() 
 
col1, col2, col3, col4 = st.columns(4) 
 
with col1: 
    st.metric("หุ้น Core (ถือยาว)", f"{len(core)} ตัว", "ปันผล 5-8%%") 
 
with col2: 
    st.metric("หุ้น Satellite (เล่นรอบ)", f"{len(satellite)} ตัว", "EDCA + ขายทำกำไร") 
 
with col3: 
    st.metric("กองทุน RMF", f"{len(funds)} กอง", "DCA + EDCA") 
 
with col4: 
    st.metric("กองทุนต่างประเทศ", f"{len(watchlist['us_etfs'])} ตัว", "เบญจภาคี") 
 
st.markdown("---") 
st.caption("พัฒนาโดย Suchat50") 
