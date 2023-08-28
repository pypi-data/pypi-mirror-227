import qrcode
import cv2  # opencv-python

class qrmanager:
    """
    A class for managing QR codes including generation, display, and reading.

    This class provides methods to generate, display, and read QR codes.

    Attributes:
        None

    Methods:
        save(self, text, filename): Generate and save a QR code image to a file.
        show(self, text): Generate and display a QR code containing the provided text.
        read(self, qr_file): Read a QR code image from a file and return the decoded text.
    """
    
    def save(self, text, filename):

        """
        Generate and save a QR code image to a file.

        Args:
            text (str): The text to be encoded in the QR code.
            filename (str): The desired filename for the saved image (without extension).

        Returns:
            None

        This method creates a QR code using the qrcode library with the provided text and saves it as a PNG image.

        Example:
            qr_manager = qrmanager()
            qr_manager.save("https://www.example.com", "example_qr")
        """
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
        """
        Generate and display a QR code containing the provided text.

        Args:
            text (str): The text to be encoded in the QR code.

        Returns:
            None

        This method creates a QR code using the qrcode library with the provided text. The generated QR code is displayed using the default image viewer.

        Example:
            qr_manager = qrmanager()
            qr_manager.show("https://www.example.com")
        """
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
        """
        Read the QR code from the file and return the decoded text.

        Args:
            qr_file (str): The path to the QR code image file.

        Returns:
            str or None: The decoded text from the QR code, or None if the QR code cannot be read.
        """
        img = cv2.imread(qr_file)
        qrcode_detector = cv2.QRCodeDetector()
        data, _, _ = qrcode_detector.detectAndDecode(img)

        if data is None:
            return None
        return data

qrmanager = qrmanager()