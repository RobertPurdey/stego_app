from enum import Enum
import os

class ImageType(Enum):
    """
    Purpose:
        Possible image types

    Types:
        SECRET = 1: The image is to be hidden
        CARRIER = 2: The image is to have an image hidden in it
    """
    SECRET = 1
    CARRIER = 2


class StegoImgHolder:
    """
    Purpose:
        Abstract class
        Holds an image being used by the stego tool
    """

    def __init__(self, img_type):
        """
        Purpose:
            Empty CTOR. If used, make sure to call setup function before using any functionality of this class
        """
        # todo: maybe get rid of this ctor?
        self.img_type = img_type
        self.frmt = ""
        self.path = ""
        self.filename = ""
        self.fullpath = ""
        self.size = 0
        self.x_max = 0
        self.y_max = 0

    def __init__(self, img_type, img_loc):
        """
        Purpose:
            Sets up initial instance variables

        Args:
            img_type (ImageType): type of image being held
            img_loc (str): Location of the img being held (strip for img type /
        """
        self.img_type = img_type
        self.frmt = ""
        self.path = ""
        self.filename = ""
        self.fullpath = ""
        self.size = 0
        self.x_max = 0
        self.y_max = 0

        self.set_path_and_format(img_loc)

    def get_pixel_count(self):
        return self.x_max * self.y_max

    def set_path_and_format(self, img_loc):
        """
        Purpose:
            Sets up initial instance variables:
            - img_path
            - img_frmt
            - img_filename

        Args:
            img_loc (str): Location of the img being held (strip for img path)
        """
        # todo: make this find backslash on linux and forward slash on windows
        filename_index_begin = img_loc.rfind('/')
        ext_index_begin = img_loc.rfind('.')

        self.path = img_loc[0:ext_index_begin]
        self.frmt = img_loc[ext_index_begin:len(img_loc)]
        self.filename = img_loc[filename_index_begin + 1:ext_index_begin]
        self.fullpath = self.path + self.frmt
        self.size = os.path.getsize(self.fullpath)


class SecretStegoImgHolder(StegoImgHolder):
    """
    Purpose:
        Holds a secret image being used by the stego tool
    """
    def __init__(self, image_loc):
        # Super call (handles image format and file path
        StegoImgHolder.__init__(self, ImageType.SECRET, image_loc)


class CarrierStegoImgHolder(StegoImgHolder):
    """
    Purpose:
        Holds a carrier image being used by the stego tool
    """
    def __init__(self, image_loc):
        # Super call (handles image format and file path
        StegoImgHolder.__init__(self, ImageType.CARRIER, image_loc)
