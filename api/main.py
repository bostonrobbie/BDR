"""Entry point wrapper that adds batch 2 auto-import after init_and_seed."""
import index  # This runs init_and_seed() at module level, setting up the DB
app = index.app  # Export the FastAPI app for Vercel

# Now import batch 2 data (DB is ready after index module loaded)
import sqlite3
import os
from batch2_import import _auto_import_batch2

try:
    db_path = os.environ.get("OCC_DB_PATH", "/tmp/outreach.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        _auto_import_batch2(conn)
        conn.close()
        print("Batch 2 auto-import: completed via main.py wrapper")
except Exception as e:
    print(f"Batch 2 auto-import warning: {e}")
