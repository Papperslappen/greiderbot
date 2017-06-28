import os
import base64

def token_bytes(nbytes=None):
    if nbytes is None:
        nbytes = 16
    return os.urandom(nbytes)

def token_urlsafe(nbytes=None):
    tok = token_bytes(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')
