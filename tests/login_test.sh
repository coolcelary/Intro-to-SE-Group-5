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

sqlite3 ./backend/EcommerceDB.db "DELETE FROM Authentication;"
register_result=$(python3 ./backend/Login.py register "test" "testpass" "customer" "test@test.com" "1001001000")
login_result=$(python3 ./backend/Login.py login "test" "testpass")

if [[ $register_result = "True" ]]; then
	print_green "Test 1 Passed..."
else
	print_red "Test 1 Failed..."
fi

if [ ! -z $login_result ]; then
	print_green "Test 2 Passed..."
else
	print_red "Test 2 Failed..."
fi
