import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    # Convert the password to bytes and hash it
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")  # Convert back to string for storage


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        password (str): The plaintext password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Compare the password to the hashed password
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
