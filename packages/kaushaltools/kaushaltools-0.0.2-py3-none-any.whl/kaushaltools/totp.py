import pyotp
import re
import time
import os
from kaushaltools.qrmanager import qrmanager

class totp:
    """
    A class for generating and managing Time-Based One-Time Passwords (TOTP).

    This class provides methods to generate TOTP keys, generate OTPs, create 2FA URLs, show and save QR codes, scan QR codes, and authenticate using OTPs.

    Attributes:
        None

    Methods:
        generate_key(self, num_characters=int, prefix=Str, suffix=None): Generate a TOTP key.
        get_otp(self, key=Str): Generate an OTP using a TOTP key.
        generate_url(self, secret=str, label=str, issuer=str): Generate a 2FA URL.
        show_qr(self, secret=str, label=str, issuer=str): Display a QR code for a 2FA URL.
        save_qr(self, secret=str, label=str, issuer=str, filename=str): Save a QR code as an image.
        scan_qr(self, qr_code_path): Scan a QR code and extract the secret key, label, and issuer.
        authenticate(self, key, otp): Authenticate a provided OTP against a key. Key can be a picture path or key itself.
    """
    
    def generate_key(self, num_characters=None, prefix=None, suffix=None):
        """
        Generate a Time-Based One-Time Password (TOTP) key.

        Args:
            num_characters (int, optional): The number of characters in the key. Default is 32.
            prefix (str, optional): Prefix to be added to the generated key. Default is None.
            suffix (str, optional): Suffix to be added to the generated key. Default is None.

        Returns:
            str: The generated TOTP key.

        Example:
            totp.generate_key(num_characters=32, prefix="first", suffix="Last")
        """
        if num_characters is None:
            num_characters = 32
        else:
            num_characters = int(num_characters)
        
        if num_characters < 32:
            num_characters = 32
        
        key = pyotp.random_base32(length=num_characters)
        
        if prefix is not None:
            key = prefix + key[len(prefix):]

        if suffix is not None:
            key = key[:-len(suffix)] + suffix

        return re.sub(r'[^a-zA-Z0-9]', '', key).upper()

    def get_otp(self, key = None):
        """
        Generate an OTP from the given key.

        Args:
            key (str): The TOTP key.

        Returns:
            str: The generated OTP.

        Example:
            totp.get_otp("ESZ3EEXWUQRRMFU5Y5VDOIXMZCZKVATH")
        """
        if key is None:
            return "Please Provide Key."
        
        totp = pyotp.TOTP(key)
        return totp.now()

    def generate_url(self, secret=None, label=None, issuer=None):
        """
        Generate a 2FA URL.

        Args:
            secret (str): The TOTP key.
            label (str, optional): Label for the key. Default is "2FA".
            issuer (str, optional): Issuer of the key. Default is "kaushaltools".

        Returns:
            str: The generated 2FA URL.

        Example:
            totp.generate_url(secret="ESZ3EEXWUQRRMFU5Y5VDOIXMZCZKVATH", label="my_label", issuer="google")
        """
        if secret is None:
            raise ValueError("Secret key is required to generate the URL.")
        
        if label is None:
            label = "2FA"
        if issuer is None:
            issuer = "kaushaltools"

        label = label.replace(" ", "%20")
        issuer = issuer.replace(" ", "%20")
        secret = re.sub(r'[^a-zA-Z0-9]', '', secret).upper()

        return f"otpauth://totp/{label}?secret={secret}&issuer={issuer}"

    def show_qr(self, secret=None, label=None, issuer=None):
        """
        Display a QR code for a 2FA URL.

        Args:
            secret (str): The TOTP key.
            label (str, optional): Label for the key. Default is "2FA".
            issuer (str, optional): Issuer of the key. Default is "kaushaltools".

        Returns:
            None

        Example:
            totp.show_qr(secret="ESZ3EEXWUQRRMFU5Y5VDOIXMZCZKVATH", label="my_label", issuer="google")
        """
        if secret is None:
            raise ValueError("Secret key is required to generate the QR code.")
        
        qrmanager.show(self.generate_url(secret, label, issuer))

    def save_qr(self, secret=None, label=None, issuer=None, filename=None):
        """
        Save a QR code as an image.

        Args:
            secret (str): The TOTP key.
            label (str, optional): Label for the key. Default is "2FA".
            issuer (str, optional): Issuer of the key. Default is "kaushaltools".
            filename (str, optional): Name for saving the image. Default is None.

        Returns:
            None

        Example:
            totp.save_qr(secret="ESZ3EEXWUQRRMFU5Y5VDOIXMZCZKVATH", label="my_label", issuer="google", filename="my_qr_code.png")
        """
        if secret is None:
            raise ValueError("Secret key is required to generate the QR code.")

        url = self.generate_url(secret, label, issuer)

        if filename is None:
            if issuer is None and label is None:
                name = "2FA QR - " + time.strftime("%y%m%d%H%M%S", time.localtime())
            elif issuer is None:
                name = label
            elif label is None:
                name = issuer
            else:
                name = issuer + " - " + label
        else:
            name = filename

        qrmanager.save(text=url, filename=name)

    def scan_qr(self, qr_code_path):
        """
        Scan a QR code and extract the secret key, label, and issuer.

        Args:
            qr_code_path (str): Path to the QR code image.

        Returns:
            dict: Dictionary containing secret key, label, and issuer.

        Example:
            result = totp.scan_qr("my_qr_code.png")
        """
        url = qrmanager.read(qr_code_path)
        
        key_pattern = r"secret=([A-Z0-9]+)"
        label_pattern = r"otpauth://totp/([^?]+)"
        issuer_pattern = r"issuer=([^&]+)"

        key_match = re.search(key_pattern, url)
        label_match = re.search(label_pattern, url)
        issuer_match = re.search(issuer_pattern, url)

        if key_match:
            secret_key = key_match.group(1)
        else:
            raise ValueError("Secret key not found in the QR.")
        
        if label_match:
            label = label_match.group(1).replace("%20", " ")
        else:
            label = None
        
        if issuer_match:
            issuer = issuer_match.group(1).replace("%20", " ")
        else:
            issuer = None

        return {
            "key": secret_key,
            "label": label,
            "issuer": issuer
        }
    
    def authenticate(self, key, otp):
        """
        Authenticate a provided OTP against a key.

        Args:
            key (str): The TOTP key or the path to a QR code image.
            otp (str or int): The OTP to be authenticated.

        Returns:
            bool: True if OTP is valid, False otherwise.

        Example:
            authenticated = totp.authenticate("ESZ3EEXWUQRRMFU5Y5VDOIXMZCZKVATH", "123456")
        """
        def identify_input(input_str):
            image_path_pattern = r"\.(jpg|jpeg|png|gif|bmp)$"
            if re.search(image_path_pattern, input_str, re.IGNORECASE) and os.path.exists(input_str):
                return 1  # Image file

            key_string_pattern = r"^[A-Z0-9]+$"
            if re.match(key_string_pattern, input_str):
                return 0  # String file

            return 0  # Unknown

        if identify_input(key):
            secret_key = self.scan_qr(key)['key']
        else:
            secret_key = key
        
        if str(otp) == self.get_otp(secret_key):
            return True
        else:
            return False

totp = totp()
