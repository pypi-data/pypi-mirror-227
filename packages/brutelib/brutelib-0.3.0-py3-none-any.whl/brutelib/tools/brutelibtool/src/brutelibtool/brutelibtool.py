import hashlib
wordlist = 'env/wordlist.txt'
hashlist = 'env/hashlist.txt'


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
