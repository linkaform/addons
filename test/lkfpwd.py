#!/usr/bin/python

# from sha import sha
from hashlib import md5, sha1
import sys


#class pwd(self):

def get_pwd(user_id):
    alias = 'client_{0}'.format(user_id)
    MONGO_SECRET = '_lkf'
    pswd =  sha1('{}{}'.format(md5(alias.encode('utf-8')).hexdigest(), MONGO_SECRET).encode('utf-8')).hexdigest()
    return pswd
