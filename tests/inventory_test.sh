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

search_result=$(python3 ./backend/Inventory.py search "Flower" "birdhouses")
idsearch_result=$(python3 ./backend/Inventory.py idsearch "1")

echo "Testing Inventory Module:"

if [[ ! -z $search_result ]]; then
	print_green "Search Inventory Works"
else
	print_red "Search Inventory Failed"
	exit 1
fi

if [[ ! -z $idsearch_result ]]; then
	print_green "Search by ID Works"
else
	print_red "Search by ID Failed"
	exit 1
fi
