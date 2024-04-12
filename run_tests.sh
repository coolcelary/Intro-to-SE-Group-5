#!/bin/bash

print_title() {
	local yellow='\033[1;33m'
	local reset='\033[0m'
	echo -e "${yellow}$1${reset}"
}

print_green() {
	echo -e "\033[32m$@\033[0m"
}

print_red() {
	echo -e "\033[31m$@\033[0m"
}

check_curl() {
	local url="$1"
	local response=$(curl -L -X GET -s -o curl.out -w "%{http_code}" "$url")

	if [ "$response" -eq 200 ]; then
		print_green "curl to URL $url is successful"
	else
		cat ./curl.out
		echo
		print_red "curl to URL $url failed"
		exit 1
	fi
}

terminate() {
	ps aux | awk '/node/ && !/awk/{print $2}' | while read -r pid; do kill $pid; done
	exit 0
}

trap terminate SIGINT

print_title "Creating Testing Database"

# Refresh the database
rm -f ./backend/EcommerceDB.db
touch ./backend/EcommerceDB.db

# Create Database structure
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE Authentication (
    UserID INTEGER PRIMARY KEY,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    UserType TEXT NOT NULL,
    Email TEXT,
    PhoneNumber TEXT
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY,
    UserID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER,
    Name TEXT,
    Address TEXT,
    Email TEXT,
    CardNumber TEXT,
    ExpirationDate TEXT,
    CardName TEXT,
    CVV INTEGER
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE contact (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE Cart (
    UserID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (UserID) REFERENCES Authentication(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE Reviews (
    ReviewID INTEGER PRIMARY KEY,
    ProductID INTEGER,
    Username TEXT,
    Rating INTEGER,
    ReviewText TEXT,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE admin (
    AdminID INTEGER PRIMARY KEY,
    Username TEXT,
    Password TEXT
);"
sqlite3 ./backend/EcommerceDB.db "CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT,
    SellerID INTEGER,
    FOREIGN KEY (SellerID) REFERENCES Sellers(SellerID)
);"

# Add preliminary data
sqlite3 ./backend/EcommerceDB.db "INSERT INTO admin (AdminID, Username, Password) VALUES (NULL, 'testing', 'testing');"

print_title "Adding Products..."

sqlite3 ./backend/Products.db "SELECT * FROM products;" | while IFS="|" read -r product_id name price category image_url SellerID; do
	nm=$(echo $name | sed "s/'//g")
	pr=$(echo $price | sed "s/'//g")
	ct=$(echo $category | sed "s/'//g")
	img=$(echo $image_url | sed "s/'//g")
	sel=$(echo $SellerID | sed "s/'//g")
	insert_stmt="INSERT INTO products (product_id, name, price, category, image_url, SellerID) VALUES (NULL, '$nm', '$pr', '$ct', '$img', '$sel')"
	echo $insert_stmt
	sqlite3 ./backend/EcommerceDB.db "$insert_stmt"
done

print_title "Running Python Backend Tests:"

check_failure() {
	if [ ! $? -eq 0 ]; then
		echo "Test Failed"
		exit 1
	fi
}

./tests/login_test.sh
check_failure
./tests/inventory_test.sh
check_failure
./tests/cart_test.sh
check_failure

# Create a testing cart
python3 ./backend/Cart.py add 1 13 >/dev/null
python3 ./backend/Cart.py add 1 13 >/dev/null
python3 ./backend/Cart.py add 1 14 >/dev/null

./tests/order_test.sh
check_failure
./tests/review_test.sh
check_failure

python3 ./backend/Login.py register "test_user" "testthis" "seller" "test@test.com" 123123123 >/dev/null

./tests/seller_test.sh
check_failure
./tests/admin_test.sh
check_failure

print_title "Running Server Tests:"
command_exists() {
	command -v "$1" >/dev/null 2>&1
}

if ! command_exists node; then
	echo "Node.js is not installed. Installing..."
	if command_exists apt; then
		sudo apt update
		sudo apt install -y nodejs
	elif command_exists yum; then
		sudo yum install -y nodejs
	else
		print_red "Cannot install Node.js. Package manager not found."
		exit 1
	fi
fi

if ! command_exists npm; then
	echo "npm is not installed. Installing..."
	if command_exists apt; then
		sudo apt update
		sudo apt install -y npm
	elif command_exists yum; then
		sudo yum install -y npm
	else
		print_red "Cannot install npm. Package manager not found."
		exit 1
	fi
fi

print_green "Installing required Node.js modules..."
npm install

print_green "Starting Node.js Express server..."
nohup node server.js >./server.out &

while true; do
	done=$(cat ./server.out | grep -o "localhost")
	if [ ! -z $done ]; then
		print_green "Server Ready"
		break
	fi
	echo "Waiting"
	sleep 0.1
done

sleep 2
check_curl "http://localhost:3000/login"
check_curl "http://localhost:3000/register"
check_curl "http://localhost:3000/inventory"
check_curl "http://localhost:3000/contact"
check_curl "http://localhost:3000/about"
check_curl "http://localhost:3000/checkout"
check_curl "http://localhost:3000/admin"
check_curl "http://localhost:3000/sellers_add"
check_curl "http://localhost:3000/sellers_view"
check_curl "http://localhost:3000/review/13"
check_curl "http://localhost:3000/hasPurchased/13"
check_curl "http://localhost:3000/more_info"
check_curl "http://localhost:3000/cart_search"
check_curl "http://localhost:3000/search"
rm -rf ./curl.out ./nohup.out
print_title "All test completed successfully."

terminate
