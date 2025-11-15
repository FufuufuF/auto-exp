from src.config import ModelConfig
from openai import OpenAI

class QwenModel:

    system_prompt = """你是一个文档阅读助手, 负责将文档内容转化为markdown格式, 只返回markdown源码"""

    def __init__(self):
        self.client = OpenAI(
            base_url=ModelConfig.QWEN["base_url"],
            api_key=ModelConfig.QWEN["api_key"],
        )

    def read_richtext(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            file_object = self.client.files.create(
                file=f,
                purpose="file-extract",
            )

        file_id = file_object.id
        if not file_id or file_id == "":
            raise ValueError("未获取到文件ID")

        completion = self.client.chat.completions.create(
            model=ModelConfig.QWEN["model_name"],
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'system', 'content': f'fileid://{file_id}'},
                {'role': 'user', 'content': '给我这篇文档的markdown格式内容'}
            ],
            stream=True,
            stream_options={"include_usage": True}
        )

        full_content = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        return full_content

qwen_model = QwenModel()