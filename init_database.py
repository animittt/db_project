import psycopg2

DATABASE = "dekanat"
USER = "AniMit"
PASSWORD = "parol8"
HOST = "83.149.198.142"
PORT = "5432"

def init_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {DATABASE} OWNER {USER};")
        print(f"{DATABASE} created")

    except psycopg2.Error as e:
        print(f"error during database creation: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()