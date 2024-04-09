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
	cat ./curl.out
	echo

	if [ "$response" -eq 200 ]; then
		print_green "curl to URL $url is successful"
	else
		print_red "curl to URL $url failed"
		exit 1
	fi
}

terminate() {
	ps aux | awk '/node/ && !/awk/{print $2}' | while read -r pid; do kill $pid; done
	exit 0
}

trap terminate SIGINT

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
nohup ./start_server.sh &
sleep 5
check_curl "http://localhost:3000/login"
check_curl "http://localhost:3000/register"
check_curl "http://localhost:3000/inventory"
#check_curl "http://localhost:3000/contact"
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
