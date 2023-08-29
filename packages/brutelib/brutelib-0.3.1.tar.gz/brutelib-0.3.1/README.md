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

def crack(): #Cracks hash md5 password and sha256 and normal password ( STRING PASSWORDS ) 
	[...]
"""
