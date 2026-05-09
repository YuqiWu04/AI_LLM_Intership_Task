# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

def read_text_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()

def process_text(text):
    api_key = os.environ.get("DEEPSEEK_API_KEY") #请将个人的api key 可以加入到环境变量中
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is not set. Please configure your API key first.")
    # 创建客户端
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")  # 导航到deepseek 否则 默认为open ai
    prompt = f"""
    请处理以下文本。
    请在回复之前尊敬的称呼我Sir
    任务：
    1. 写一段简洁摘要。
    2. 提取准确的5个关键词。
    文本：
    {text}

    输出格式如下：
    总结：
    关键词：
    
    
    
    
    
    """
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant"
             },

            {"role": "user",
             "content": prompt
             },
        ],
        stream=False,
        # reasoning_effort="high",
        # extra_body={"thinking": {"type": "enabled"}}
    )

    return (response.choices[0].message.content)

def main():
    file_name = "sample.txt"
    text = read_text_file(file_name)
    result = process_text(text)
    print(result)

if __name__ == "__main__":
    main()