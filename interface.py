"""
    streamlit frontend interface for JLPT questions.
"""

import streamlit as st
from plugins import (
    general_summary,
    KanjiMondai
)

# load_files()

# mondais = csv_to_kanji_mondais("data/mock/mock.csv")
# mondai_id, instruction = mondais[0].MONDAI_ID, mondais[0].INSTRUCTION

m1 = KanjiMondai(
    id=1,
    description="これから<u><b>概略</b></u>をご説明します。",
    choices=["がいかく", "きかく", "がいりゃく", "きりゃく"],
    answer_idx=0
)

question_id, question_text, options  = m1.id, m1.description, m1.choices

mondai_description = f'<h5 style="font-weight: bold;">{m1.INSTRUCTION}</h5>'
question      = f"{question_id}. {question_text}"

st.caption('<div style="text-align: center; margin-bottom: 1rem;">2010.9 N1 / 文字</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])

if "question_begin" not in st.session_state:
    st.session_state.question_begin = False
col1.button("上一题", disabled=not st.session_state.question_begin)

col2.selectbox("选择题目", [1, 2, 3, 4, 5], index=0, label_visibility="collapsed", help="选择题目编号")
    
if "question_end" not in st.session_state:
    st.session_state.question_end = False
col3.button("下一题", disabled=not st.session_state.question_end)

st.html(mondai_description) 

with st.form("question_form"):
    st.html(question)
    selected_option = st.radio("choose-answers", options, index=None, label_visibility="collapsed")
    submit = st.form_submit_button(label="提交", help="提交答案之后可以看 AI 解析哦！")

if submit:
    st.write("##### AI 解析")
    if selected_option == "がいかく":
        st.success("回答正确")
    else:
        st.error("回答错误")
    general_summary(question_text)