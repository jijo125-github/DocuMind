DocuMind — Starter repo

This starter includes basic scripts to ingest a repository, chunk files, and run a simple query demo.

Files added:
- `src/ingest.py` — clone or read a repo and copy source files to a data folder
- `src/chunker.py` — semantic chunker with a fallback parser
- `src/utils.py` — small helpers (file reading, safe write)
- `scripts/query_repo.py` — simple query CLI that searches chunks (placeholder for RAG)

Quick start

1. Create a virtual environment and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Ingest a repo (local path or git URL):

```bash
python src/ingest.py --repo ./some-repo --out data/myrepo
# or
python src/ingest.py --repo https://github.com/owner/repo.git --out data/myrepo
```

4. Chunk the ingested repo:

```bash
python src/chunker.py --in data/myrepo/raw --out data/myrepo/chunks.jsonl
```

5. Query (simple substring-based fallback):

```bash
python scripts/query_repo.py --chunks data/myrepo/chunks.jsonl --question "How does authentication work?"
```

Next steps:
- Replace the simple search in `scripts/query_repo.py` with embeddings + vector DB retrieval.
- Add `generate_docs.py` to run writer and reviewer agents (RAG pipeline).
- Add tests and CI.
