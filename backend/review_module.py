import sqlite3
import sys
import Order

def add_review(ProductID, Username, Rating, review_text):
    # Check if the user has ordered the item
    try:
        if has_ordered(UserID, ProductID) == "valid":
            # Connect to the SQLite database
            conn = sqlite3.connect('ecommerceDB.db')
            cursor = conn.cursor()

            # Insert review into the Reviews table
            cursor.execute("INSERT INTO Reviews (ReviewID, ProductID, Username, Rating, ReviewText) VALUES (null, ?, ?, ?, ?)",
                        (ProductID, Username, Rating, review_text))

            # Commit the transaction
            conn.commit()

            # Close the connection
            conn.close()
            #return "Review added successfully."
        else:
            return "valid"
    except:
        return "invalid"

def get_reviews(ProductID):
    conn = sqlite3.connect('ecommerceDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ")