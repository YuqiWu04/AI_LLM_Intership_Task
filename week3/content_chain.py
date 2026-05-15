import os

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import re
# # 读取 api key
def get_api_key():
    api_key = os.environ.get("DEEPSEEK_API_KEY")  # 请将个人的api key 可以加入到环境变量中
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is not set. Please configure your API key first.")
    return api_key
# # 创建模型
def get_model():
    api_key = get_api_key()
    llm = ChatOpenAI(
        model="deepseek-v4-flash",
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    return llm
# # 创建第一个 promptTemplate
def get_title_chain(llm):
    title = PromptTemplate(
        input_variables=["topic"],
        template="写一个关于{topic}的生成3个小红书笔记的标题。"


    )
    title_chain = title | llm
    return title_chain
# # 创建第二个 promptTemplate
def get_content_chain(llm):
    content= PromptTemplate(
        input_variables=["title"],
        template="现在你作为小红书知名网红博主，从生成的3个标题中选择一个{title}，并向这个标题生成一篇包含emoji的正文草稿"
    )
    content_chain = content | llm
    return content_chain


def extract_first_title(output):
    lines = output.content.splitlines()
    first_line = next((line for line in lines if line.strip()), "")
    first_title = first_line.strip()
    return {"title": first_title}

def main():
    topic = input("请输入你想要的主题：")
    llm_model = get_model()
    # title_response = get_title_chain(llm_model).invoke({"topic": topic})
    # titles_text = title_response.content
    # first_title = titles_text.splitlines()[0]
    # content_response = get_content_chain(llm_model).invoke({"title": first_title})
    full_chain = (
            {"topic": RunnablePassthrough()}  # 输入原始 topic
            | get_title_chain(llm_model)  # 生成3个标题
            | RunnableLambda(extract_first_title)  # 提取第一个标题
            | get_content_chain(llm_model)  # 生成正文
    )

    result = full_chain.invoke(topic)


    print(result.content)

if __name__ == "__main__":
        main()

