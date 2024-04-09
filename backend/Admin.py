import sqlite3
import sys

def admin_login(username, password):
    if not username or not password:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()

    userid = cursor.execute("SELECT * FROM admin WHERE Username = ? AND Password = ?", (username, password,)).fetchone()
    if userid:
        print(userid[0])
        return
    else:
        return

def main():
    command = sys.argv[1]
    if command == "login":
        admin_login(sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
