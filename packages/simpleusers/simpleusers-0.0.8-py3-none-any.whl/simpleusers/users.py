import os
import yaml
from passlib.hash import pbkdf2_sha256


class usermgr:
    """
    A class for managing user data and authentication.

    Attributes:
        srcdir (str): The directory where user data is stored.
    """

    def __init__(self):
        """
        Initializes the UserManager instance.

        Creates the data directory if it doesn't exist.
        """
        if not os.path.exists("db"):
            os.makedirs("db")
        self.srcdir = "db"

    def write_user(self, uid, obj):
        """
        Writes user data to a YAML file.

        Args:
            uid (str): User ID or filename.
            obj (dict): User data as a dictionary.

        Returns:
            None
        """
        with open(os.path.join(self.srcdir, uid), "w") as f:
            f.write(yaml.dump(obj))

    def get_user(self, uid):
        """
        Retrieves user data from a YAML file.

        Args:
            uid (str): User ID or filename.

        Returns:
            dict: User data as a dictionary.
        """
        if self.check_user_exists(uid):
            with open(os.path.join(self.srcdir, uid)) as f:
                obj = yaml.safe_load(f)
            return obj
        else:
            return {"message": "not found"}

    def check_user_exists(self, uid):
        """
        Checks if a user exists.

        Args:
            uid (str): User ID or filename.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        if uid == "" or uid is None:
            return False
        if os.path.exists(os.path.join(self.srcdir, uid)):
            return True
        return False

    def auth_user(self, uid, attempt):
        """
        Authenticates a user.

        Args:
            uid (str): User ID or filename.
            attempt (str): Password attempt for authentication.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        if self.check_user_exists(uid):
            phash = self.get_user(uid)["passw"]
            if pbkdf2_sha256.verify(attempt, phash):
                return True
        return False

    def make_user(self, uid, passw):
        """
        Creates a new user.

        Args:
            uid (str): User ID or filename.
            passw (str): User password.

        Returns:
            None
        """
        obj = {"passw": pbkdf2_sha256.hash(passw), "tokens": {}}
        self.write_user(uid, obj)

    def set_user_password(self, uid, newpass):
        """
        Sets a new password for a user.

        Args:
            uid (str): User ID or filename.
            newpass (str): New password.

        Returns:
            dict: Result message.
        """
        if self.check_user_exists(uid):
            obj = self.get_user(uid)
            hashed_pw = pbkdf2_sha256.hash(newpass)
            obj["passw"] = hashed_pw
            self.write_user(uid, obj)
            return {"message": "done."}
        else:
            return {"message": f"error: no such user {uid}"}

    def set_user_prop(self, uid, key, val):
        """
        Sets a property for a user.

        Args:
            uid (str): User ID or filename.
            key (str): Property key.
            val: Property value.

        Returns:
            dict: Result message.
        """
        if self.check_user_exists(uid):
            obj = self.get_user(uid)
            obj[key] = val
            self.write_user(uid, obj)
            return {"message": "done"}
        else:
            return {"message": f"error: no such user {uid}"}

    def dump_users(self):
        """
        Lists the users in the data directory.

        Returns:
            list: List of user filenames.
        """
        return os.listdir(self.srcdir)

    def set_auth_token(self, uid, ip, token):
        """
        Sets an authentication token for a user by IP address.

        Returns:
            bool: success
        """

        if self.check_user_exists(uid):
            obj = self.get_user(uid)
            obj["tokens"][ip] = token
            self.write_user(uid, obj)
            return True
        else:
            return False

    def expire_auth_token(self, uid, ip):
        """
        Expire auth token for user by ip address.
        """

        if self.check_user_exists(uid):
            obj = self.get_user(uid)
            obj["tokens"][ip] = ""
            self.write_user(uid, obj)
            return True
        else:
            return False

    def auth_user_with_token(self, uid, token):
        """
        Check if token is valid for user

        Returns:
            bool: success
        """

        if self.check_user_exists(uid):
            obj = self.get_user(uid)
            for ip in obj["tokens"]:
                if obj["tokens"][ip] == token:
                    return True

        return False
