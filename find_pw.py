import os
import sys
import pexpect


COMMAND = "firmwarepasswd -verify"
FILE_FOLDER = '/Users/admin/SecLists/Passwords'
FILE_FOLDER = '/Users/vlado/Projects/SecLists/Passwords'

FILES_PROCESSED = [
    'xato-net-10-million-passwords-100000.txt',
    'Keyboard-Combinations.txt',
    'UserPassCombo-Jay.txt',
    'bt4-password.txt',
    'Most-Popular-Letter-Passes.txt',
    'darkweb2017-top10000.txt',
    'darkweb2017-top1000.txt',
    'darkweb2017-top100.txt',
    'days.txt',
    'months.txt',
]

FILES_TO_PROCESS = [
    'xato-net-10-million-passwords-100.txt',
]

FILES_TO_PROCESS = [

    'openwall.net-all.txt',


    '500-worst-passwords.txt',
    '2020-200_most_used_passwords.txt',
    'cirt-default-passwords.txt',
    'citrix.txt',
    'clarkson-university-82.txt',
    'common_corporate_passwords.lst',
    'darkc0de.txt',
    'der-postillon.txt',
    # 'dutch_common_wordlist.txt',
    'dutch_passwordlist.txt',
    'german_misc.txt',
    'mssql-passwords-nansh0u-guardicore.txt',
    'PHP-Magic-Hashes.txt',
    'probable-v2-top207.txt',
    'probable-v2-top1575.txt',
    'probable-v2-top12000.txt',
    'richelieu-french-top5000.txt',
    'richelieu-french-top20000.txt',
    'scraped-JWT-secrets.txt',
    'seasons.txt',
    'stupid-ones-in-production.txt',
    'twitter-banned.txt',
    'unkown-azul.txt',
    'xato-net-10-million-passwords.txt',
    'xato-net-10-million-passwords-1000000.txt',
    'xato-net-10-million-passwords-dup.txt',

]


def load_tested_pwds():
    # read all pwds from FILES_PROCESSED and append them to a list
    tested_pwds = []
    for file in FILES_PROCESSED:
        with open(os.path.join(FILE_FOLDER, file), 'r') as f:
            tested_pwds += f.read().splitlines()

    # convert the list to a set to remove duplicates
    tested_pwds = set(tested_pwds)

    print(f"Passwords loaded: {len(tested_pwds):,}")
    return tested_pwds


def sort_files_to_process_by_size():
    # sort FILES_TO_PROCESS by number of lines
    files_to_process = []
    for file in FILES_TO_PROCESS:
        # get the number of lines in the file
        # print(file)
        with open(os.path.join(FILE_FOLDER, file), 'r') as f:
            lines = f.readlines()
            files_to_process.append((file, len(lines)))

    files_to_process.sort(key=lambda x: x[1], reverse=False)

    # print the size and file name
    for file in files_to_process:
        print(f"{file[1]:,}  {file[0]}")

    return files_to_process


def test_pwds(pwds):
    # test each pwd against the command
    for pwd in pwds:
        # print(f"Testing {pwd}...")
        child = pexpect.spawn(COMMAND, timeout=10)
        child.expect('Enter password:')
        child.sendline(pwd)
        child.expect(pexpect.EOF)

        test_result = child.before.decode('utf-8')
        # print(test_result)

        if "Correct" in test_result:
            print(f"Password found: {pwd}")
            sys.exit(1)
        # else:
        #     print(f"Password not found: {pwd}")

        child.close()


def test_file(file_name):
    # read all pwds from the file
    with open(os.path.join(FILE_FOLDER, file_name), 'r') as f:
        pwds_to_process = f.read().splitlines()

    pwds_to_process = set(pwds_to_process)
    pwds_to_process = pwds_to_process - tested_pwds
    # remove pwds with spaces
    pwds_to_process = [pwd for pwd in pwds_to_process if ' ' not in pwd]

    print(f"Testing {len(pwds_to_process):,} passwords from '{file_name}' ...")

    # test the pwds
    #test_pwds(pwds_to_process)

    return pwds_to_process


tested_pwds = set()
tested_pwds = load_tested_pwds()
files_to_process = sort_files_to_process_by_size()

print("\nTesting:")

for file in files_to_process:
    tested_pwds = tested_pwds.union(test_file(file[0]))

