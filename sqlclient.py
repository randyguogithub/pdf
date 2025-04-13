import sqlite3
# Initialize SQLite database

# --- Classes ---
class DBclint():
    """
    Represents a dog with a name and breed.
    """
    def __init__(self):
        self.db_name = "data/data.db"
        self.init_db()
    def init_db(self):
        # self.run_sql("DROP TABLE companies")
        sql = """
        CREATE TABLE IF NOT EXISTS companies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                created_by TEXT NOT NULL,
                auditor TEXT NOT NULL DEFAULT 'admin',
                status TEXT NOT NULL DEFAULT 'draft',
                created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """
        self.run_sql(sql)
        sql = """
        CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL default 'user',
                lastlogin TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """
        self.run_sql(sql)
        # sql = """
        # CREATE TABLE IF NOT EXISTS users (
        #         id TEXT PRIMARY KEY,
        #         username TEXT NOT NULL,
        #         email TEXT NOT NULL,
        #         password TEXT NOT NULL,
        #         role TEXT NOT NULL default 'user',
        #         lastlogin TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        #     )
        # """
        # self.run_sql(sql)
    def run_sql(self,sql=None, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)    
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
