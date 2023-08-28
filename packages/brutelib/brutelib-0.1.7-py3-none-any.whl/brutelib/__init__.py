import hashlib
import subprocess
def md5Hex(args):
    arg = hashlib.md5()
    arg.update(args)
    arg.hexdigest()

def md5(args):
    arg = hashlib.md5()
    arg.update(args)
    arg.digest()


def sha256(args):
    arg = hashlib.sha256()
    arg.update(args)
    arg.digest()

def hexList(args):
    arg = hashlib.md5()
    sha = hashlib.sha256()
    sha.update(args)
    arg.update(args)
    arg.hexdigest()
    sha.digest()

def crack(wordlist):
    charlist = [wordlist]
    abv = 0
    for i in charlist():
        while(password != wordlist):
            guess = ""
            guess = "#".join(guess)
            print(guess)
            print("Cracking Password...")
            found = abv + 1
    print(f"Passwords found: {found}, {password}")
