#!/bin/bash

# Path to the password list file
password_list_file="$1"

script_dir=$(dirname "$0")

# Loop through each password in the file
while IFS= read -r password; do
    # Run the verification command with sudo and capture the exit code
    $script_dir/test_pw2.expect "$password" >/dev/null 2>&1
    exit_code=$?

    echo "Exit code: $exit_code, $password"


done < "$password_list_file"

