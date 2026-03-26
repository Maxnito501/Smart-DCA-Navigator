import streamlit as st 
import pandas as pd 
import sys 
import os 
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from utils.config import get_watchlist 
 
st.set_page_config(layout="wide") 
 
st.title("📋 จัดการ Watchlist") 
st.markdown("รายชื่อหุ้น/กองทุนที่ติดตาม สำหรับการวิเคราะห์และแจ้งเตือน") 
 
@st.cache_data 
def load_core(): 
    return pd.read_csv("data/watchlist_core.csv") 
 
@st.cache_data 
def load_satellite(): 
    return pd.read_csv("data/watchlist_satellite.csv") 
 
@st.cache_data 
def load_funds(): 
    return pd.read_csv("data/funds_rmf.csv") 
 
core = load_core() 
satellite = load_satellite() 
funds = load_funds() 
watchlist = get_watchlist() 
 
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Core (ถือยาว)", "🚀 Satellite (เล่นรอบ)", "💰 กองทุน RMF", "🌍 กองทุนต่างประเทศ"]) 
 
with tab1: 
    st.subheader("หุ้นไทย Core (ถือยาว)") 
    st.dataframe(core, use_container_width=True, hide_index=True) 
 
with tab2: 
    st.subheader("หุ้นไทย Satellite (เล่นรอบ)") 
    st.dataframe(satellite, use_container_width=True, hide_index=True) 
 
with tab3: 
    st.subheader("กองทุน RMF") 
    st.dataframe(funds, use_container_width=True, hide_index=True) 
 
with tab4: 
    st.subheader("กองทุนต่างประเทศ (เบญจภาคี)") 
    us_etfs_df = pd.DataFrame({ 
        "กองทุน": watchlist["us_etfs"], 
        "ลักษณะ": ["High Yield", "Dividend Growth", "Core Growth", "High Yield", "Quality Growth"], 
        "กลยุทธ์": ["DCA", "DCA", "DCA", "DCA", "EDCA"] 
    }) 
    st.dataframe(us_etfs_df, use_container_width=True, hide_index=True) 
 
st.markdown("---") 
st.caption("พัฒนาโดย Suchat50 — สามารถเพิ่ม/ลด Watchlist ได้โดยแก้ไขไฟล์ CSV ใน data/") 
