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

login_result=$(python3 ./backend/Admin.py login testing testing)
get_result=$(python3 ./backend/Admin.py listall)

echo "Testing Review Module:"

if [[ $login_result = "1" ]]; then
	print_green "Admin Login Works"
else
	print_red "Admin Login Failed"
	exit 1
fi

if [[ ! -z $get_result ]]; then
	print_green "Get Users Works"
else
	print_red "Get Users Failed"
	exit 1
fi
