import os

PROMPT = {}
PROMPT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

doct_prompt_path = os.path.join(PROMPT_ROOT_PATH, "doct")

def load_prompt(doct_name: str):
    prompt_path = os.path.join(doct_prompt_path, f"{doct_name}.mdc")
    prompt = ""
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    
    PROMPT[doct_name] = prompt

doct_list = os.listdir(doct_prompt_path)
for doct_name in doct_list:
    load_prompt(doct_name)