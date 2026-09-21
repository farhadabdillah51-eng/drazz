#!/usr/bin/env python3
"""Check schema and add story content + scenes"""
import sqlite3

DB = 'd:/WEBCERITAA/cerita-nusantara/database/cerita_nusantara.db'
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# Check tables
tables = [r['name'] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)

# Check schema for each table
for t in tables:
    cols = db.execute(f"PRAGMA table_info({t})").fetchall()
    print(f"\n--- {t} ---")
    for c in cols:
        print(f"  {c['name']} ({c['type']})")

# Check stories content
print("\n--- STORY CONTENT ---")
for s in db.execute("SELECT id, title, content, description FROM stories").fetchall():
    print(f"ID:{s['id']} | {s['title']}")
    print(f"  content: {s['content'][:100] if s['content'] else 'EMPTY'}...")
    print(f"  desc: {s['description'][:80] if s['description'] else 'EMPTY'}...")

db.close()
