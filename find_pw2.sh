#!/bin/bash

# Path to the password list file
password_list_file="$1"

# Prompt for the administrator password
#read -s -p "Enter administrator password for sudo: " admin_password
#echo

admin_password=admin1234567

# Loop through each password in the file
while IFS= read -r password; do
    # Run the verification command with sudo and capture the exit code
    #sudo -n firmwarepasswd -verify <<< "$password" 
    #<<< "$admin_password" 
    #sudo -S -l <<< "$admin_password" >/dev/null 2>&1
    ~/test_pw2.expect "$password" #>/dev/null 2>&1
    exit_code=$?

    echo "Exit code: $exit_code, $password"


done < "$password_list_file"

