import string
from secrets import choice, token_hex
from hashlib import sha256

def __hash_password_custom__(password: str, salt: str) -> str:
    """
    Creates a sha256 hash given a password string and a string of salt.
    """
    temp_password = password + salt
    hashed_password = sha256(temp_password.encode("utf-8")).hexdigest()
    return hashed_password

def __gen_salt_custom__(length: int = 8) -> str:
    """
    Creates a string of random letters and numbers provided a string
    length. By default the string will have a length of 8 if no length
    is provided.
    """
    alphabet = string.ascii_letters + string.digits
    salt = ''.join(choice(alphabet) for i in range(length))
    return salt

def __gen_login_token__(length: int = 32) -> str:
    """
    Creates a token to be stored on the client side to validate login.
    This should be used instead of storing the users password directly
    on the client side.
    """
    token = token_hex(length)
    return token

class Secured_Password:
    """
    Call to_string() to convert to string

    Use from_string(str) to convert string to Secured_Password
    """
    def __init__(self, password_hash, salt, login_token):
        self.password_hash: str = password_hash
        self.salt: str = salt
        self.login_token: str = login_token

    def to_string(self) -> str:
        """
        Creates a string that can be stored in a database.
        This string can later be used to create another
        instance of Secured_Password using its static
        from_string() method.
        """
        out = "-".join([self.password_hash,self.salt,self.login_token])
        return out
    
    def __equals__(self, other) -> bool:
        """
        Not used to validate user inputed password!
        Please use validate_password or validate_login_token
        for that.
        """
        return (
            self.password_hash == other.password_hash and
            self.salt == other.salt and
            self.login_token == other.login_token
        )

    @staticmethod
    def from_string(string: str):
        """
        Creates a Secured_Password instance from a string.
        Used to convert the string returned by this class'
        to_string() method back into a Secured_Password.
        """
        array = string.split("-")
        if len(array) != 3:
            raise Exception("Invalid string format")
        return Secured_Password(array[0], array[1], array[2])


def secure_password(password: str) -> Secured_Password:
    """
    Secures a password by generating a random string of "salt"
    and then hashing the password+salt. This is done to prevent
    duplicate passwords from having the same hash. A login_token
    is also generated. This should be stored !!SECURELY!! on the
    client side for the use of remembering the user. 
    """
    salt = __gen_salt_custom__()
    temp_password = password + salt
    hashed_password = sha256(temp_password.encode("utf-8")).hexdigest()
    token = __gen_login_token__()
    
    return Secured_Password(hashed_password, salt, token)

def validate_password(password: str, _secured_password):
    """
    Takes a plain text password and a Secured_Password and returns
    if the password is correct.

    Note: the Secured_Password can either be an instance of
    Secured_Password OR it can be the string returned from
    Secured_Password's to_string() method
    """
    secured_password = _secured_password
    if type(_secured_password) == str:
        secured_password = Secured_Password.from_string(_secured_password)
    
    hashed_password = __hash_password_custom__(password, secured_password.salt)
    return hashed_password == secured_password.password_hash

def validate_login_token(login_token: str, _secured_password):
    """
    Takes a plain login_token and a Secured_Password and returns
    if the login_token is correct.

    Note: the Secured_Password can either be an instance of
    Secured_Password OR it can be the string returned from
    Secured_Password's to_string() method
    """
    secured_password = _secured_password
    if type(_secured_password) == str:
        secured_password = Secured_Password.from_string(_secured_password)
    
    return login_token == secured_password.login_token