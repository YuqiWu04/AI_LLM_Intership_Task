import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# 读取 api key
api_key = os.environ.get("DEEPSEEK_API_KEY")  # 请将个人的api key 可以加入到环境变量中
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY is not set. Please configure your API key first.")
# 创建模型
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
# 创建第一个 promptTemplate
title = PromptTemplate(
    input_variables=["topic"],
    template="请写一个关于{topic}的生成3个小红书笔记的标题。"
)
# 创建第二个promptTemplate
content= PromptTemplate(
    input_variables=["title"],
    template="从生成的3个标题中选择一个，为这个【标题】生成一篇包含emoji的正文草稿"
)
# 创建链
# title chain
title_chain = title | llm
# content chain
content_chain = content | llm

topic = input("请输入你想要的主题：")
title_response = title_chain.invoke({"topic": topic})
content_response = content_chain.invoke({"title": title})
print(f"标题：{title_response.text}\n正文：{content_response.text}")
