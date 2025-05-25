import json

def get_i18n_msg(msg: str, lang: str) -> str:
    with open("app/util/langs.json", 'r', encoding='utf-8') as file:
        content = json.load(file)
    
    return content.get(msg).get(lang)