from img_holder import *
from PIL import Image


class StegoProcessor:
    """
    Purpose:
        Provides capability to hide or extract an image
    """

    @staticmethod
    def extract_img(stego_img, extracted_img, password):
        """
        Purpose:
            Extracts an image from the carrier image
        Args:
            stego_img (ImageTk) - image carrying the secret image
            extracted_img (ImageTk) - image extracted from the carrier image
        Returns:
            0 - if extraction failed
            1 - if extraction passed
        """
    @staticmethod
    def hide_img(carrier_img, secret_img, stego_img, password, filename, err_msg=0):
        """
        Purpose:
            Hides an image in the carrier image
        Args:
            carrier_img (ImageTk) - image to carry the secret image
            secret_img (ImageTk) - image to hide in the carrier image
            stego_img (ImageTk) - carrier image with the secret image hidden inside
        Returns:
            0 - if hide failed
            1 - if hide passed
        """
        # Load images (PIL Image) and set y/x max into image holders
        carrier_load = Image.open(carrier_img.fullpath)
        carrier_img.x_max = carrier_load.size[0]
        carrier_img.y_max = carrier_load.size[1]

        secret_load = Image.open(secret_img.fullpath)
        secret_img.x_max = secret_load.size[0]
        secret_img.y_max = secret_load.size[1]

        if StegoProcessor.validate_stego_hide(carrier_img, secret_img):
            print("starting to hide image")
            # hide image code

    @staticmethod
    def validate_stego_extract(hidden_img, password):
        """
        Purpose:
            Validates hidden image can be extracted:
                - must be a .bmp image
        Args:
            hidden_img (ImageTk) - image to carrying the secret image
        Returns:
            0 - if invalid for stego extract processing
            1 - if valid for stego extract processing
        """
        # todo: right actual validate logic
        return 1

    @staticmethod
    def validate_stego_hide(carrier_img, secret_img):#, password, filename, err_msg=0):
        """
        Purpose:
            Validates secret image can be hidden in the carriers image:
                - carrier img size can hold secret (img size + password size + filename length) in LSB bits
                - carrier img is a .bmp
        Args:
            carrier_img (ImageTk) - image to carrying the secret image
            secret_img (ImageTk) - image to hide in carrier image
            password (str) - Password to be imbedded (used for extracting process)
            filename (str) - Name of the file to extract secret image as (20 char max)
            err_msg (str) - (Optional) If process setup is invalid, an error message is stored
        Returns:
            0 - if invalid for stego hide processing
            1 - if valid for stego hide processing
        """
        is_valid = 0

        # Validate all data can be hidden inside the carrier image
        carrier_holder_bits = carrier_img.get_pixel_count() * 3
        secret_bits_to_hide = secret_img.get_pixel_count() * 24

        if carrier_holder_bits < secret_bits_to_hide:
            print("Secret Image too big!")
            print("Carrier = " + str(carrier_holder_bits))
            print("Secret  = " + str(secret_bits_to_hide))

        # All validation passed
        is_valid = 1

        # todo: right actual validate logic
        return 1

        #print("holder 1: " + carrier_img.size + " -- holder 2: " + secret_img.size)
        #if carrier_img.size <= secret_img.size:
        #    print("Success!")