import qrcode
import cv2

class QRCodeManager:
    def save(self, text, filename):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        qr_data = qr.make_image(fill_color="black", back_color="white")
        qr_data.save(filename + ".png")

    def show(self, text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        qr_data = qr.make_image(fill_color="black", back_color="white")
        qr_data.show()

    def read(self, qr_file):
        """Read the QR code from the file and return the text."""
        img = cv2.imread(qr_file)
        qrcode_detector = cv2.QRCodeDetector()
        data, _, _ = qrcode_detector.detectAndDecode(img)

        if data is None:
            return None
        return data

    def test(self):
        while True:
            print("1. Save QR Code")
            print("2. Show QR Code")
            print("3. Read QR Code")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                text = input("Enter the text to encode: ")
                filename = input("Enter the filename (without extension): ")
                QRCodeManager.save(text, filename)
            elif choice == "2":
                text = input("Enter the text to encode: ")
                QRCodeManager.show(text)
            elif choice == "3":
                filename = input("Enter the QR code image filename: ")
                decoded_text = QRCodeManager.read(filename)
                print("Decoded Text:", decoded_text)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please select a valid option.")

# module-level instance 
QRCodeManager = QRCodeManager()

