import os
from pathlib import Path
from typing import List


def safe_mkdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def list_source_files(root: str, exts: List[str] = None) -> List[str]:
    exts = exts or [".py", ".js", ".ts", ".java", ".go"]
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if any(fn.endswith(e) for e in exts):
                files.append(os.path.join(dirpath, fn))
    return files
