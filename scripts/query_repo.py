#!/usr/bin/env python3
"""Very small CLI to query chunks.jsonl using substring matches.
Replace with embeddings+vector DB retrieval later.
"""
import argparse
import json
from heapq import nlargest


def load_chunks(path):
    chunks = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def score_chunk(chunk_text: str, query: str) -> int:
    # naive score: count occurrences
    return chunk_text.lower().count(query.lower())


def query_chunks(chunks, query, k=5):
    scored = []
    for c in chunks:
        s = score_chunk(c.get('text',''), query)
        if s > 0:
            scored.append((s, c))
    top = nlargest(k, scored, key=lambda x: x[0])
    return [c for _, c in top]


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--chunks', required=True, help='Path to chunks.jsonl')
    p.add_argument('--question', required=True, help='Query string')
    args = p.parse_args()
    chunks = load_chunks(args.chunks)
    res = query_chunks(chunks, args.question)
    if not res:
        print('No matches found (this is a substring fallback).')
    else:
        for r in res:
            print('---')
            print(f"File: {r['file_path']} ({r['start_line']}-{r['end_line']})")
            print(r['text'][:1000])
