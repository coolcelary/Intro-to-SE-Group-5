import sqlite3

def insert_testing_users():
    # Connect to the SQLite database
    conn = sqlite3.connect('./EcommerceDB.db')
    cursor = conn.cursor()

    # Insert testing users
    users = [
        ('user1', 'password1', 'user1@example.com'),
        ('user2', 'password2', 'user2@example.com'),
        ('user3', 'password3', 'user3@example.com')
    ]

    cursor.executemany('''
        INSERT INTO Authentication (username, password, email)
        VALUES (?, ?, ?)
    ''', users)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_testing_users()
    print("Testing users inserted into the database successfully.")
