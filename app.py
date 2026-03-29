import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- הגדרות בסיסיות ---
st.set_page_config(page_title="Momentum Mentor", layout="centered")
st.title("📈 The Momentum Mentor")
st.subheader("Performance Coach for VCP Traders")

# הכנס כאן את ה-API Key שלך מ-Google AI Studio
API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(AIzaSyBn6AFP1EhKNY0MFViOft5F3MQq-8je4hA)

# --- הגדרת ה"מוח" של הבוט (System Instruction) ---
SYSTEM_PROMPT = """
You are a Trading Performance Coach specializing in Mark Minervini's VCP methodology.
Tone: Professional, stoic, supportive, and objective. Never aggressive.
Core Rules to Enforce:
1. Every trade must be in a Stage 2 uptrend.
2. Entry must be at a VCP Pivot Point (Tightness).
3. THE 10% RULE: If a trade is up 10%, the stop MUST be at Break-even. No exceptions.
4. Capital preservation is #1.
5. If the user has 3 losses in a row, suggest a 48-hour trading break.

Interaction Flow:
- Validate the user's feelings briefly.
- Ask about the 4 points: Stage 2, VCP Setup, Stop Loss, Position Size.
- If they show a chart, analyze the price action and volume.
- End with a mindset reset.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # מודל מהיר וחכם שקורא תמונות
    system_instruction=SYSTEM_PROMPT
)

# --- ממשק המשתמש ---

# ניהול היסטוריית הצ'אט
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת הצ'אט
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# העלאת תמונה (גרף)
uploaded_file = st.sidebar.file_uploader("העלה צילום מסך של גרף (TradingView)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.sidebar.image(uploaded_file, caption="הגרף לניתוח", use_column_width=True)

# תיבת הקלט של המשתמש
if prompt := st.chat_input("מה קרה היום במסחר?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # יצירת תגובה מה-AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # הכנת הקלט (טקסט + תמונה אם קיימת)
        content_to_send = [prompt]
        if uploaded_file:
            img = Image.open(uploaded_file)
            content_to_send.append(img)
        
        # שליחה ל-Gemini
        response = model.generate_content(content_to_send)
        full_response = response.text
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# כפתור איפוס (Circuit Breaker)
if st.sidebar.button("הפעל Circuit Breaker (48 שעות מנוחה)"):
    st.sidebar.warning("המסך ננעל למנוחה. צא לטייל, השוק יחכה לך.")
