import hashlib
import os


def hash_password(password):
    """ Converts the received password into a hash for storage in the database """
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100000
    )
    return key.hex(), salt.hex()


def check_password(password, key, salt):
    """ Checks if the password is entered correctly """
    key = bytes.fromhex(key)
    salt = bytes.fromhex(salt)
    entered_key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100000
    )

    if key == entered_key:
        return True
    
    return False
