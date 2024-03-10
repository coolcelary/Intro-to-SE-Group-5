import sqlite3
import sys


def post_massage(name, email, message):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    if name == "" or email == "" or message == "":
        print("message invalid")
        
    try:
        cursor.execute("INSERT INTO contact (id, name, email, message) VALUES (NULL, ?, ?, ?)", (name, email, message))
        conn.commit()
    except:
        print("message invalid")
        return
    print("message OK")


if __name__ == "__main__":
    name = sys.argv[1]
    email = sys.argv[2]
    message = sys.argv[3]
    post_massage(name, email, message)
