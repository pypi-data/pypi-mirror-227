import json
from cryptography.fernet import Fernet
import time

class Encrypto:
    def encrypt(self, data, key):
        if isinstance(data, dict):
            json_data = json.dumps(data)
            encrypted_text = self._encrypt_text(json_data, key)
        elif isinstance(data, str):
            encrypted_text = self._encrypt_text(data, key)
        else:
            raise ValueError("Unsupported data type for encryption")
        return encrypted_text
    
    def decrypt(self, encrypted_text, key):
        decrypted_json = self._decrypt_text(encrypted_text, key)
        try:
            decrypted_data = json.loads(decrypted_json)
            return decrypted_data
        except json.JSONDecodeError:
            return decrypted_json
    
    def _encrypt_text(self, text, key):
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(text.encode())
        return encrypted_text
    
    def _decrypt_text(self, encrypted_text, key):
        cipher_suite = Fernet(key)
        decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
        return decrypted_text
    
    def generate_key(self):
        return Fernet.generate_key()

    def test(self):
        while True:
            # genrating key
            print("\n\n Encrypto By Kaushal Chaudhary \n")

            def get_choice():
                while True:
                    choice = input("Enter your choice: ")
                    try:
                        choice = int(choice)
                        return choice
                    except:
                        print("Please Enter Numbers Only!!")
            
            def ch_1():
                print("Genrating Key...")
                print(f"Genrated Key is : {encrypto.generate_key()}\n")
                time.sleep(2)

            def ch_2():
                print("Text Encryption")
                print(f"Encrypted Text is: {encrypto.encrypt(input('Enter text to encrypt: '), input('Enter Key: '))}\n")
                time.sleep(2)

            def ch_3():
                print("Text Decryption")
                print(f"Decrypted Text is: {encrypto.decrypt(input('Enter text to Decrypt: '), input('Enter Key: '))}\n")
                time.sleep(2)

            print("Select options:\n [1] Genrate Key \n [2] Encrypt Text\n [3] Decrypt Text\n [4] Exit")
            choice = get_choice()
            if choice == 1 :
                ch_1()
            elif choice == 2:
                ch_2()
            elif choice == 3:
                ch_3()
            else:
                break

            print("[1] Back to Menu, [2] Exit Program")
            if get_choice() == 2: 
                break



                

# Create a module-level instance of Encrypto
encrypto = Encrypto()
