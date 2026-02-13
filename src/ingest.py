#!/usr/bin/env python3
"""Simple repo ingestion:
- If `--repo` is a local path, copy source files to `out/raw/`
- If `--repo` is a git URL, `git clone` into a temp folder then copy

This is intentionally minimal — extend as needed.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import safe_mkdir, list_source_files, read_text_file


def clone_repo(url: str, target: str):
    safe_mkdir(target)
    subprocess.check_call(["git", "clone", url, target])


def copy_source(src_root: str, out_root: str):
    safe_mkdir(out_root)
    files = list_source_files(src_root)
    for p in files:
        rel = os.path.relpath(p, src_root)
        dest = os.path.join(out_root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(p, dest)


def ingest(repo: str, out: str):
    out_raw = os.path.join(out, "raw")
    safe_mkdir(out_raw)
    if repo.startswith("http://") or repo.startswith("https://") or repo.endswith(".git"):
        with tempfile.TemporaryDirectory() as td:
            print(f"cloning {repo} -> {td}")
            clone_repo(repo, td)
            copy_source(td, out_raw)
    else:
        print(f"copying local path {repo} -> {out_raw}")
        copy_source(repo, out_raw)
    print(f"done. raw files are at: {out_raw}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, help="Local path or git URL")
    p.add_argument("--out", required=True, help="Output folder (e.g. data/myrepo)")
    args = p.parse_args()
    ingest(args.repo, args.out)
