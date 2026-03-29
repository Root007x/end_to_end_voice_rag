import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format="[%(asctime)s:] %(message)s:")

project_name = "mysoft_rag"

list_of_files = [
    f"src/{project_name}/api/endpoints/__init__.py",
    f"src/{project_name}/schemas/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/services/__init__.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/config.py",
    f"src/{project_name}/main.py",
    "config/config.yaml",
    ".env",
    "app.py",
    "requirements.txt",
    "research/research_notebook.ipynb",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Created empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")
