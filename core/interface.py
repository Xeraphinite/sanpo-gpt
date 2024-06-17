from dotenv import load_dotenv
import streamlit as st
from litellm import completion
import os

load_dotenv()

question_id = 1
question_text = "これから<u><b>概略</b></u>をご説明します。"
options = ["がいかく", "きかく", "がいりゃく", "きりゃく"]

question_description = '<h5 style="text-algn: center; font-weight: bold;">問題 1 &nbsp&nbsp  <u>_____</u>の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。</h5>'

question = f"{question_id}. {question_text}"

st.write(question_description, unsafe_allow_html=True)

st.write(question, unsafe_allow_html=True)

selected_option = st.radio('choose-answers', options, index=None, label_visibility='collapsed')

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    navigation = st.columns(2)
    navigation[0].button("上一题")
    navigation[1].button("下一题")

with col3:
    result = st.columns(2)

if "submit" not in st.session_state:
    st.session_state.submit = True

if selected_option:
    st.session_state.submit = False

submit = result[1].button("提交", type="primary", disabled=st.session_state.submit)

if submit:
    st.write("##### AI 解析")

    if selected_option == "がいりゃく":
        st.success("回答正确")
    else:
        st.error("回答错误")

    def stream():
        response = completion(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
            model=os.getenv("MODEL_NAME"),
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": "请给出详细的中文答案解析，题目如下" + question_description,
                },
                {"role": "user", "content": "问题如下：\n" + question},
                {"role": "user", "content": "问题选项如下：\n" + "\n".join(options)},
                {"role": "user", "content": "用户选择的选项是：" + selected_option},
            ],
        )

        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            yield content

    st.write_stream(stream=stream())
