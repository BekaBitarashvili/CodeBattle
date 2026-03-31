import sqlite3

def check_db_connection():
    try:
        conn = sqlite3.connect('local_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result == (1,):
            print("Success")
        else:
            print("Failed to connect to the database.")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_db_connection()
