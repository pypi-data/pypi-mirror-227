# Building something
"""
def md5(args): - converts "args" to md5
    arg = hashlib.md5()
    arg.update(args)
    arg.digest()


def sha256(args): - converts "args" to sha256
    arg = hashlib.sha256()
    arg.update(args)
    arg.digest()

def hexList(args):  - Shows an hash list in md5 and sha256 
    arg = hashlib.md5()
    sha = hashlib.sha256()
    sha.update(args)
    arg.update(args)
    arg.hexdigest()
    sha.digest()

def crack(wordlist): - Cracks password
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


def newWordlist(wordPath): - Creates an new wordlist in PATH: "wordPath"
    subprocess.call(r"cd {wordPath}".format(wordPath))
    filename  = "wordlist.txt"
    text = "123456 password 123456789 12345 12345678 qwerty 1234567 1111 0123123"
    with open('wordlist.txt', 'w') as f:
        f.write(text)
"""
