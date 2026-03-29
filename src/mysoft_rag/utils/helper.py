import re
from typing import List, Dict
from pathlib import Path
import shutil


def clean_company_profile_markdown(text: str) -> Dict[str, List[str]]:

    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    text = re.sub(r"^\s*0\s*$", "", text, flags=re.MULTILINE)

    def fix_spaced_words(match):
        return match.group(0).replace(" ", "")

    text = re.sub(
        r"\b(?:[A-Za-z]\s){2,}[A-Za-z]\b", lambda m: m.group(0).replace(" ", ""), text
    )

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    raw_sections = re.split(r"\n## ", text)

    sections = []
    for sec in raw_sections:
        sec = sec.strip()
        if len(sec) > 50:  # Ignore tiny fragments
            sections.append(sec)

    return {"clean_text": text.strip(), "sections": sections}


def clean_web_text(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()


def delete_file_from_folder(folder_path):

    folder = Path(folder_path)

    try:
        for item in folder.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print("Folder Cleaned")
    except Exception as e:
        raise e


def check_data_exist(file_path):
    folder = Path(file_path)

    if any(f.is_file() for f in folder.iterdir()):
        return True
    return False
