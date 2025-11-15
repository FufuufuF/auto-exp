import dotenv
import os

dotenv.load_dotenv()

class ModelConfig:
    QWEN = {
        "base_url": os.getenv("QWEN_BASE_URL"),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "model_name": os.getenv("QWEN_MODEL_NAME"),
    }
    DEEPSEEK = {
        "base_url": os.getenv("DEEPSEEK_BASE_URL"),
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "model_name": os.getenv("DEEPSEEK_MODEL_NAME"),
    }