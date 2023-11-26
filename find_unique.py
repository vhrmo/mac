import os
from file_list import FILE_FOLDER, FILES_PROCESSED, FILES_TO_PROCESS


# read all pwds from FILES_PROCESSED and append them to a list
tested_pwds = []
for file in FILES_PROCESSED:
    with open(os.path.join(FILE_FOLDER, file), 'r') as f:
        tested_pwds += f.read().splitlines()

# convert the list to a set to remove duplicates
tested_pwds = set(tested_pwds)

print(f"Passwords loaded: {len(tested_pwds):,}")

# read all pwds from FILES_TO_PROCESS and create a new list with pwds not in pwds
pwds_to_process = []
for file in FILES_TO_PROCESS:
    with open(os.path.join(FILE_FOLDER, file), 'r') as f:
        pwds_to_process += f.read().splitlines()

pwds_to_process = set(pwds_to_process)

print(f"Passwords to process: {len(pwds_to_process):,}")

pwds_to_process = pwds_to_process - tested_pwds

print(f"Not tested passwords to process: {len(pwds_to_process):,}")

# remove pwds with spaces
pwds_to_process = [pwd for pwd in pwds_to_process if ' ' not in pwd]

print(f"Not tested passwords (reduced) : {len(pwds_to_process):,}")

# write the new list to a file
# file_name = 'xato-net-10-million-passwords-1000000.txt2'
file_name = FILES_TO_PROCESS[0] + '2'
with open(os.path.join(FILE_FOLDER, file_name), 'w') as f:
    for pwd in pwds_to_process:
        f.write(f"{pwd}\n")
    print(f"Data stored to '{file_name}'")