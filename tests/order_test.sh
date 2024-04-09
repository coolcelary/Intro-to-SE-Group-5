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

checkout_result=$(python3 ./backend/Order.py checkout 1 "test" "4444 test avenue." "test@test.com" "1234 1234 1234 1234" "23/23" "test" "697")
verify_result=$(python3 ./backend/Order.py verify 1 13)

echo "Testing Order Module:"

if [[ $checkout_result = "valid" ]]; then
	print_green "Checkout Works"
else
	print_red "Checkout Failed"
	exit 1
fi

if [[ $verify_result = "valid" ]]; then
	print_green "Order Verification Works"
else
	print_red "Order Verification Failed"
	exit 1
fi
