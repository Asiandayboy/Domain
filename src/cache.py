import sqlite3


CACHE_FILE_NAME = "cache.db"
SQL_CACHE_TABLE_NAME = "cache"

SQL_QUERY_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {SQL_CACHE_TABLE_NAME} (
    prompt TEXT PRIMARY KEY,
    response TEXT
)
"""


SQL_QUERY_GET_CACHED_RESPONSE = f"SELECT response FROM {SQL_CACHE_TABLE_NAME} where prompt = ?"
SQL_QUERY_SET_CACHED_RESPONSE = f"REPLACE into {SQL_CACHE_TABLE_NAME} values (?, ?)"


def init_db():
    with sqlite3.connect(CACHE_FILE_NAME) as conn:
        conn.execute(SQL_QUERY_CREATE_TABLE)


def get_cached_response(prompt):
    with sqlite3.connect(CACHE_FILE_NAME) as conn:
        cur = conn.cursor()
        cur.execute(SQL_QUERY_GET_CACHED_RESPONSE, (prompt,))
        row = cur.fetchone()
        return row[0] if row else None
    

def set_cached_response(prompt, response):
    with sqlite3.connect(CACHE_FILE_NAME) as conn:
        conn.execute(SQL_QUERY_SET_CACHED_RESPONSE, (prompt, response))