import sqlite3
import sys

def display_authentication_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the Authentication table
    cursor.execute("SELECT * FROM Authentication")
    rows = cursor.fetchall()

    # Display the retrieved rows
    for row in rows:
        print("UserID:", row[0])
        print("Username:", row[1])
        print("Password:", row[2])
        print("UserType:", row[3])
        print("Email:", row[4])
        print("PhoneNumber:", row[5])
        print("")

    # Close the database connection
    conn.close()

def login_user(username, password):
    # Check if username and password are provided
    if not username or not password:
        #print("Error: Username and password are required.")
        return

    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    try:
        users = cursor.execute("SELECT UserID, Username FROM Authentication WHERE Username = ? AND Password = ?", (username, password))
        for user in users:
            return user[0]
    except sqlite3.Error as e:
        return
    finally:
        conn.close()

def register_user(username, password, usertype, email, phoneNum):
    # Check if username and password are provided
    if not username or not password:
        print("Error: Username and password are required.")
        return False
    
    # Check if email is provided and has a valid format
    if not email or '@' not in email:
        print("Error: Invalid or missing email address.")
        return False
    
    # Check if phone number is provided and is a valid integer
    try:
        phoneNum = int(phoneNum)
    except ValueError:
        print("Error: Phone number must be a valid integer.")
        return False
    # connect to database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    #insert register info into database
    try:
        cursor.execute("INSERT INTO Authentication (Username, Password, UserType, Email, PhoneNumber) VALUES (?, ?, ?, ?, ?)", (username, password, usertype, email, phoneNum))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        conn.close()

    def delete_user(username, password):
        # Check if username and password are provided
        if not username or not password:
            return False

        # connect to database
        conn = sqlite3.connect('./backend/EcommerceDB.db')
        cursor = conn.cursor()

        #delete user info from database
        try:
            cursor.execute("DELETE FROM Authentication WHERE Username = ? Password = ?", (username, password))
            conn.commit()
            return True
        except sqlite3.Error as e:
            return False
        finally:
            conn.close()


def main():
    command = sys.argv[1]
    argA = sys.argv[2]
    argB = sys.argv[3]
    if command == "login":
        result = login_user(argA, argB)
        if result:
            print(result)

    elif command == "register":
        argC = sys.argv[4]
        argD = sys.argv[5]
        argE = sys.argv[6]
        print(register_user(argA, argB, argC, argD, argE))


if __name__ == "__main__":
    main()
