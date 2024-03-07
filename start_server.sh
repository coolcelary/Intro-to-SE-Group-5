#!/bin/bash

# Function to check if a command is available
command_exists() {
	command -v "$1" >/dev/null 2>&1
}

# Check if Node.js is installed
if ! command_exists node; then
	echo "Node.js is not installed. Installing..."
	# Check if apt package manager is available
	if command_exists apt; then
		sudo apt update
		sudo apt install -y nodejs
	# Check if yum package manager is available
	elif command_exists yum; then
		sudo yum install -y nodejs
	else
		echo "Cannot install Node.js. Package manager not found."
		exit 1
	fi
fi

# Check if npm is installed
if ! command_exists npm; then
	echo "npm is not installed. Installing..."
	# Check if apt package manager is available
	if command_exists apt; then
		sudo apt update
		sudo apt install -y npm
	# Check if yum package manager is available
	elif command_exists yum; then
		sudo yum install -y npm
	else
		echo "Cannot install npm. Package manager not found."
		exit 1
	fi
fi

# Install required Node.js modules
echo "Installing required Node.js modules..."
npm install

# Run the Node.js Express server
echo "Starting Node.js Express server..."
node server.js
