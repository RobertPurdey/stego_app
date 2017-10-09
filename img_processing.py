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
    def extract_img(stego_img, password):
        """
        Purpose:
            Extracts an image from the carrier image
        Args:
            stego_img (StegoImgHolder) - data for image carrying secret image
            password (str) - password used to encrypt image
        Returns:
            0 - if extraction failed
            1 - if extraction passed
        """
        # Extract encrypted data from stego image
        stego_load = Image.open(stego_img.fullpath)
        stego_img.x_max = stego_load.size[0]
        stego_img.y_max = stego_load.size[1]
        # encrypted data
        encrypted_data = open("encrypted_data_extract", "w")

        # read encrypted data into a file (files are just images as is)
        for i in range(stego_img.x_max):
            for j in range(stego_img.y_max):
                r, g, b = stego_load.getpixel((i, j))
                data = ""
                r = bin(r)[-1]
                g = bin(g)[-1]
                b = bin(b)[-1]
                data = str(r) + str(g) + str(b)

                encrypted_data.write(data)
        #print("PIXELS READ = " + str(pixels_read))
        encrypted_data.close()
        encrypted_data = open("encrypted_data_extract", "r")
        decrypted_data = open("decrypted_data_extract", "w")

        # Decrypt XOR bit string data to hide
        temp_pass = ''.join([bin(ord(ch))[2:].zfill(8) for ch in password]).zfill(144)  # read 144 bits
        xor_bit_len = len(temp_pass)
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

        decrypted_data = open("decrypted_data_extract", "r")

        # read password
        bytes_read_cnt = 0
        bin_password = decrypted_data.read(144)
        bytes_read_cnt += 144
        password = ''.join(chr(int(bin_password[i:i+8], 2)) for i in range(0, len(bin_password), 8))
        print("Decoded password: " + str(password))

        # read filename len
        bin_filename_len = decrypted_data.read(5)
        bytes_read_cnt += 5
        filename_len = int(bin_filename_len, 2)
        print("File length: " + str(filename_len))

        # read in filename
        bin_filename = decrypted_data.read(filename_len*8)
        bytes_read_cnt += filename_len*8
        filename = ''.join(chr(int(bin_filename[i:i + 8], 2)) for i in range(0, len(bin_filename), 8))
        print("Filename: " + filename)

        # read in file format
        bin_file_frmt = decrypted_data.read(32)
        bytes_read_cnt += 32
        file_frmt = ''.join(chr(int(bin_file_frmt[i:i + 8], 2)) for i in range(0, len(bin_file_frmt), 8))
        print("File format: " + file_frmt)

        # read image width
        bin_img_width = decrypted_data.read(16)
        bytes_read_cnt += 16
        img_width = int(bin_img_width, 2)
        print("File width: " + str(img_width))

        # read image height
        bin_img_height = decrypted_data.read(16)
        bytes_read_cnt += 16
        img_height = int(bin_img_height, 2)
        print("File height: " + str(img_height))

        # read image width
        bin_img_bit_data_len = decrypted_data.read(32)
        bytes_read_cnt += 32
        img_bit_data_len = int(bin_img_bit_data_len, 2)
        print("File length: " + str(img_bit_data_len))
        #bin_password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in "fake"]).zfill(144)  # read 144 bits
        #bin_filename_len = ''.join([bin(len(new_filename))[2:]]).zfill(5)  # read 5 bits
        #bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in new_filename])  # read filename_len bits
        #bin_file_fmt = ''.join([bin(ord(ch))[2:].zfill(8) for ch in secret_img.frmt])  # read 32 bits
        #bin_img_width = bin(secret_img.x_max)[2:].zfill(16)  # read 16 bits
        #bin_img_height = bin(secret_img.y_max)[2:].zfill(16)  # read 16 bits
        #bin_img_bit_data_len = ''.join([bin(secret_img.get_pixel_count() * 24)[2:]]).zfill(32)  # 2^32-1 pixels max
        print("BYTES READ: = " + str(bytes_read_cnt))
        # Save decrypted image
        # Image to store extracted img
        secret_found = Image.new("RGB", (img_width, img_height))
        secret_load = secret_found.load()
        pixels_read = 0
        pixels_total = img_bit_data_len
        print("TOTAL PIXELS To read = " + str(pixels_total))
        read_rgb = ""
        sets_o_24 = 0
        #right_24 = pixels_total / 24
        #print("expected total sets" + str(right_24))
        # for testing strip off expected header length
        #decrypted_data.read(277)
        # create image from extracted img data
       # print("s image x = " + str(secret_img.x_max))
        #print("s image y = " + str(secret_img.y_max))
        for i in range(img_width):
            for j in range(img_height):
                # read rgb byte string (8 bytes per pixel)
                read_rgb = decrypted_data.read(24)
                r = int(read_rgb[0:8], 2)
                g = int(read_rgb[8:16], 2)
                b = int(read_rgb[16:24], 2)

                secret_load[i, j] = (r, g, b)
                pixels_read += len(read_rgb)

        secret_found.save(filename + file_frmt)

    @staticmethod
    def hide_img(carrier_img, secret_img, new_filename, stego_img_name, password):
        """
        Purpose:
            Hides an image in the carrier image
        Args:
            carrier_img (Image) - image holder for carrier img
            secret_img (ImageTk) - image holder for secret image
            new_filename (str) - Filename when extracting hidden image
            stego_img_name (str) - Stego image filename to save as (always .bmp)
            password (str) - password to encrypt header info + secret img pixels
        Returns:
            0 - if hide failed
            1 - if hide passed
        """

        print("PASSWORD PASSED IN: " + password)
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
            # TOTAL Header length for testing =
            bin_password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in password]).zfill(144)  # read 144 bits
            bin_filename_len = ''.join([bin(len(new_filename))[2:]]).zfill(5)  # read 5 bits
            bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in new_filename])  # read filename_len bits
            bin_file_fmt = ''.join([bin(ord(ch))[2:].zfill(8) for ch in secret_img.frmt])  # read 32 bits
            bin_img_width = bin(secret_img.x_max)[2:].zfill(16)  # read 16 bits
            bin_img_height = bin(secret_img.y_max)[2:].zfill(16)  # read 16 bits
            bin_img_bit_data_len = ''.join([bin(secret_img.get_pixel_count()*24)[2:]]).zfill(32)  # 2^32-1 pixels max

            bin_hdr = bin_password + \
                bin_filename_len + \
                bin_filename + \
                bin_file_fmt + \
                bin_img_width + \
                bin_img_height + \
                bin_img_bit_data_len

            #bin_hdr_len = ''.join([bin(len(bin_hdr))[2:]]).zfill(16)  # read pixel co
            #bin_hdr = bin_hdr_len + bin_hdr

            print("Pass:" + bin_password)
            print("Pass len:" + str(len(bin_password)))
            print("file len " + bin_filename_len)
            print("filename " + bin_filename)
            print("frmt " + bin_file_fmt)
            print("width: " + bin_img_width)
            print("height: " + bin_img_height)
           # print("bit data len: " + bin_img_bit_data_len)
            #print("hdr len: " + bin_hdr_len)
           # print(bin_img_bit_data_len)
            # write entire header into file
            bit_data_file.write(bin_hdr)
            print(str(len(bin_hdr)))
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
            xor_bit_len = len(bin_password)
            temp_pass = bin_password
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

            # Stego RGB image
            stego_image = Image.new("RGB", (carrier_img.x_max, carrier_img.y_max))
            stego_pixels = stego_image.load()

            # store stego data into new image
            for i in range(carrier_img.x_max):
                for j in range(carrier_img.y_max):
                    r, g, b = carrier_load.getpixel((i, j))
                    dbytes = bit_data_encrypted_file.read(3)
                    r = bin(r)
                    g = bin(g)
                    b = bin(b)
                    # write in secret image bits
                    if len(dbytes) == 3:
                        r = str(r)[:-1] + dbytes[0]
                        g = str(g)[:-1] + dbytes[1]
                        b = str(b)[:-1] + dbytes[2]

                    stego_pixels[i, j] = (int(r, 2), int(g, 2), int(b, 2))

            stego_image.save(stego_img_name + carrier_img.frmt)

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
