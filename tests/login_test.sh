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

echo "Testing Login Module:"

sqlite3 ./backend/EcommerceDB.db "DELETE FROM Authentication;"
register_result=$(python3 ./backend/Login.py register "test" "testpass" "customer" "test@test.com" "1001001000")
login_result=$(python3 ./backend/Login.py login "test" "testpass")

if [[ $register_result = "True" ]]; then
	print_green "Register Works"
else
	print_red "Register Failed"
	exit 1
fi

if [ ! -z $login_result ]; then
	print_green "Login Works"
else
	print_red "Login Failed"
	exit 1
fi
