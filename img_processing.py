from PIL import Image
from img_encryption import ImgEncryption
import os


class StegoProcessor:
    """
    Purpose:
        Provides capability to hide or extract an image
    """

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
        # ------------- Extract encrypted data from stego image
        stego_load = Image.open(stego_img.fullpath)
        stego_img.x_max = stego_load.size[0]
        stego_img.y_max = stego_load.size[1]
        # encrypted data
        encrypted_data = open("encrypted_data_extract", "w")

        # read encrypted data into a file
        for i in range(stego_img.x_max):
            for j in range(stego_img.y_max):
                r, g, b = stego_load.getpixel((i, j))
                r = bin(r)[-1]
                g = bin(g)[-1]
                b = bin(b)[-1]
                data = str(r) + str(g) + str(b)

                encrypted_data.write(data)

        encrypted_data.close()

        # ------------- Decrypt XOR bit string data
        temp_pass = ''.join([bin(ord(ch))[2:].zfill(8) for ch in password]).zfill(144)  # read 144 bits
        ImgEncryption.xor_decrypt("encrypted_data_extract", "decrypted_data_extract", temp_pass)

        # ------------- Start reading extracting and reading decrypted data
        decrypted_data = open("decrypted_data_extract", "r")

        # read password
        bin_password = decrypted_data.read(144)
        password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in password]).zfill(144)

        # FAILED password return early
        if password != bin_password:
            decrypted_data.close()
            return ""

        # read filename len
        bin_filename_len = decrypted_data.read(5)
        filename_len = int(bin_filename_len, 2)

        # read in filename
        bin_filename = decrypted_data.read(filename_len*8)
        filename = ''.join(chr(int(bin_filename[i:i + 8], 2)) for i in range(0, len(bin_filename), 8))

        # read in file format
        bin_file_frmt = decrypted_data.read(32)
        file_frmt = ''.join(chr(int(bin_file_frmt[i:i + 8], 2)) for i in range(0, len(bin_file_frmt), 8))

        # read image width
        bin_img_width = decrypted_data.read(16)
        img_width = int(bin_img_width, 2)

        # read image height
        bin_img_height = decrypted_data.read(16)
        img_height = int(bin_img_height, 2)

        # Save decrypted image
        # Image to store extracted img
        secret_found = Image.new("RGB", (img_width, img_height))
        secret_load = secret_found.load()

        # create image from extracted img data
        for i in range(img_width):
            for j in range(img_height):
                # read rgb byte string (8 bytes per pixel)
                read_rgb = decrypted_data.read(24)
                r = int(read_rgb[0:8], 2)
                g = int(read_rgb[8:16], 2)
                b = int(read_rgb[16:24], 2)

                secret_load[i, j] = (r, g, b)

        secret_found.save(filename + file_frmt)
        decrypted_data.close()

        # Delete data binary files (were only temporary and don't want traces of them)
        os.remove("encrypted_data_extract")
        os.remove("decrypted_data_extract")

        return filename

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
            0  - if hide failed because of invalid size
            1  - if hide passed
        """
        # Load carrier / secret image (PIL Image) and set y/x max into image holders
        carrier_load = Image.open(carrier_img.fullpath)
        carrier_img.x_max = carrier_load.size[0]
        carrier_img.y_max = carrier_load.size[1]

        secret_load = Image.open(secret_img.fullpath)
        secret_img.x_max = secret_load.size[0]
        secret_img.y_max = secret_load.size[1]

        # Error handling return early
        if StegoProcessor.validate_stego_hide(carrier_img, secret_img) == 0:
            return 0
        # end of error handling

        # ----------- convert ascii to binary for storage data
        # - (password (144 bits)
        # - filename length (5 bits)
        # - filename
        # - image width (16 bits)
        # - image height (16 bits)
        # - image bit data string length (32 bits)
        # - image data bit string length (32 bits)
        bin_password = ''.join([bin(ord(ch))[2:].zfill(8) for ch in password]).zfill(144)  # read 144 bits
        bin_filename_len = ''.join([bin(len(new_filename))[2:]]).zfill(5)  # read 5 bits
        bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in new_filename])  # read filename_len bits
        bin_file_fmt = ''.join([bin(ord(ch))[2:].zfill(8) for ch in secret_img.frmt])  # read 32 bits
        bin_img_width = bin(secret_img.x_max)[2:].zfill(16)  # read 16 bits
        bin_img_height = bin(secret_img.y_max)[2:].zfill(16)  # read 16 bits

        bin_hdr = bin_password + \
            bin_filename_len + \
            bin_filename + \
            bin_file_fmt + \
            bin_img_width + \
            bin_img_height

        # write entire header into file
        bit_data_file = open("decrypted_data_extract", "w")
        bit_data_file.write(bin_hdr)

        for i in range(secret_img.x_max):
            for j in range(secret_img.y_max):
                r, g, b = secret_load.getpixel((i, j))
                br = bin(r)[2:].zfill(8)
                bg = bin(g)[2:].zfill(8)
                bb = bin(b)[2:].zfill(8)
                b_data = br + bg + bb

                bit_data_file.write(b_data)

        bit_data_file.close()

        # ---------------- Encrypt XOR bit string data to hide
        ImgEncryption.xor_encrypt("decrypted_data_extract", "encrypted_data_extract", bin_password)

        # ---------------- Start reading data into image carrier
        bit_data_encrypted_file = open("encrypted_data_extract", "r")

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
        bit_data_encrypted_file.close()

        # Delete data binary files (were only temporary and don't want traces of them)
        os.remove("decrypted_data_extract")
        os.remove("encrypted_data_extract")

        return 1

    @staticmethod
    def validate_stego_hide(carrier_img, secret_img):
        """
        Purpose:
            Validates secret image can be hidden in the carriers image:
                - carrier img size can hold secret (img bits + img header bits)
        Args:
            carrier_img (Image) - image to carrying the secret image
            secret_img (Image) - image to hide in carrier image
            err_msg (str) - message to store any errors in
        Returns:
            0 - if invalid size
            1 - if valid for stego hide processing
        """
        is_valid = 0
        carrier_holder_bits = carrier_img.get_pixel_count() * 3 / 8

        # Max space required for image header
        img_header_max = 485 / 8
        secret_bits_to_hide = (secret_img.get_pixel_count() * 3) + img_header_max

        if carrier_holder_bits < secret_bits_to_hide:
            is_valid = 0
        else:
            # All validation passed
            is_valid = 1

        return is_valid

