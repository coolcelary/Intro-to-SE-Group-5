import sqlite3
import sys




def login(username, password, cursor):
    users = cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    for user in users:
        if user[2] == password:
            return True
        else:
            return False
    return False

def main():
    # Open the Database for writing
    conn = sqlite3.connect('./Database.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    command = sys.argv[1]
    arg1 = sys.argv[2]
    arg2 = sys.argv[3]
    if command == "login":
        print(login(arg1, arg2, cursor))

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()




