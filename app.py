import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("香港賽馬 單場測試版")

# 用戶輸入
race_date = st.text_input("輸入賽事日期 (例如: 2025-09-01)")
race_no = st.number_input("輸入場次 (例如: 1)", min_value=1, max_value=12, step=1)

if st.button("獲取賽果"):
    if race_date and race_no:
        # HJC Racecard URL 格式
        url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?RaceDate={race_date}&Racecourse=ST&RaceNo={race_no}"
        
        st.write(f"📡 正在爬取: {url}")
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            tables = soup.find_all("table")
            if tables:
                df = pd.read_html(str(tables[0]))[0]
                st.dataframe(df)
            else:
                st.error("未搵到比賽數據，可能網址格式唔啱 / HKJC 攔截")
        else:
            st.error("爬取失敗 ❌")
    else:
        st.warning("請先輸入日期同場次")
