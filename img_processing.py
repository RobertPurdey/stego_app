from img_holder import *
from PIL import Image
from Crypto.Util import strxor
from Crypto.Hash import SHA
from io import BytesIO
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

        # decrypt encrypted data file (xor bit string)
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
            sec_red_p = secret_load.split()[0]
            sec_green_p = secret_load.split()[1]
            sec_blue_p = secret_load.split()[2]

            # Stego RGB image
            stego_image = Image.new("RGB", (carrier_img.x_max, carrier_img.y_max))
            stego_pixels = stego_image.load()

            print(str(bin(sec_red_p.getpixel((0, 0)))))
            print("car_red_p")
            # convert ascii to binary
            #bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.filename])
            #bin_filefrmt = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.frmt])
            #bin_img_bits = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.frmt])
            #bin_password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in stego_img.password])

            # todo: convert filename / frmt / size into file

            # convert pixels in secret image to bit string file (easy to work with)
            bit_data = open("bit_data_to_hide", "w")
            for i in range(secret_img.x_max):
                for j in range(secret_img.y_max):
                    r, g, b = carrier_load.getpixel((i, j))
                    br = bin(r)[2:].zfill(8)
                    bg = bin(g)[2:].zfill(8)
                    bb = bin(b)[2:].zfill(8)
                    b_data = br + bg + bb
                    bit_data.write(b_data)

            bit_data.close()
            bit_data = open("bit_data_to_hide", "r")

            # todo: encrypt data (XOR??)

            # store stego data into new image (at this point should have filename, and image size)
            for i in range(carrier_img.x_max):
                for j in range(carrier_img.y_max):
                    r, g, b = carrier_load.getpixel((i, j))
                    dbytes = bit_data.read(3)
                    bytes_read = len(dbytes)
                    r = bin(r)
                    g = bin(g)
                    b = bin(b)
                    if bytes_read == 3:
                        r = str(r)[:-1] + dbytes[0]
                        g = str(g)[:-1] + dbytes[1]
                        b = str(b)[:-1] + dbytes[2]
                    elif bytes_read == 2:
                        r = str(r)[:-1] + dbytes[0]
                        g = str(g)[:-1] + dbytes[1]
                    elif bytes_read == 1:
                        r = str(r)[:-1] + dbytes[0]

                    stego_pixels[i, j] = (int(r, 2), int(g, 2), int(b, 2))
            stego_image.save("setgo_image_hidden.bmp")

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
