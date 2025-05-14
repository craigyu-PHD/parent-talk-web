import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

st.title("遊戲化親子語言轉換器（網頁版）")

# 對話紀錄存在 session_state
if 'history' not in st.session_state:
    st.session_state['history'] = []

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("請輸入你想和孩子說的話", height=100)
    if st.button("轉換"):
        with st.spinner("轉換中..."):
            prompt = f"""
請將下列語句隨機選擇一種「遊戲化親子語言」風格（包含但不限於：擬人化／角色扮演、遊戲化、正向鼓勵、畫面感、溫柔幽默），並直接轉換成有創意且符合該風格的語句，不要加任何說明或客套話：
{user_input}
"""
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-DmKceRwr6AUlf04z0a58BaE4B5Bf46Ad806aC898D1Be0915"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "你是專業的親子語言轉換助手。"},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post("https://free.v36.cm/v1/chat/completions", headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"].strip()
                st.session_state['history'].append({
                    'user': user_input,
                    'ai': result
                })
                st.success(result)
            else:
                st.error("API 請求失敗，請稍後再試。")

with col2:
    st.markdown("### 對話紀錄")
    for item in reversed(st.session_state['history']):
        st.markdown(f"**你：** {item['user']}")
        st.markdown(f"**AI：** {item['ai']}")
        st.markdown("---")