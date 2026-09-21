import sqlite3

db_path = 'd:/WEBCERITAA/cerita-nusantara/database/cerita_nusantara.db'
db = sqlite3.connect(db_path)

# Update all stories to approved
db.execute("UPDATE stories SET status='approved'")
db.commit()

# Verify
rows = db.execute("SELECT id, title, status FROM stories").fetchall()
for r in rows:
    print(f"ID:{r[0]} | {r[1]} | Status: {r[2]}")

db.close()
print("All stories set to approved!")
