import sqlite3

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
        print("Error: Username and password are required.")
        return False

    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT UserID, Username FROM Authentication WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchall()
        for i in user:
            print(i)
        return True
    except sqlite3.Error as e:
        print("Error Logging in:", e)
        return False
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
    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    #insert register info into database
    try:
        cursor.execute("INSERT INTO Authentication (Username, Password, UserType, Email, PhoneNumber) VALUES (?, ?, ?, ?, ?)", (username, password, usertype, email, phoneNum))
        conn.commit()
        print("User registered successfully.")
        return True
    except sqlite3.Error as e:
        print("Error inserting user:", e)
        return False
    finally:
        conn.close()

## Test functions ##
#login_user('Guest', 'Guest123')
#register_user('Guest2', 'Guest2123', '1', 'guest@icloud.com', '4567890123')
#display_authentication_table()
