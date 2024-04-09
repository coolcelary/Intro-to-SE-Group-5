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

add_result=$(python3 ./backend/review_module.py add 1 13 "testing username" 5 "This is a testing review")
get_result=$(python3 ./backend/review_module.py get 13)

echo $add_result

echo "Testing Review Module:"

if [[ $add_result != "Invalid" ]]; then
	print_green "Add Review Works"
else
	print_red "Add Review Failed"
	exit 1
fi

if [[ ! -z $get_result ]]; then
	print_green "Get Review Works"
else
	print_red "Get Review Failed"
	exit 1
fi
