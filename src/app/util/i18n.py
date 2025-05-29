import json

from pathlib import Path

PARENT_DIR = Path(__file__).parent
LANGS = PARENT_DIR / "langs.json"

def get_i18n_msg(msg: str, lang: str | None = 'uz') -> str:
    with open(LANGS, 'r', encoding='utf-8') as file:
        content = json.load(file)

    message_dict = content.get(msg, {})
    return message_dict.get(lang) or message_dict.get('uz')