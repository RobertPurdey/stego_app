from img_holder import *
from PIL import Image
from Crypto.Util import strxor
from Crypto.Hash import SHA

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
        # todo: potential to move decryption to own class??
        # Extract encrypted data from stego image
        stego_load = Image.open(stego_img.fullpath)
        stego_img.x_max = stego_load.size[0]
        stego_img.y_max = stego_load.size[1]

        # Get RGB color channels
        red_c = stego_load.split()[0]
        green_c = stego_load.split()[1]
        blue_c = stego_load.split()[2]

        encrypted_data = open("encrypted_data", "w")

        # read encrypted data into a file
        for i in range(stego_img.x_max):
            for j in range(stego_img.y_max):
                bit_1 = red_c.getpixel(i, j)[-1]
                bit_2 = green_c.getpixel(i, j)[-1]
                bit_3 = blue_c.getpixel(i, j)[-1]
                data = str(bit_1) + str(bit_2) + str(bit_3)
                encrypted_data.write(data)

        # decrypt encrypted data file
        key = password

        # decrypt 48 pixels (6 bytes) (filename + file ext)
        # decrypt 48 pixels (6 bytes) (file size to read in bytes)
        # decrypt n chars where n is the amount of bytes to read

    @staticmethod
    def hide_img(carrier_img, secret_img, stego_img, password, filename, err_msg=0):
        """
        Purpose:
            Hides an image in the carrier image
        Args:
            carrier_img (Image) - image holder for carrier img
            secret_img (ImageTk) - image holder for secret image
            stego_img (ImageTk) - image holder for stego image
        Returns:
            0 - if hide failed
            1 - if hide passed
        """
        # Load images (PIL Image) and set y/x max into image holders
        # todo: this could be done by holder class at some point?
        carrier_load = Image.open(carrier_img.fullpath)
        carrier_img.x_max = carrier_load.size[0]
        carrier_img.y_max = carrier_load.size[1]

        secret_load = Image.open(secret_img.fullpath)
        secret_img.x_max = secret_load.size[0]
        secret_img.y_max = secret_load.size[1]

        if StegoProcessor.validate_stego_hide(carrier_img, secret_img):
            print("starting to hide image")

            # Carrier RGB
            car_red_p = carrier_load.split()[0]
            car_green_p = carrier_load.split()[1]
            car_blue_p = carrier_load.split()[2]

            # Secret RGB
            car_red_p = secret_load.split()[0]
            car_green_p = secret_load.split()[1]
            car_blue_p = secret_load.split()[2]

            print("car_red_p")
            # convert ascii to binary
            #bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.filename])
            #bin_filefrmt = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.frmt])
            #bin_img_bits = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.frmt])
            #bin_password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.password])
            stego_pixels = carrier_img.get_pixel_count()
            ind = -1
            red_bit = 0
            green_bit = 1
            blue_bit = 2
            for i in range(carrier_img.x_max):
                for j in range(carrier_img.y_max):
                    # set last bit of each rgb pixel
                    for y in range(0, 3):
                        # set last red bit
                        if y == red_bit:
                        # set last green_bit
                            x=1
                        if y == green_bit:
                        # set last blue bit
                            x=2
                        if y == blue_bit:
                            y=3
            # hide image code

            # Add filename to secret image

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
            carrier_img (Image) - image to carrying the secret image
            secret_img (Image) - image to hide in carrier image
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
