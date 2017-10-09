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
        self.tlbr_img_selection = Frame(master, bg="gray")

        # Contains password selection
        self.tlbr_pass_selection = Frame(master, bg="gray")

        # Contains new image filename
        self.tlbr_new_filename_selection = Frame(master, bg="gray")

        # Contains stego image filename
        self.tlbr_stego_filename_selection = Frame(master, bg="gray")

        # Contains image conversion selection
        self.tlbr_convert_selection = Frame(master, bg="gray")

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
        self.lbl_img_selection = Label(self.tlbr_img_selection, text="Select Image:")

        # Password choice label
        self.lbl_pass_selection = Label(self.tlbr_pass_selection, text="Select Password:")

        # Conversion type label
        self.lbl_conversion_selection = Label(self.tlbr_convert_selection, text="Select Conversion:")

        # New image name label
        self.lbl_new_image_selection = Label(self.tlbr_new_filename_selection, text="Extracted Image Name:")

        # Stego image name label
        self.lbl_stego_image_selection = Label(self.tlbr_stego_filename_selection, text="Stego Image Name:")

        # ****************************************************** Text boxes
        # Password entry
        self.txtb_pass = Text(self.tlbr_pass_selection, height=1, width=35)

        # New image filename entry
        self.txtb_new_img_filename = Text(self.tlbr_new_filename_selection, height=1, width=35)

        # Stego image filename entry
        self.txtb_stego_img_filename = Text(self.tlbr_stego_filename_selection, height=1, width=35)

        # ****************************************************** File holder
        # Secret image to hide
        self.img_secret_hldr = None

        # Image that will carry the secret image (only init with default holder -- must setup holder)
        self.img_carrier_hldr = None

        # Carrier image that now contains the secret image (only init with default holder -- must setup holder)
        self.img_stego = None
        # ************************************************ End of Instance Variables

        # ****************************************************** Sub windows
        # window to show the secret image when one is selected
        self.img_secret_display = None

        # window to show the carrier image when one is selected
        self.img_carrier_display = None

        # window to show the secret image when one is selected
        self.img_stego_display = None

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
        self.layout_new_filename_selection_toolbar()
        self.layout_stego_filename_selection_toolbar()
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
        self.lbl_img_selection.pack(side=LEFT, padx=(55, 0), pady=2)
        self.bttn_select_carrier.pack(side=LEFT, padx=4, pady=2)
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
        self.lbl_pass_selection.pack(side=LEFT, padx=(37, 0), pady=2)
        self.txtb_pass.pack(side=LEFT, padx=4, pady=2)
        self.tlbr_pass_selection.pack(side=TOP, fill=X)

    def layout_new_filename_selection_toolbar(self):
        """
        Purpose:
            Layout password selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_new_image_selection.pack(side=LEFT, padx=2, pady=2)
        self.txtb_new_img_filename.pack(side=LEFT, padx=2, pady=2)
        self.tlbr_new_filename_selection.pack(side=TOP, fill=X)

    def layout_stego_filename_selection_toolbar(self):
        """
        Purpose:
            Layout password selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_stego_image_selection.pack(side=LEFT, padx=(20, 0), pady=2)
        self.txtb_stego_img_filename.pack(side=LEFT, padx=4, pady=2)
        self.tlbr_stego_filename_selection.pack(side=TOP, fill=X)

    def layout_conversion_selection_toolbar(self):
        """
        Purpose:
            Layout conversion selection toolbar
        Args:
            n/a
        Returns:
            n/a
        """
        self.lbl_conversion_selection.pack(side=LEFT, padx=(27, 0), pady=2)
        self.bttn_hide.pack(side=LEFT, padx=4, pady=2)
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

        if secret_img_loc != "":
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
        if self.img_secret_display is not None:
            self.img_secret_display.destroy()

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
        if self.img_carrier_display is not None:
            self.img_carrier_display.destroy()

        self.img_carrier_display = Toplevel(self.master)
        self.img_carrier_display.title("Carrier Image")

        img_load = Image.open(self.img_carrier_hldr.fullpath)
        img_render = ImageTk.PhotoImage(img_load)
        img = Label(self.img_carrier_display, image=img_render)
        img.image = img_render
        img.place(x=0, y=0)
        img.pack()

    def open_img_display_window(self, filename, window_title):
        """
        Purpose:
            Opens stegonagraphy image result and closes secret image
        Args:
            n/a
        Returns:
            n/a
        """
        if self.img_secret_display is not None:
            self.img_secret_display.destroy()
        if self.img_stego_display is not None:
            self.img_stego_display.destroy()

        self.img_stego_display = Toplevel(self.master)
        self.img_stego_display.title(window_title)

        img_load = Image.open(filename + ".bmp")
        img_render = ImageTk.PhotoImage(img_load)
        img = Label(self.img_stego_display, image=img_render)
        img.image = img_render
        img.place(x=0, y=0)
        img.pack()

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

        if carrier_img_loc != "":
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
        password = self.txtb_pass.get("1.0", 'end-1c')

        if self.img_carrier_hldr is not None and password != "":
            # teardown
            new_filename = StegoProcessor.extract_img(self.img_carrier_hldr, password)
            if new_filename != "":
                self.img_secret_hldr = None
                self.img_carrier_hldr = None
                self.open_img_display_window(new_filename, "Extracted Image")
            else:
                print("Invalid password.")
        else:
            print("Carrier file and password must be set in order to extract image.")

    def encode_img(self):
        """
        Purpose:
            Validates and hides image if valid
        """
        password = self.txtb_pass.get("1.0", 'end-1c')
        new_filename = self.txtb_new_img_filename.get("1.0", 'end-1c')
        stego_filename = self.txtb_stego_img_filename.get("1.0", 'end-1c')
        hide_result = 2
        if self.img_carrier_hldr is not None and self.img_secret_hldr is not None and password != "" and new_filename != "" and stego_filename != "":
            hide_result = StegoProcessor.hide_img(self.img_carrier_hldr, self.img_secret_hldr, new_filename, stego_filename, password)
        else:
            print("Ensure carrier img, secret img, password, extracted image name and stego file name are set")

        if hide_result == 1:
            self.open_img_display_window(stego_filename, "Stegonagraphy Image")
            self.img_secret_hldr = None
            self.img_carrier_hldr = None
        elif hide_result == 0:
            print("Carrier image is too small to hold secret image + image header")




