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

add_result=$(python3 ./backend/Cart.py add 1 13)
search_result=$(python3 ./backend/Cart.py searchid 1)
remove_result=$(python3 ./backend/Cart.py remove 1 13)

echo "Testing Cart Module:"

if [[ $add_result = "valid" ]]; then
	print_green "Add to Cart Works"
else
	print_red "Add to Cart Failed"
	exit 1
fi

if [[ ! -z $search_result ]]; then
	print_green "Search Cart Works"
else
	print_red "Search Cart Failed"
	exit 1
fi

if [[ $remove_result = "valid" ]]; then
	print_green "Remove from Cart Works"
else
	print_red "Remove from Cart Failed"
	exit 1
fi
