import json
from cryptography.fernet import Fernet

class Encrypto:
    """
    A class for encrypting and decrypting data using Fernet encryption.

    Methods:
        encrypt(data, key): Encrypts the provided data using the given key.
        decrypt(encrypted_text, key): Decrypts the encrypted text using the given key.
        generate_key(): Generates a new encryption key.
    """
    
    def encrypt(self, data, key):
        """
        Encrypts the provided data using the given key.

        Args:
            data (dict or str): The data to be encrypted. If dict, it will be JSON-encoded before encryption.
            key (str): The encryption key.

        Returns:
            str: The encrypted text.
        
        Raises:
            ValueError: If an unsupported data type is provided for encryption.
        """
        if isinstance(data, dict):
            json_data = json.dumps(data)
            encrypted_text = self._encrypt_text(json_data, key)
        elif isinstance(data, str):
            encrypted_text = self._encrypt_text(data, key)
        else:
            raise ValueError("Unsupported data type for encryption")
        return encrypted_text
    
    def decrypt(self, encrypted_text, key):
        """
        Decrypts the encrypted text using the given key.

        Args:
            encrypted_text (str): The encrypted text to be decrypted.
            key (str): The encryption key.

        Returns:
            dict or str: The decrypted data. If decryption fails, returns the decrypted text.

        Note:
            If the decrypted text is a valid JSON format, it will be parsed and returned as a dict.
            Otherwise, the decrypted text itself will be returned.
        """
        decrypted_json = self._decrypt_text(encrypted_text, key)
        try:
            decrypted_data = json.loads(decrypted_json)
            return decrypted_data
        except json.JSONDecodeError:
            return decrypted_json
    
    # Rest of the class methods...
    def _encrypt_text(self, text, key):
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(text.encode())
        return encrypted_text.decode()
    
    def _decrypt_text(self, encrypted_text, key):
        cipher_suite = Fernet(key)
        decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
        return decrypted_text
    
    def generate_key(self):
        return Fernet.generate_key().decode()

# Module-level instance of Encrypto
encrypto = Encrypto()

"""
An instance of the `Encrypto` class created at the module level for convenience.
You can use this instance to access the class methods without instantiating the class explicitly.
"""

    

