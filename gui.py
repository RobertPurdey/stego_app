from tkinter import *
from tkinter import filedialog
from img_holder import *
from PIL import Image
from PIL import ImageTk
from img_processing import StegoProcessor

class StegoGui(Frame):
    """
        Stegonagraphy GUI.
    """

    def __init__(self, master):
        """
        Purpose:
            Setup GUI
        Args:

        """
        # Super call
        Frame.__init__(self, master)

        # ************************************************************* Instance Variables

        # ****************************************************** Toolbars
        # Contains image selection
        self.tlbr_img_selection = Frame(master, bg="purple")

        # Contains password selection
        self.tlbr_pass_selection = Frame(master, bg="green")

        # Contains image conversion selection
        self.tlbr_convert_selection = Frame(master, bg="red")

        # Contains encryption type election
        self.tlbr_encrypt_selection = Frame(master, bg="yellow")

        # ****************************************************** Buttons
        # Allows selection for the secret image
        self.bttn_select_secret = Button(self.tlbr_img_selection, text="Secret", command=self.select_secret_img)

        # Allows selection for the carrier image
        self.bttn_select_carrier = Button(self.tlbr_img_selection, text="Carrier", command=self.select_carrier_img)

        # Hides secret image inside carrier image
        self.bttn_hide = Button(self.tlbr_convert_selection, text="Hide", command=self.encode_img)

        # Extracts hidden image from stego image
        self.bttn_extract = Button(self.tlbr_convert_selection, text="Extract", command=self.decode_img)

        # ****************************************************** Labels
        # Image selection label
        self.lbl_img_selection = Label(self.tlbr_img_selection, text="Select Image: ")

        # Password choice label
        self.lbl_pass_selection = Label(self.tlbr_pass_selection, text="Select Password: ")

        # Conversion type label
        self.lbl_conversion_selection = Label(self.tlbr_convert_selection, text="Select Conversion: ")

        # Encryption type label
        self.lbl_encryption_selection = Label(self.tlbr_encrypt_selection, text="Select Encryption: ")

        # ****************************************************** Text boxes
        # Password entry
        self.txtb_pass = Entry(self.tlbr_pass_selection)

        # todo: robert add radio buttons for encryption type

        # ****************************************************** File holder
        # Secret image to hide
        self.img_secret_hldr = StegoImgHolder

        # Image that will carry the secret image (only init with default holder -- must setup holder)
        self.img_carrier_hldr = StegoImgHolder

        # Carrier image that now contains the secret image (only init with default holder -- must setup holder)
        self.img_stego = StegoImgHolder
        # ************************************************ End of Instance Variables

        # ****************************************************** Sub windows
        # window to show the secret image when one is selected
        self.img_secret_display = ""

        # window to show the carrier image when one is selected
        self.img_carrier_display = ""

        # window to show the secret image when one is selected
        self.img_stego_display = ""

        # Setup ui layouts
        self.layout_toolbars()

    def layout_toolbars(self):
        """
        Purpose:
            Layout toolbar orders
            -
            -
        Args:
            n/a
        Returns:
            n/a
        """
        self.layout_img_selection_toolbar()
        self.layout_password_selection_toolbar()
        self.layout_conversion_selection_toolbar()

    def layout_img_selection_toolbar(self):
        """
        Purpose:
            Layout image selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_img_selection.pack(side=LEFT, padx=2, pady=2)
        self.bttn_select_carrier.pack(side=LEFT, padx=2, pady=2)
        self.bttn_select_secret.pack(side=LEFT, padx=2, pady=2)
        self.tlbr_img_selection.pack(side=TOP, fill=X)

    def layout_password_selection_toolbar(self):
        """
        Purpose:
            Layout password selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_pass_selection.pack(side=LEFT, padx=2, pady=2)
        self.txtb_pass.pack(side=LEFT, padx=2, pady=2)
        self.tlbr_pass_selection.pack(side=TOP, fill=X)

    def layout_conversion_selection_toolbar(self):
        """
        Purpose:
            Layout conversion selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_conversion_selection.pack(side=LEFT, padx=2, pady=2)
        self.bttn_hide.pack(side=LEFT, padx=2, pady=2)
        self.bttn_extract.pack(side=LEFT, padx=2, pady=2)
        self.tlbr_convert_selection.pack(side=TOP, fill=X)

    def select_secret_img(self):
        """
        Purpose:
            Allows user to select the image to be hidden and shows user the img
        Args:
            n/a
        Returns:
            n/a
        """
        secret_img_loc = self.get_img_dialog()
        self.set_secret_img_holder(secret_img_loc)
        # test printing (use for test screenshots)
        print("Secret Image selected: " + secret_img_loc)
        print("-- Format:   " + self.img_secret_hldr.frmt)
        print("-- Path:     " + self.img_secret_hldr.path)
        print("-- Filename: " + self.img_secret_hldr.filename)
        print("-- Fullpath: " + self.img_secret_hldr.fullpath)

        self.open_secret_img_display_window()

    def open_secret_img_display_window(self):
        """
        Purpose:
            Opens secret image window display with chosen image
        Args:
            n/a
        Returns:
            n/a
        """
        # todo: move common code into "open_img_display_window"
        # todo: how to unset window / image selection when X is clicked by user??
        self.img_secret_display = Toplevel(self.master)
        self.img_secret_display.title("Secret Image")

        img_load = Image.open(self.img_secret_hldr.fullpath)
        img_render = ImageTk.PhotoImage(img_load)
        img = Label(self.img_secret_display, image=img_render)
        img.image = img_render
        img.place(x=0, y=0)
        img.pack()

    def open_carrier_img_display_window(self):
        """
        Purpose:
            Opens secret image window display with chosen image
        Args:
            n/a
        Returns:
            n/a
        """
        # todo: move common code into "open_img_display_window"
        # todo: how to unset window / image selection when X is clicked by user??
        self.img_carrier_display = Toplevel(self.master)
        self.img_carrier_display.title("Carrier Image")

        img_load = Image.open(self.img_carrier_hldr.fullpath)
        img_render = ImageTk.PhotoImage(img_load)
        img = Label(self.img_carrier_display, image=img_render)
        img.image = img_render
        img.place(x=0, y=0)
        img.pack()

    def open_img_display_window(self, fullpath, img_display):
        """
        Purpose:
            Opens image window display with chosen image
        Args:
            n/a
        Returns:
            n/a
        """

    def select_carrier_img(self):
        """
        Purpose:
            Allows user to select the image to carry the secret image and shows user the img
        Args:
            n/a
        Returns:
            str - carrier
        """
        carrier_img_loc = self.get_img_dialog()
        self.set_carrier_img_holder(carrier_img_loc)
        # test printing (use for test screenshots)
        print("Carrier Image selected: " + carrier_img_loc)
        print("-- Format: " + self.img_carrier_hldr.frmt)
        print("-- Path:   " + self.img_carrier_hldr.path)
        print("-- Filename: " + self.img_carrier_hldr.filename)
        print("-- Fullpath: " + self.img_carrier_hldr.fullpath)

        self.open_carrier_img_display_window()

    def get_img_dialog(self):
        """
        Purpose:
            Gets image location the user selected of an acceptable format (BMP, PNG, JPG)
        Args:
            n/a
        Returns:
            str - image location of the selected file
        """
        filename = filedialog.askopenfilename(filetypes=[("Bitmap (*.bmp)", "*.bmp")])

        return filename

    def set_secret_img_holder(self, secret_img_loc):
        """
        Purpose:
            sets up the secret image holder with the following:
            - image type
            - image format
            - image file path
            - image size
        Args:
            n/a
        Returns:
            n/a
        """
        self.img_secret_hldr = SecretStegoImgHolder(image_loc=secret_img_loc)

    def set_carrier_img_holder(self, secret_img_loc):
        """
        Purpose:
            sets up the carrier image holder with the following:
            - image type
            - image format
            - image file path
            - image size
        Args:
            n/a
        Returns:
            n/a
        """
        self.img_carrier_hldr = CarrierStegoImgHolder(image_loc=secret_img_loc)

    def decode_img(self):
        """
        Purpose:
            Validates and decodes image if valid
        """
        StegoProcessor.extract_img(self.img_carrier_hldr, self.img_secret_hldr, "")

    def encode_img(self):
        """
        Purpose:
            Validates and hides image if valid
        """
        StegoProcessor.hide_img(self.img_carrier_hldr, self.img_secret_hldr, self.img_carrier_hldr, "test", "fake_filename.bmp")

