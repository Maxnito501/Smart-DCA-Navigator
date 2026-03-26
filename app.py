import streamlit as st

st.set_page_config(
    page_title="Smart DCA Navigator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart DCA Navigator")
st.markdown("""
แอปช่วยบริหารการลงทุนแบบ DCA/EDCA
- หุ้นไทย Core / Satellite
- กองทุน RMF
- กองทุนต่างประเทศ (เบญจภาคี)
- หุ้นนอก US (Magnificent 5)
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📈 หุ้นไทย Core", "10 ตัว", "PTT, SCB, TISCO, AP, CPALL, ADVANC, GULF, BDMS, WHA, GPSC")

with col2:
    st.metric("🚀 หุ้นไทย Satellite", "10 ตัว", "TRUE, BH, AOT, SIRI, HMPRO, CPAXT, LH, KTC, DELTA, SCBSEMI")

with col3:
    st.metric("💰 กองทุน RMF", "7 ตัว", "SCBRMS&P500, SCBRMNDQ, KKPGQUAL, SCBRMWORLD, SCBRMS50, SCBRMLEQ, SCBGOLD")

with col4:
    st.metric("🌍 กองทุนต่างประเทศ", "5 ตัว", "SCHD, VIG, DGRO, VYM, DGRW")

st.markdown("---")
st.info("💡 ระบบแจ้งเตือนจะทำงานทุกวัน เช้า-เย็น (เมื่อ Deploy แล้ว)")
st.caption("พัฒนาโดย Suchat50")