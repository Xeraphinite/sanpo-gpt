"""
    Streamlit interface. The main entry point for the application.
    You can run this script by executing `streamlit run interface.py` in the terminal. Make sure you have proper environment setup.
"""

import streamlit as st
from plugins import (
    mondai1_analyse,
    csv_to_kanji_mondais,
)

mondais = csv_to_kanji_mondais("data/mock/mock.csv")

st.caption('<div style="text-align: center; margin-bottom: 1rem;">N1 / 文字</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 6, 1])

st.session_state.setdefault("current_id", 0)

current_id = st.session_state.get("current_id", 0)

if col1.button("上一题", disabled=current_id == 0):
    st.session_state.current_id -= 1

if col3.button("下一题", disabled=current_id == len(mondais) - 1):
    st.session_state.current_id += 1

current_id = col2.selectbox(
    "选择题目", 
    [i + 1 for i in range(len(mondais))], 
    index=current_id, 
    label_visibility="collapsed", 
    help="选择题目编号",
)

# st.session_state.update(current_id=current_id)

current_mondai = mondais[current_id - 1] # type: ignore

question_id, question_text, options = current_mondai.id, current_mondai.description, current_mondai.choices
mondai_description = f'<h5 style="font-weight: bold;">{current_mondai.INSTRUCTION}</h5>'
question      = f"{question_id}. {question_text}"

st.html(mondai_description) 

with st.form("question_form"):
    st.html(question)
    selected_option = st.radio("choose-answers", options, index=None, label_visibility="collapsed")
    submit = st.form_submit_button(label="提交", help="提交答案之后可以看 AI 解析哦！")

if submit:
    st.write("##### AI 解析")
    if current_mondai.check_answer(selected_option):
        st.success("回答正确")
    else:
        st.error("回答错误")
    
    stream = mondai1_analyse(current_mondai)
    
    st.write_stream(stream=stream)