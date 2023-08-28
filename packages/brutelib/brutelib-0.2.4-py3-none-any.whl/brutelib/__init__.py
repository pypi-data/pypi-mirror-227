import hashlib
import subprocess
def md5Hex(args):
    arg = hashlib.md5(args.encode('utf-8')).hexdigest()
    print(arg)

def md5(args):
    arg = hashlib.md5(args.encode('utf-8')).digest()
    print(arg)

def sha256(args):
    sha = hashlib.sha256(args.encode('utf-8')).digest()
    print(sha)
    
def sha256Hex(args):
    sha = hashlib.sha256(args.encode('utf-8')).hexdigest()
    print(sha)
    
def hexList(args):
    sha = hashlib.sha256(args.encode('utf-8')).hexdigest()
    print(sha)
    arg = hashlib.md5(args.encode('utf-8')).hexdigest
    print(arg)

def crack(wordlist):
    charlist = [wordlist]
    abv = 0
    password = charlist
    for i in charlist:
        while(password != wordlist):
            print("Cracking Password...")
            if (wordlist.__contains__(password)):
                found = abv + 1
    print(f"Passwords found: {found}, {password}")
