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

if ! command_exists python3; then
	sudo apt install python3 python3-pip
else
	echo "Python3 already installed"
fi

add_result=$(python3 ./backend/Cart.py add 1 13)
search_result=$(python3 ./backend/Cart.py searchid 1)
remove_result=$(python3 ./backend/Cart.py remove 1 13)

if [[ $add_result = "valid" ]]; then
	print_green "Test 1 Passed..."
else
	print_red "Test 1 Failed..."
fi

if [[ ! -z $search_result ]]; then
	print_green "Test 2 Passed..."
else
	print_red "Test 2 Failed..."
fi

if [[ $remove_result = "valid" ]]; then
	print_green "Test 3 Passed..."
else
	print_red "Test 3 Failed..."
fi
