import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
from tkinter import ttk
import py_simple_ttk as sttk
from PIL import Image, ImageTk


WIDTH = 600
HEIGHT = 500

# Constants, need to move to enum
# #Color options constants
BLACKANDWHITE = 0
GRAYSCALE = 1
RGBA = 2
COLOR_OPTIONS = {BLACKANDWHITE: "Black and White", GRAYSCALE: "Grayscale", RGBA: "RGBA"}


# # Sizing options constants
SCALAR = 0
PIXELS = 1
SIZING_OPTIONS = {SCALAR: "Scale output", PIXELS: "Custom"}

# # Sizing options constants
LOOP = 0
NO_LOOP = 1
LOOP_OPTIONS = {LOOP: "Loop Gif", NO_LOOP: "Don't Loop Gif"}


class selection_box(ttk.LabelFrame):
    def __init__(self, label_text, selection_list, command, *args, **kwargs):
        ttk.LabelFrame.__init__(self, *args, **kwargs)
        self.inner_frame = ttk.Frame(self)
        self.inner_frame.pack(fill="both", expand=True, side="left")
        self.configure(text=label_text)
        self.var = tk.IntVar()
        for text, value in selection_list:
            b = ttk.Radiobutton(
                self.inner_frame,
                text=text,
                variable=self.var,
                value=value,
                command=command,
            )
            b.pack(anchor="w", fill="y", expand=False, side="left", padx=(0, 10))
        # select first option
        self.var.set(selection_list[0][1])

    def get(self):
        return self.var.get()


# class SaveMenu(tk.Toplevel):
#     def __init__(self, parent: tk.Tk, image_data, gif: bool = False):
#         tk.Toplevel.__init__(self, parent)
class SaveMenu(sttk.FocusedToplevel):
    def __init__(self, parent: tk.Tk, image_data, gif: bool = False):
        sttk.FocusedToplevel.__init__(self, window=parent, title="Save Image")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        # self.set_exit_function()
        self.title("Export")
        self.resizable(False, False)
        self.image_data = image_data
        self.gif = gif

        sizing_and_color_frame = ttk.Frame(self.frame)
        sizing_and_color_frame.pack(expand=True, fill="both")
        sizing_options = [
            (SIZING_OPTIONS[SCALAR], SCALAR),
            (SIZING_OPTIONS[PIXELS], PIXELS),
        ]

        # --------------------------------------------
        # Color
        color_options = [
            (COLOR_OPTIONS[RGBA], RGBA),
            (COLOR_OPTIONS[GRAYSCALE], GRAYSCALE),
            (COLOR_OPTIONS[BLACKANDWHITE], BLACKANDWHITE),
        ]
        self.color_selection = selection_box(
            "COLOR", color_options, self.on_color_select, sizing_and_color_frame
        )
        self.color_selection.pack(fill="x", padx=4)

        # -------------------------------------------------
        # Size

        size_selection_and_size_option_frame = ttk.Frame(sizing_and_color_frame)
        size_selection_and_size_option_frame.pack(fill="both", expand=True, padx=4)
        self.size_selection = selection_box(
            "SIZE",
            sizing_options,
            self.on_size_select,
            size_selection_and_size_option_frame,
        )
        self.size_selection.pack(side="left", fill="y")

        selection_frame_frame = ttk.LabelFrame(
            size_selection_and_size_option_frame, text="SIZE CONFIG"
        )
        selection_frame_frame.pack(fill="both", expand=True, side="left")

        self.scaling_frame = ttk.Frame(selection_frame_frame)
        self.scaling_frame.place(relwidth=1, relheight=1)
        self.scaling_factor = sttk.LabeledIntEntry(
            self.scaling_frame, labeltext="Scaling Factor - ", default=1
        )
        self.scaling_factor.label.configure(style="Normal.TLabel")
        self.scaling_factor.pack(fill="x")

        self.custom_dimensions_frame = ttk.Frame(selection_frame_frame)
        self.custom_dimensions_frame.place(relwidth=1, relheight=1)
        self.dimension_x_entry = sttk.LabeledEntry(
            self.custom_dimensions_frame, labeltext="Width (px)- ", default="16"
        )
        self.dimension_x_entry.label.configure(style="Normal.TLabel")
        self.dimension_x_entry.pack(fill="x", anchor="w")
        self.dimension_y_entry = sttk.LabeledEntry(
            self.custom_dimensions_frame, labeltext="Height (px)- ", default="16"
        )
        self.dimension_y_entry.label.configure(style="Normal.TLabel")
        self.dimension_y_entry.pack(fill="x", anchor="w")
        self.on_size_select()

        # Gif Stuff--------------------------------------------
        if self.gif:
            gif_option_frame = ttk.Frame(sizing_and_color_frame)
            gif_option_frame.pack(fill="both", expand=True, padx=4)
            loop_options = [
                (LOOP_OPTIONS[LOOP], LOOP),
                (LOOP_OPTIONS[NO_LOOP], NO_LOOP),
            ]
            self.loop_selection = selection_box(
                "LOOP OPTIONS", loop_options, self.on_loop_select, gif_option_frame
            )
            self.loop_selection.pack(side="left", fill="y")

            loop_frame = ttk.LabelFrame(gif_option_frame, text="LOOP CONFIG")
            loop_frame.pack(fill="both", expand=True, side="left")
            self.number_of_loops_frame = ttk.Frame(loop_frame)
            self.number_of_loops_frame.place(relwidth=1, relheight=1)
            self.number_of_loops = sttk.LabeledIntEntry(
                self.number_of_loops_frame,
                labeltext="Loops:",
            )
            self.number_of_loops.label.configure(style="Normal.TLabel")
            self.number_of_loops.pack(fill="x")

            ttk.Label(
                self.number_of_loops_frame, text="(Leave blank for infinite loop)"
            ).pack(fill="x", anchor="n")

            self.no_loop_frame = ttk.Frame(loop_frame)
            self.no_loop_frame.place(relwidth=1, relheight=1)
            ttk.Label(self.no_loop_frame, text="Don't loop gif.").place(
                relwidth=1, relheight=1
            )

            self.on_loop_select()

        if self.gif:
            duration_frame = ttk.LabelFrame(sizing_and_color_frame, text="GIF PLAYBACK")
            duration_frame.pack(fill="x", padx=2)
            self.duration_entry = sttk.LabeledEntry(
                duration_frame,
                labeltext="Frame Duration in Milliseconds",
                default=100,
            )
            self.duration_entry.pack(fill="both", padx=2)
            self.duration_entry.label.configure(style="Normal.TLabel")

        footer = ttk.LabelFrame(self.frame, text="FILE")

        select_path_frame = ttk.Frame(footer)
        select_path_frame.pack(fill="both", expand=True)
        self.file_path_entry = sttk.LabeledEntry(
            select_path_frame, labeltext="File path", default=""
        )
        self.file_path_entry.pack(fill="x", side="left", expand=True, padx=(2, 2))
        self.file_path_entry.label.configure(style="Normal.TLabel")
        select_path_button = ttk.Button(
            select_path_frame, command=self.set_save_path, text="Select file"
        ).pack(side="right", pady=(4, 6), padx=(2, 2), expand=False)

        ttk.Button(
            footer, text="Save", command=self.save_gif if self.gif else self.save
        ).pack(fill="x", expand=False, padx=4, pady=4)

        footer.pack(fill="x", expand=False, padx=4, pady=4)

        self.update_idletasks()
        self.after_idle(lambda: sttk.center_window(parent.winfo_toplevel(), self))

    def set_save_path(self):
        if self.gif:
            save_as = tkfiledialog.asksaveasfilename(
                defaultextension=".*", filetypes=[("GIF files", ".gif")]
            )
        else:
            save_as = tkfiledialog.asksaveasfilename(
                defaultextension=".*",
                filetypes=[
                    ("All files", ".*"),
                    ("PNG files", ".png"),
                    ("JPEG files", ".jpg .jpeg"),
                    ("BMP files", ".bmp"),
                    ("ICO files", ".ico"),
                ],
            )
        self.file_path_entry.set(save_as)

    def on_size_select(self):
        {
            SCALAR: self.scaling_frame.tkraise,
            PIXELS: self.custom_dimensions_frame.tkraise,
        }[self.size_selection.get()]()

    def on_loop_select(self):
        {
            LOOP: self.number_of_loops_frame.tkraise,
            NO_LOOP: self.no_loop_frame.tkraise,
        }[self.loop_selection.get()]()

    def on_color_select(self):
        # In case I want to add custom color options later
        pass

    def save(self):
        print("Beginning image conversion")
        image_data = (
            self.image_data
        )  # Make a copy of the image data for manipulation in case save fails and needs to bre redone

        def handle_scalar(image):
            print("Appling scalar resize to image")
            try:
                factor = self.scaling_factor.get()
                print(f"Resizing image by factor {factor}")
            except Exception as e:
                self.error(f"Invalid scaling factor: {e}")
                return
            if not factor:
                self.error(f"Scaling factor cannot be zero")
                return

            if factor == 1:
                return image
            else:
                return image.resize(
                    (int(image.height) * int(factor), int(image.width) * int(factor)),
                    Image.BOX,
                )

        def handle_pixels(image):
            try:
                width = self.dimension_x_entry.get()
                height = self.dimension_y_entry.get()
                print(f"Resizing image to {width} x {height}")
            except Exception as e:
                self.error(f"Invalid pixel resize values {e}")
                return

            try:
                return image.resize((int(height), int(width)), Image.BOX)
            except Exception as e:
                self.error(f"Error resizing image - {e}")
                return

        def handle_RGBA(image):
            print(f"ALREADY RGBA")
            return image

        sizing_options = {SCALAR: handle_scalar, PIXELS: handle_pixels}
        sizing_mode = self.size_selection.get()
        image_data = sizing_options[sizing_mode](image_data)
        if not image_data:
            return

        color_options = {
            RGBA: handle_RGBA,
            GRAYSCALE: sttk.convert_image_to_grayscale,
            BLACKANDWHITE: sttk.convert_image_to_blackandwhite,
        }
        color_mode = self.color_selection.get()
        try:
            mode = color_options[color_mode]
            if not mode:
                self.error("Unable to determine color mode")
                return
        except Exception as e:
            self.error(f"Error determining color mode: {e}")
            return
        try:
            image_data = mode(image_data)
            if not image_data:
                self.error("Invalid data after applying color mode")
                return
        except Exception as e:
            self.error(f"Error applying color mode: {e}")
            return

        try:
            filename = self.file_path_entry.get()
        except Exception as e:
            self.error(f"Error getting file name: {e}")
            return
        if not filename:
            self.error(f"No filename specified")
            return

        try:
            print("Saving...")
            image_data.save(filename)
        except Exception as e:
            self.error(f"Error saving image: {e}")
            return

        self.destroy()  # Sucessful!

    def save_gif(self):
        print("Beginning image conversion")

        def handle_scalar(image):
            print("Appling scalar resize to image")
            try:
                factor = self.scaling_factor.get()
                print(f"Resizing image by factor {factor}")
            except Exception as e:
                self.error(f"Invalid scaling factor: {e}")
                return
            if not factor:
                self.error(f"Scaling factor cannot be zero")
                return

            if factor == 1:
                return image
            else:
                return image.resize(
                    (int(image.height) * int(factor), int(image.width) * int(factor)),
                    Image.BOX,
                )

        def handle_pixels(image):
            try:
                width = self.dimension_x_entry.get()
                height = self.dimension_y_entry.get()
                print(f"Resizing image to {width} x {height}")
            except Exception as e:
                self.error(f"Invalid pixel resize values {e}")
                return

            try:
                return image.resize((int(height), int(width)), Image.BOX)
            except Exception as e:
                self.error(f"Error resizing image - {e}")
                return

        def handle_RGBA(image):
            print(f"ALREADY RGBA")
            return image

        sizing_options = {SCALAR: handle_scalar, PIXELS: handle_pixels}
        sizing_mode = self.size_selection.get()

        images = []

        try:
            for i in self.image_data:
                images.append(sizing_options[sizing_mode](i))
        except Exception as e:
            self.error(f"Error resizing images: {e}")
            return
        for i in images:
            if not i:
                self.error(f"Invalid image data after applying resize")
                return

        color_options = {
            RGBA: handle_RGBA,
            GRAYSCALE: sttk.convert_image_to_grayscale,
            BLACKANDWHITE: sttk.convert_image_to_blackandwhite,
        }
        color_mode = self.color_selection.get()
        try:
            mode = color_options[color_mode]
            if not mode:
                self.error("Unable to determine color mode")
                return
        except Exception as e:
            self.error(f"Error determining color mode: {e}")
            return
        try:
            images = [mode(i) for i in images]
            for i in images:
                if not i:
                    self.error("Invalid data after applying color mode")
                    return
        except Exception as e:
            self.error(f"Error applying color mode: {e}")
            return

        try:
            filename = self.file_path_entry.get()
        except Exception as e:
            self.error(f"Error getting file name: {e}")
            return
        if not filename:
            self.error(f"No filename specified")
            return

        duration = 100

        def handle_loop():
            if self.number_of_loops.get():
                return int(self.number_of_loops.get())
            else:
                return 0

        def handle_no_loop():
            return 1

        loop_options = {
            LOOP: handle_loop,
            NO_LOOP: handle_no_loop,
        }

        loop = loop_options[self.loop_selection.get()]()
        duration = int(self.duration_entry.get() or 0)
        if not duration and loop:
            self.error(
                f"Error - option to loop gif was selected but invalid duration provided."
            )
            return
        try:
            images[0].save(
                filename,
                format="GIF",
                save_all=True,
                append_images=images[1:],
                duration=int(duration),
                loop=int(loop),
                transparency=255,
                optimize=False,
                disposal=2,
            )
        except Exception as e:
            self.error(f"Error saving image: {e}")
            return

        self.destroy()  # Sucessful!

    def error(self, error):
        tkmessagebox.showwarning("Error", error)
