from langchain.tools import tool

from src.utils.micorsoft_office_reader import MicrosoftOfficeReader
from src.service.langchain.core.models import qwen_model

@tool
def read_richtext(file_path: str, read_method: str = "py") -> str:
    if read_method == "py":
        return MicrosoftOfficeReader.read_microsoft_word(file_path)
    elif read_method == "LLM":
        return qwen_model.read_richtext(file_path)
    else:
        raise ValueError(f"不支持的阅读方法: {read_method}")
    