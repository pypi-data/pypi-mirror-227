from joserfc import jwt
import json
import time

from flask_app_security.password_utils import __gen_salt_custom__

def encode_dict(d: dict, secret_key: str, valid_time_ms = -1.0) -> str:
    """
    Encodes a python dictionary provided a secret key used to
    encode. Takes optional parameter for creating a timed
    encode. Meaning the encoded dict will have an expiriation.
    This is done by passing the time in ms as the third 
    parameter. If no 3rd parameter or -1 is passed, no time
    will be set and the encoded dict will not expire.
    """
    clone_dict = d.copy()
    if valid_time_ms != -1.0:
        cur_time = time.time()
        invalid_time = cur_time + (valid_time_ms/1000)
        clone_dict["__invalid_time__"] = str(invalid_time)
    salt = __gen_salt_custom__()
    clone_dict["__salt__"] = salt
    encoded = jwt.encode({"alg": "HS256"}, clone_dict, secret_key)
    return encoded

def decode_dict(string: str, secret_key: str) -> dict:
    """
    Decodes dict. Works with both timed and non-timed encodes.
    Returns None if expired or if invalid secret_key is given.
    """
    try:
        token = jwt.decode(string, secret_key)
        d = token.claims
        if "__invalid_time__" in d:
            cur_time = time.time()
            if cur_time >= float(d["__invalid_time__"]):
                return None
        del d["__salt__"]
        return d
    except:
        return None

def force_decode_dict(string: str, secret_key: str) -> dict:
    """
    !WARNING! Only use if you know what you are doing.
    This force reads the encoded dict even if the timer
    on the dict if expired. 
    """
    token = jwt.decode(string, secret_key)
    d = token.claims
    return d