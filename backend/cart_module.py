import sqlite3

def display_cart_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the Authentication table
    cursor.execute("SELECT * FROM Cart")
    rows = cursor.fetchall()

    # Display the retrieved rows
    for row in rows:
        print("CartID:", row[0])
        print("UserID:", row[1])
        print("ProductID:", row[2])
        print("Quantity:", row[3])
        print("Price:", row[4])
        print("")

    # Close the database connection
    conn.close()


def AddToCart(userID, productID, quantity):
    # Check if username and password are provided
    if not userID or not productID or not quantity:
        print("Error: UserID, ProductID, or Quantity not read.")
        return False

    # connect to database
    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Cart (UserID, ProductID, Quantity) VALUES (?, ?, ?, ?)", (userID, productID, quantity))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Error inserting product:", e)
        return False
    finally:
        conn.close()
    
def RemoveFromCart(userID, productID, quantity):
    # Check if username and password are provided
    if not userID or not productID or not quantity:
        print("Error: UserID, ProductID, or Quantity not read.")
        return False

    # connect to database
    conn = sqlite3.connect('EcommerceDB.db')
    cursor = conn.cursor()

    try:
        # Check if the item is in the cart and the quantity is sufficient
        cursor.execute("SELECT Quantity FROM Cart WHERE UserID = ? AND ProductID = ?", (userID, productID))
        row = cursor.fetchone()
        if row:
            current_quantity = row[0]
            print("Current quantity in cart:", current_quantity)
            print("Quantity requested to remove:", quantity)
            if current_quantity >= quantity:
                # Update the quantity in the cart
                new_quantity = current_quantity - quantity
                if new_quantity == 0:
                    # If the new quantity is 0, remove the item from the cart entirely
                    cursor.execute("DELETE FROM Cart WHERE UserID = ? AND ItemID = ?", (userID, productID))
                    print("Item removed from cart successfully.")
                else:
                    # Update the quantity of the item in the cart
                    cursor.execute("UPDATE Cart SET quantity = ? WHERE UserID = ? AND ProductID = ?", (new_quantity, userID, productID))
                    print("Quantity of item updated in cart successfully.")
                conn.commit()
            else:
                print("Insufficient quantity in the cart.")
        else:
            print("Item is not in the cart.")
    except sqlite3.Error as e:
        print("Error removing item from cart:", e)
    finally:
        conn.close()


##AddToCart(3, 345, 3)
##display_cart_table()
##RemoveFromCart(23,343,1)