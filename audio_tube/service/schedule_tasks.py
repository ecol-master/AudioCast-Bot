from config import on_delete_filenames, OUTPUT_DIR
from pathlib import Path
import os
import logging


def del_downloaded_files():
    print("Тут")
    for fn in on_delete_filenames:
        _del_downloaded_files_by_fn(fn)
    on_delete_filenames.clear()


def _del_downloaded_files_by_fn(fn: str):
    content = os.listdir(Path(f"{OUTPUT_DIR}"))
    downloaded_files = filter(lambda f: f.startswith(fn), content)
    for file in downloaded_files:
        os.remove(Path(f"{OUTPUT_DIR}", file))
        logging.info(f"Delete file: {file}")
