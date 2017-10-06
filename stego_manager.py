class StegoManager:
    """
    Purpose:
        Coordinates the process of extracting / hiding images

        Extracting Process:
            - Validate process can be done
            - Extract secret image from stego image
            - Decrypt secret image

        Hiding Process:
            - Validate process can be done
            - Encrypt secret image
            - Hide secret image in carrier image
    """

    def hide_process(self, carrier_img, secret_img, stego_img):
        """
        Purpose:
            Encrypts secret img and hides in carrier img creating the stego img.
        Args:
            carrier_img (ImageTk) - image to carry the secret image
            secret_img (ImageTk) - image to hide in the carrier image
            stego_img (ImageTk) - carrier image with the secret image hidden inside
        Returns:
            0 - if hide process failed
            1 - if hide process passed
        """

    def extract_process(self, secret_img, stego_img):
        """
        Purpose:
            Extracts img from stego img and decrypts to create original secret img
        Args:
            secret_img (ImageTk) - image extracted from stego image
            stego_img (ImageTk) - carrier image with the secret image hidden inside
        Returns:
            0 - if extract process failed
            1 - if extract process passed
        """