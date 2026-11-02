from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import BaseModel
from .query import ask_question, stream_answer
import os

app = FastAPI(title="AI 知识库问答 API")

# 允许跨域（方便以后把前端分开部署）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体格式
class QueryRequest(BaseModel):
    question: str

# 1. 根路由：返回前端 HTML 页面
@app.get("/")
def read_root():
    # 注意：这里使用绝对路径，确保能找到 frontend 文件夹
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "frontend", "index.html")
    return FileResponse(html_path)

@app.post("/chat")
def chat(request: QueryRequest):
    return StreamingResponse(
        stream_answer(request.question),
        media_type="text/plain; charset=utf-8",
    )

@app.post("chat/ask")
def chat(question:str):
    answer  = ask_question(question)
    print("答案是",answer)


'''
from fastapi import FastAPI
from pydantic import BaseModel
from .query import ask_question

app = FastAPI(title="AI 知识库问答 API")

# 定义请求体格式
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "AI 知识库 API 已启动！"}

@app.post("/chat")
def chat(request: QueryRequest):
    answer = ask_question(request.question)
    return {"question": request.question, "answer": answer}
'''