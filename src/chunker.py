#!/usr/bin/env python3
"""Chunker with a tree-sitter fallback.
Outputs newline-delimited JSON objects with keys: id, file_path, start_line, end_line, text
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import read_text_file, list_source_files, safe_mkdir

try:
    from tree_sitter import Language, Parser
    TREE_SITTER_AVAILABLE = True
except Exception:
    TREE_SITTER_AVAILABLE = False


def naive_chunk(text: str, max_lines: int = 200) -> List[tuple]:
    """Fallback chunker: split by blank lines and by max_lines."""
    lines = text.splitlines()
    chunks = []
    start = 0
    for i in range(0, len(lines), max_lines):
        end = min(i + max_lines, len(lines))
        chunk_text = "\n".join(lines[i:end]).strip()
        if chunk_text:
            chunks.append((i + 1, end, chunk_text))
    return chunks


def python_function_chunks(text: str) -> List[tuple]:
    # crude regex to find def/class boundaries
    pattern = re.compile(r"^(def |class )", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return naive_chunk(text)
    chunks = []
    starts = [m.start() for m in matches]
    starts.append(len(text))
    for i in range(len(starts) - 1):
        s = starts[i]
        e = starts[i + 1]
        chunk = text[s:e].strip()
        if chunk:
            # compute line numbers
            start_line = text[:s].count("\n") + 1
            end_line = text[:e].count("\n") + 1
            chunks.append((start_line, end_line, chunk))
    return chunks


def chunk_file(path: str) -> List[dict]:
    text = read_text_file(path)
    if path.endswith('.py'):
        chunks = python_function_chunks(text)
    else:
        chunks = naive_chunk(text)
    out = []
    for idx, (start, end, chunk_text) in enumerate(chunks):
        out.append({
            "id": f"{os.path.basename(path)}:{idx}",
            "file_path": path,
            "start_line": start,
            "end_line": end,
            "text": chunk_text,
        })
    return out


def chunk_folder(input_root: str, out_file: str):
    safe_mkdir(os.path.dirname(out_file) or ".")
    files = list_source_files(input_root)
    with open(out_file, "w", encoding="utf-8") as fw:
        for f in files:
            for c in chunk_file(f):
                fw.write(json.dumps(c) + "\n")
    print(f"wrote chunks -> {out_file}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_dir", required=True, help="Input raw folder")
    p.add_argument("--out", dest="out_file", required=True, help="Output JSONL file for chunks")
    args = p.parse_args()
    chunk_folder(args.in_dir, args.out_file)
