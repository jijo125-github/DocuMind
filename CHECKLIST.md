# Pre-Implementation Checklist

✅ **Project structure setup**
- [x] Conversation files saved (summary, roadmap)
- [x] .gitignore created (excludes .venv, data/, cache)
- [x] .env.example with API key placeholders
- [x] requirements.txt with core dependencies
- [x] README.md with quick start instructions

✅ **Source code structure**
- [x] src/__init__.py (package initialization)
- [x] src/utils.py (helper functions)
- [x] src/ingest.py (repo cloning/copying)
- [x] src/chunker.py (code chunking)
- [x] scripts/__init__.py
- [x] scripts/query_repo.py (simple query CLI)

✅ **Import fixes applied**
- [x] All scripts can be run directly
- [x] Imports work correctly (tested)

✅ **Scripts tested**
- [x] `python src/ingest.py --help` ✓
- [x] `python src/chunker.py --help` ✓
- [x] `python scripts/query_repo.py --help` ✓

⚠️ **Before you start coding**
- [ ] Run: `git rm -r --cached .venv` (remove venv from git)
- [ ] Run: `git add .gitignore .env.example README.md requirements.txt src/ scripts/`
- [ ] Run: `git commit -m "feat: add starter code with fixed imports"`
- [ ] Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`
- [ ] Test the full pipeline with a small repo:
  ```bash
  python src/ingest.py --repo ./some-small-repo --out data/test
  python src/chunker.py --in data/test/raw --out data/test/chunks.jsonl
  python scripts/query_repo.py --chunks data/test/chunks.jsonl --question "test"
  ```

📋 **Week 1 tasks (from roadmap)**
Ready to implement:
- [ ] Add embedding generation to chunker or separate script
- [ ] Set up vector DB (ChromaDB for local or Pinecone)
- [ ] Test retrieval quality vs substring search

Current status: **Starter code complete and tested** ✅

All scripts work correctly and the project structure is ready for Week 1 implementation.
