import hashlib
import subprocess
import hashlib
wordlist = 'env/wordlist.txt'
hashlist = 'env/hashlist.txt'



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

def crack():
    method = input("{INSERT METHOD. 1 = Normal type, 2 = Hashes}: ")
    if (method == "1"):
        print("Cracking Password")
    with open(wordlist, 'r') as f:
        password = input("[]: ")
        if f.read().__contains__(password):
                print(f"Password found: {password} ")
        else:
            print("PASSWORD NOT FOUND")

    if method == "2":
        with open(hashlist) as hsh:
            hashpassword = input("[]: ")
            if hsh.read().__contains__(hashpassword):
                print(f'Password found: {hashpassword}')
            else:
                print(f'PASSWORD NOT FOUND')
            
    if not method == "1" and not method == "2":
        print("INSERT A VALID METHOD")
