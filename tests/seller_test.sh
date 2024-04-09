#!/bin/bash
#
command_exists() {
	command -v "$1" >/dev/null 2>&1
}

print_green() {
	echo -e "\033[32m$@\033[0m"
}

print_red() {
	echo -e "\033[31m$@\033[0m"
}

login_result=$(python3 ./backend/Seller.py login "test_user" "testthis")
add_result=$(python3 ./backend/Seller.py add "Test Product" 100 "birhouses" "https://test.com" 1)
search_result=$(python3 ./backend/Seller.py search 1)

echo "Testing Seller Module:"

if [[ ! -z $login_result ]]; then
	print_green "Seller Login Works"
else
	print_red "Seller Login Failed"
	exit 1
fi

if [[ $add_result = "valid" ]]; then
	print_green "Add Product Works"
else
	print_red "Add Product Failed"
	exit 1
fi

if [[ ! -z $search_result ]]; then
	print_green "Search Seller Products Works"
else
	print_red "Search Seller Products Failed"
	exit 1
fi
