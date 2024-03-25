import sqlite3
import sys
import Order

def add_review(ProductID, UserID, Rating, review_text):
    # Check if the user has ordered the item
    try:
        if has_ordered(UserID, ProductID) == "valid":
            # Connect to the SQLite database
            conn = sqlite3.connect('ecommerceDB.db')
            cursor = conn.cursor()

            # Insert review into the Reviews table
            cursor.execute("INSERT INTO Reviews (ProductID, UserID, Rating, ReviewText) VALUES (?, ?, ?, ?)",
                        (ProductID, UserID, Rating, review_text))

            # Commit the transaction
            conn.commit()

            # Close the connection
            conn.close()
            #return "Review added successfully."
        else:
            return "You have not purchased this item."
    except sqlite3.Error as e:
        return "Error: Failed to add review. " + str(e)