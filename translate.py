from langchain_openai import ChatOpenAI 
#from langchain_core.cache import InMemoryCache  
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

with st.sidebar:
    api_vendor = st.radio(label='请选择服务提供商：', options=['OpenAI', 'DeepSeek'])
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_options = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1', 'gpt-4.1-nano', 'gpt-5.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_options = ['deepseek-chat', 'deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：', options=model_options)
    api_key = st.text_input(label='请输入你的Key：', type='password')


def translate(text):
    set_llm_cache(SQLiteCache(database_path=".langchain.db"))

    llm = ChatOpenAI(
        base_url=base_url,
        model_name=model_name,
        api_key=api_key,
        temperature=0.2,
        max_tokens=4096,
        streaming=True,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的翻译助手，擅长给出信达雅的翻译"),
        ("user",'请将下面的内容翻译成{language}:\n{text}')
        ])
    chain = prompt | llm
    for language in languages:
        msg = chain.invoke({'language':language,'text':text})
        st.write(f"{language}翻译：{msg.content}")

st.title('文本翻译助手')
user_prompt = st.text_input(label='',placeholder='请输入要翻译的文本：',width = 640)
languages =st.multiselect(label='请选择要翻译的语言：', options=['英文','中文','日文','韩文','法文','德文'],placeholder='点击选择要翻译的语言')
ok_button = st.button("点击翻译",type="primary")

if ok_button and user_prompt.strip():
    if languages:
        try:
            with st.spinner("翻译中..."):
                translate(user_prompt)
                st.success("翻译完成！")
        except Exception as e:
            st.error("请检查你的Key是否正确配置")
    else:
        st.error("请选择翻译的语言")

