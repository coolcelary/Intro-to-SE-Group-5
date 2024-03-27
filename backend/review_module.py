import sqlite3
import sys
from Order import has_ordered

def add_review(UserID, ProductID, Username, Rating, review_text):
    # Check if the user has ordered the item
    if has_ordered(UserID, ProductID):
        # Connect to the SQLite database
        conn = sqlite3.connect('./backend/EcommerceDB.db')
        cursor = conn.cursor()

        # Insert review into the Reviews table
        try:
            cursor.execute("INSERT INTO Reviews (ReviewID, ProductID, Username, Rating, ReviewText) VALUES (NULL, ?, ?, ?, ?)",
                        (ProductID, Username, Rating, review_text.replace("\"", '')))
        except expression as identifier:
            print(expression)

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()
        #return "Review added successfully."
        print("valid")
    else:
        print("invalid")

def get_reviews(ProductID):
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    reviews = cursor.execute("SELECT * FROM Reviews WHERE ProductID = ?", (ProductID,)).fetchall()
    result = list()
    for row in reviews:
        item = dict()
        item["text"] = row[4]
        item["username"] = row[2]
        item["stars"] = row[3]
        result.append(item)
    print(result)


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "get":
        get_reviews(sys.argv[2])
    if command == "add":
        add_review(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
