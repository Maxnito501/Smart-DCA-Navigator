# Smart DCA Navigator 
 
แอปช่วยบริหารการลงทุนแบบ DCA/EDCA สำหรับหุ้นไทย กองทุน RMF กองทุนต่างประเทศ และหุ้นนอก 
 
## ฟีเจอร์ 
- **Watchlist Manager** - จัดการหุ้น/กองทุนที่สนใจ 
- **Ranking Engine** - จัดลำดับความน่าเข้าซื้อ (Core / Satellite) 
- **DCA Date Optimizer** - หาวันที่เหมาะสมที่สุดสำหรับ DCA (อิง EMA200) 
- **LINE Alert** - แจ้งเตือนวันละ 2 ครั้ง (เช้า-เย็น) 
- **Portfolio Tracker** - บันทึกหุ้นที่ซื้อแล้ว คำนวณต้นทุนเฉลี่ย 
 
## การติดตั้ง 
```bash 
pip install -r requirements.txt 
``` 
 
## การใช้งาน 
```bash 
streamlit run app.py 
``` 
 
## การตั้งค่า LINE Messaging API 
1. สร้างไฟล์ .env 
2. ใส่ LINE_CHANNEL_ACCESS_TOKEN และ LINE_CHANNEL_SECRET 
 
## Deploy บน Streamlit Cloud 
1. Push โค้ดขึ้น GitHub 
2. เชื่อมต่อกับ Streamlit Cloud 
3. ตั้งค่า Secrets (LINE Token) 
 
พัฒนาโดย Suchat50 
