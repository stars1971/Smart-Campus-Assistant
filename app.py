from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_ai(q: Question):
    # 配置请求的 API 和 API 密钥
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 65bc2e9e-80d5-4969-9338-0e480f37dcf1"  # API 密钥
    }

    # 请求体数据
    data = {
        "model": "doubao-1-5-thinking-pro-250415",  # 使用的模型
        "messages": [
            {"role": "system", "content": "你是人工智能助手."},
            {"role": "user", "content": q.query}  # 用户输入的查询
        ]
    }

    # 发送 POST 请求
    res = requests.post(url, json=data, headers=headers)

    # 输出调试信息
    print("状态码:", res.status_code)
    print("返回内容:", res.text)

    # 处理响应
    if res.status_code == 200:
        try:
            # 获取并返回模型的回答
            answer = res.json().get("choices", [{}])[0].get("message", {}).get("content", "没有回答")
            return {"answer": answer}
        except Exception as e:
            return {"error": "解析响应失败", "detail": str(e)}
    else:
        return {"error": f"API 请求失败，状态码 {res.status_code}", "detail": res.text}

