class ImgEncryption:
    """
    Purpose:
        Provides capability to encrypt an image
    """
    _xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}

    @staticmethod
    def xor_encrypt(binary_filename, encrypted_filename, password):
        """
        Purpose:
            Encrypts secret img data file and stores in new encrypted file
        Args:
            binary_filename (str) - filename where unencrypted data is read from
            encrypted_filename (str) - filename where encrypted data is stored
            password (str) - password used to encrypt image with using XOR
        Returns:
            n/a
        """
        bit_data_file = open(binary_filename, "r")
        bit_data_encrypted_file = open(encrypted_filename, "w")
        xor_bit_len = len(password)
        xor_data = ""

        # skip XORing password
        bytes_read = bit_data_file.read(xor_bit_len)
        bit_data_encrypted_file.write(bytes_read)
        bytes_read = bit_data_file.read(xor_bit_len)

        while len(bytes_read) > 0:
            # last read XOR only necessary amount of password
            if len(bytes_read) < xor_bit_len:
                shrt_pass = password[0:len(bytes_read)]
                xor_data = ''.join([ImgEncryption._xormap[a, b] for a, b in zip(bytes_read, shrt_pass)])
            else:
                xor_data = ''.join([ImgEncryption._xormap[a, b] for a, b in zip(bytes_read, password)])

            # new password is XOR_data from previous password
            password = xor_data

            bit_data_encrypted_file.write(xor_data)
            bytes_read = bit_data_file.read(xor_bit_len)

        bit_data_file.close()
        bit_data_encrypted_file.close()

    @staticmethod
    def xor_decrypt(encrypted_filename, decrypted_filename, password):
        """
        Purpose:
            Decrypts secret img data file and stores in new encrypted file
        Args:
            encrypted_filename (str) - filename to read encrypted file
            decrypted_filename (str) - filename to write decrypted file to
            password (str) - password used to encrypt image with using XOR
        Returns:
            n/a
        """
        encrypted_data = open(encrypted_filename, "r")
        decrypted_data = open(decrypted_filename, "w")
        xor_bit_len = len(password)
        xor_data = ""

        # skip XORing password
        bytes_read = encrypted_data.read(xor_bit_len)
        decrypted_data.write(bytes_read)
        bytes_read = encrypted_data.read(xor_bit_len)

        while len(bytes_read) > 0:
            # last read XOR only necessary amount of password
            if len(bytes_read) < xor_bit_len:
                shrt_pass = password[0:len(bytes_read)]
                xor_data = ''.join([ImgEncryption._xormap[a, b] for a, b in zip(bytes_read, shrt_pass)])
            else:
                xor_data = ''.join([ImgEncryption._xormap[a, b] for a, b in zip(bytes_read, password)])

            # next password is bytes read
                password = bytes_read

            decrypted_data.write(xor_data)
            bytes_read = encrypted_data.read(xor_bit_len)

        encrypted_data.close()
        decrypted_data.close()
