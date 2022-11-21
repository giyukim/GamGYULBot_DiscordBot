import sqlite3

DB_DIR:str = "./sqlite3/DEV.db"

def main():
    conn = sqlite3.connect(DB_DIR)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ")
    conn.close()

if __name__ == "__main__":
    main()