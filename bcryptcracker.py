#!/usr/bin/env python3
########################USAGE###############################
# How to use:
# 1. Replace the 'hash' and the 'salt' bellow
# 2. Call it like this:
# Eg. root@Kali:~# ./bcryptcracker.py rockyou.txt
# Eg. root@Kali:~# python3 bcryptcracker.py rockyou.txt
############################################################

import time
import bcrypt
import base64
from multiprocessing import Pool
from signal import signal, SIGINT
from sys import exit
from termcolor import colored
from pwn import *

# PUT HERE YOUR SALT AND HASH
salt   = b'$2b$12$SVInH5XmuS3C7eQkmqa6UO'
myhash = b'$2b$12$SVInH5XmuS3C7eQkmqa6UOM6sDIuumJPrvuiTr.Lbz3GCcUqdf.z6'

start_time = time.time()

def keyHandler(sig, frame):
  log.failure(colored("Ctrl + C pressed. Program ended...\n", "red"))
  print(f"Total elapsed time: {int(time.time() - start_time)} seconds")
  sys.exit(1)
signal.signal(signal.SIGINT, keyHandler)

def usageHint():
  log.failure(colored("How to use:", "red"))
  print('''
1. Open the code and replace the 'hash' and 'salt' values 
2. Run the code specifying the password wordlist, like this:
Eg. root@Kali:~# ./bcryptcracker.py rockyou.txt
Eg. root@Kali:~# python3 bcryptcracker.py rockyou.txt

If the hash matches a password that is in the wordlist, it will find.
  ''',)

def showBanner():
  print("""
   __                     __       
  / /  __________ _____  / /_      
 / _ \/ __/ __/ // / _ \/ __/      
/_.__/\__/_/  \_, / .__/\__/       
  ________  _/___/_/____ _________ 
 / ___/ _ \/ _ |/ ___/ //_/ __/ _ \\
/ /__/ , _/ __ / /__/ ,< / _// , _/
\___/_/|_/_/ |_\___/_/|_/___/_/|_|                                                                                       
  """)

def prepareWordlist(dictionary):
  try:
    dictionary = open (dictionary, 'r').read().splitlines()
    passwords = []
    for word in dictionary:
      passwords.append(word)
    return passwords
  except Exception:
    log.failure(colored("Wordlist not found.\n", "red"))
    sys.exit(1)

def crackHash(passwords):
  process = log.progress("")
  process.status("Starting the Hash Cracking...")
  time.sleep(2)
  for password in passwords:
    bcrypt_pass = password.encode('ascii','ignore')
    passed = str(base64.b64encode(bcrypt_pass))
    hash_and_salt = bcrypt.hashpw(passed.encode(), salt)
    process.status(f"Testing with the password: {password}")
    if ( hash_and_salt == myhash ):
      process.success(colored(f"Password Found: {password}", "green"))
      print(f"\nTotal elapsed time: {int(time.time() - start_time)} seconds")
      sys.exit(0)
  process.failure(colored("Password Not Found.", "red"))
  print(f"\nTotal elapsed time: {int(time.time() - start_time)} seconds")
  sys.exit(1)

def main():
  try:
    if len(sys.argv) > 2 or len(sys.argv) < 2:
      usageHint()
    else:
      dictionary = sys.argv[1]
      passwords = prepareWordlist(dictionary)
      showBanner()
      crackHash(passwords)
  except Exception as e:
    log.error(str(e))

if __name__ == '__main__':
  main()
