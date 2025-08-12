import os, duckdb
from .config import settings

conn = duckdb.connect(database=":memory:")

def has_table(name: str) -> bool:
    q = """SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_name = ?;"""
    n = conn.execute(q, [name]).fetchone()[0]
    return bool(n > 0)

def load_csv_to_reest(path: str | None = None) -> None:
    csv_path = path or settings.REEST_CSV_PATH
    if not os.path.exists(csv_path):
        return
    conn.execute("DROP TABLE IF EXISTS reest")
    conn.execute(f"CREATE TABLE reest AS SELECT * FROM read_csv_auto('{csv_path}', header=True)")
