from img_holder import *
from PIL import Image
import binascii

class StegoProcessor:
    """
    Purpose:
        Provides capability to hide or extract an image
    """
    _xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}

    @staticmethod
    def extract_img(stego_img, secret_img, password):
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
        # Extract encrypted data from stego image
        stego_load = Image.open(stego_img.fullpath)
        stego_img.x_max = stego_load.size[0]
        stego_img.y_max = stego_load.size[1]

        # Secret image
        secret_load = Image.open(secret_img.fullpath)
        secret_img.x_max = secret_load.size[0]
        secret_img.y_max = secret_load.size[1]

        # Image to store extracted img
        secret_found = Image.new("RGB", (secret_img.x_max, secret_img.y_max))
        secret_load = secret_found.load()
        encrypted_data = open("encrypted_data_extract", "w")
        pixels_read = 0
        pixels_total = secret_img.get_pixel_count() * 24
        print("TOTAL PIXELS To read = " + str(pixels_total))

        # read encrypted data into a file (files are just images as is)
        for i in range(stego_img.x_max):
            for j in range(stego_img.y_max):
                r, g, b = stego_load.getpixel((i, j))
                data = ""
                r = bin(r)[-1]
                g = bin(g)[-1]
                b = bin(b)[-1]

                if pixels_read <= pixels_total - 4:
                    data = str(r) + str(g) + str(b)
                    pixels_read += 3
                elif pixels_read == pixels_total - 3:
                    data = str(r) + str(g)
                    pixels_read += 2
                elif pixels_read == pixels_total - 2:
                    data = str(r)
                    pixels_read += 1

                encrypted_data.write(data)
        print("PIXELS READ = " + str(pixels_read))
        encrypted_data.close()
        encrypted_data = open("encrypted_data_extract", "r")
        decrypted_data = open("decrypted_data_extract", "w")

        # todo: decrypt data (XOR cipher) based on password
        # Decrypt XOR bit string data to hide
        xor_bit_len = len("11001100110011")
        temp_pass = "11001100110011"
        bytes_read = encrypted_data.read(xor_bit_len)
        xor_data = ""
        print("before XOR: " + bytes_read)

        while len(bytes_read) > 0:
            # last read XOR only necessary amount
            if len(bytes_read) < xor_bit_len:
                shrt_pass = temp_pass[0:len(bytes_read)]
                xor_data = ''.join([StegoProcessor._xormap[a, b] for a, b in zip(bytes_read, shrt_pass)])
            else:
                xor_data = ''.join([StegoProcessor._xormap[a, b] for a, b in zip(bytes_read, temp_pass)])

            # next password is bytes read
            temp_pass = bytes_read
          #  print("after XOR:  " + str(xor_data))
            decrypted_data.write(xor_data)
            bytes_read = encrypted_data.read(xor_bit_len)
          #  print("before XOR: " + bytes_read)
          #  print("plus XOR:   " + temp_pass)

        encrypted_data.close()
        decrypted_data.close()

        # todo: read image filename / file size from set storage bytes

        # Save decrypted image
        read_rgb = ""
        decrypted_data = open("decrypted_data_extract", "r")
        sets_o_24 = 0
        right_24 = pixels_total / 24
        print("expected total sets" + str(right_24))

        # create image from extracted img data
        for i in range(secret_img.x_max):
            for j in range(secret_img.y_max):
                # read rgb byte string (8 bytes per pixel)
                read_rgb = decrypted_data.read(24)
                # todo: perform XOR decode here? rather than decrypt whole file then read
                if read_rgb == "" or len(read_rgb) < 24:
                    print("Break!")
                    break

                r = int(read_rgb[0:8], 2)
                g = int(read_rgb[8:16], 2)
                b = int(read_rgb[16:24], 2)
                secret_load[i, j] = (r, g, b)

            if read_rgb == "" or len(read_rgb) < 24:
                break
        secret_found.save("found_the_image.bmp")
        #key = password

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

            # Stego RGB image
            stego_image = Image.new("RGB", (carrier_img.x_max, carrier_img.y_max), "white")
            stego_pixels = stego_image.load()

            # todo: convert filename / frmt / size into file
            # hold entire bit data string to hide in carrier image
            bit_data_file = open("bit_data_file", "w")

            # convert ascii to binary for storage data
            # - (password (8-16 bits)
            # - filename length (8 bits)
            # - filename
            # - image width (16 bits) max = 2^16 - 1
            # - image height (16 bits) max = 2^16 - 1
            # - image bit data string length (32 bits)
            # - image bit string
            # - header length for data
           # bin_password = ''.join([bin(ord(ch))[2:].zfill(144) for ch in secret_img.password])  # read 144 bits
           ## bin_filename_len = ''.join([bin(len(secret_img.filename))]).zfill(5)  # read 5 bits
            #bin_filename = ''.join([bin(ord(ch))[2:] for ch in secret_img.filename])  # read filename_len bits
            #bin_file_fmt = ''.join([bin(ord(ch))[2:] for ch in secret_img.frmt])  # read 32 bits
            #bin_img_width = ''.join([bin(ord(ch))[2:].zfill(16) for ch in secret_img.x_max])  # read 16 bits
            #bin_img_height = ''.join([bin(ord(ch))[2:].zfill(16) for ch in secret_img.y_max])  # read 16 bits
            #bin_img__bit_data_len = ''.join([bin(secret_img.get_pixel_count()*24)[2:]]).zfill(32)  # read pixel co
            #bin_hdr = bin_password + \
            #    bin_filename_len + \
            #    bin_filename + \
            #    bin_file_fmt +\
            #    bin_password + \
            #    bin_img_width +\
            #    bin_img_height +\
            #    bin_img__bit_data_len
            #bin_hdr_len = ''.join([bin(len(bin_hdr))[2:]]).zfill(32)  # read pixel co
            #bin_hdr = bin_hdr_len + bin_hdr

            # write entire header into file
            #bit_data_file.write(bin_hdr)

            for i in range(secret_img.x_max):
                for j in range(secret_img.y_max):
                    r, g, b = secret_load.getpixel((i, j))
                    br = bin(r)[2:].zfill(8)
                    bg = bin(g)[2:].zfill(8)
                    bb = bin(b)[2:].zfill(8)
                    b_data = br + bg + bb
                    bit_data_file.write(b_data)
                    #if x == 1:
                    #    print("HIDING")
                     #   print("R: " + br)
                      #  print("G: " + bg)
                     #   print("B: " + bb)
                     #   x = 2

            bit_data_file.close()
            bit_data_file = open("bit_data_file", "r")
            bit_data_encrypted_file = open("bit_data_encrypted_file", "w")

            # todo: encrypt data (XOR based off password)
            # Encrypt XOR bit string data to hide
            xor_bit_len = len("11001100110011")
            temp_pass = "11001100110011"
            bytes_read = bit_data_file.read(xor_bit_len)
            xor_data = ""
          #  print("before XOR: " + bytes_read)

            while len(bytes_read) > 0:
                # last read XOR only necessary amount
                if len(bytes_read) < xor_bit_len:
                    shrt_pass = temp_pass[0:len(bytes_read)]
                    xor_data = ''.join([StegoProcessor._xormap[a, b] for a, b in zip(bytes_read, shrt_pass)])
                else:
                    xor_data = ''.join([StegoProcessor._xormap[a, b] for a, b in zip(bytes_read, temp_pass)])

                # new password is XOR_data from previous password
                temp_pass = xor_data
                #xor_data = xor_data[::-1]
               # xor_data = binascii.a2b_qp(xor_data).decode()
               # print("after XOR:  " + str(xor_data))
                bit_data_encrypted_file.write(xor_data)
                bytes_read = bit_data_file.read(xor_bit_len)
              #  print("before XOR: " + bytes_read)
               # print("plus XOR:   " + temp_pass)

            bit_data_file.close()
            bit_data_encrypted_file.close()
            bit_data_encrypted_file = open("bit_data_encrypted_file", "r")

            # store stego data into new image (at this point should have filename, and image size all encrypted)
            for i in range(carrier_img.x_max):
                for j in range(carrier_img.y_max):
                    r, g, b = carrier_load.getpixel((i, j))
                    dbytes = bit_data_encrypted_file.read(3)
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
            stego_image.save("stego_image_hidden.bmp")

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
        secret_bits_to_hide = (secret_img.get_pixel_count() * 24)# + str((len(5) + len(10) * 8))

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
