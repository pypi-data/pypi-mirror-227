import hashlib
import subprocess
from tools import *

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


