import httpx
import os
import sys
from dotenv import load_dotenv
from mcp.server import FastMCP
from openai import OpenAI
from pathlib import Path

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.micorsoft_office_reader import MicrosoftOfficeReader

app = FastMCP("richtext-read")

def read_richtext_with_LLM(file_path: str) -> str:
    system_prompt = """你是一个文档阅读助手, 负责将文档内容转化为markdown格式, 只返回markdown源码"""
    try:
        load_dotenv()
        base_url = os.getenv("QWEN_BASE_URL")
        api_key = os.getenv("DASHSCOPE_API_KEY")
        model_name = os.getenv("QWEN_MODEL_NAME")
        if not api_key:
            raise RuntimeError("未检测到 API Key，请设置 QWEN_API_KEY 或 OPENAI_API_KEY")
        qwen_client = OpenAI(base_url=base_url, api_key=api_key)

        with open(file_path, "rb") as f:
            file_object = qwen_client.files.create(
                file=f,
                purpose="file-extract",
            )

        file_id = file_object.id
        file_object = qwen_client.files.retrieve(file_id)
        if not file_object or file_object.purpose != "file-extract":
            raise RuntimeError("未获取到文件对象")

        if not file_id or file_id == "":
            raise RuntimeError("未获取到文件ID")

        print(f"尝试使用文档{file_id}进行阅读")
        # 初始化messages列表
        completion = qwen_client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'system', 'content': f'fileid://{file_id}'},
                {'role': 'user', 'content': '给我这篇文档的markdown格式内容'}
            ],
            stream=True,
            stream_options={"include_usage": True}
        )

        full_content = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                # 拼接输出内容
                full_content += chunk.choices[0].delta.content
        return full_content

    except Exception as e:
        print(f"读取文档失败: {e}")
        return f"读取文档失败: {e}"

@app.tool()
def read_richtext(file_path: str, read_method: str = "py") -> str:
    if read_method == "py":
        file_type = file_path.split(".")[-1]
        if file_type == "docx":
            return MicrosoftOfficeReader.read_microsoft_word(file_path)
        elif file_type == "pdf":
            return MicrosoftOfficeReader.read_microsoft_pdf(file_path)
        elif file_type == "pptx":
            return MicrosoftOfficeReader.read_microsoft_ppt(file_path)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")
        
    elif read_method == "LLM":
        return read_richtext_with_LLM(file_path)
    else:
        raise ValueError(f"不支持的阅读方法: {read_method}")

if __name__ == "__main__":
    app.run(transport="stdio")

