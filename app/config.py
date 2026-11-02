import os
from dotenv import load_dotenv
# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")


from openai import OpenAI

# 问答与入库代码使用的名称
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = "https://api.deepseek.com"
LLM_MODEL_NAME = "deepseek-flash"
# 向量库是用这个中文嵌入模型建的，查询时必须用同一个模型
EMBED_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_BASE,
    timeout=60,
)




'''
import base64
import os
from io import BytesIO
from openai import OpenAI
from PIL import Image

# ==================== 配置区【TODO 手写】 ====================
# TODO：在这里手写API配置 + 客户端初始化
# 1. 定义API_KEY、BASE_URL、MODEL_ENDPOINT
# 2. 初始化 client = OpenAI(...)



# 图片预处理工具函数（直接复制，不用手写）
def prepare_image_base64(image_path: str, max_size: int = 1024) -> str:
    """
    读取本地图片，处理透明通道，缩放并转换为 base64 字符串
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"找不到测试图片: {image_path}")
        
    with Image.open(image_path) as img:
        # 1. 处理 RGBA 透明背景
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
            
        # 2. 等比例缩放（防大图撑爆 Payload/Token）
        img.thumbnail((max_size, max_size))
        
        # 3. 转 Base64
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        
    return f"data:image/jpeg;base64,{b64}"

# ==================== multimodal_chat【TODO 手写核心逻辑】 ====================
def multimodal_chat(img_path: str, prompt: str):
    """多模态对话测试"""
    try:
        print(f"正在处理图片: {img_path} ...")
        img_b64 = prepare_image_base64(img_path)
        
        print("正在发送请求至大模型平台...")
        # TODO 手写：client.chat.completions.create()
        # 构造 messages 多模态消息体，调用接口
        # 设置 model、messages、temperature、max_tokens
        
        
        
        # TODO 手写：读取模型返回结果，打印输出
        
        
        
    except FileNotFoundError as e:
        print(f"【错误】{e}")
    except Exception as e:
        print(f"【API 请求失败】请检查网络或 Endpoint/Key 是否正确。错误信息:\n{e}")
        return None

# ==================== 程序入口【TODO 手写基础调用】 ====================
if __name__ == "__main__":
    # TODO：手写图片路径、提问内容，调用 multimodal_chat
    
    
    
    # 下面自动生成测试图片的代码，保留不用写
    image_file = "./cat-cartoon.webp"
    if not os.path.exists(image_file):
        print(f"未检测到 {image_file}，正在生成一张临时测试图...")
        Image.new('RGB', (200, 200), color = (73, 109, 137)).save(image_file)

'''