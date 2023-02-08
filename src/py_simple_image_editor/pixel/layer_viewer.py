import tkinter as tk
from tkinter import ttk
import py_simple_ttk as sttk
from PIL import Image, ImageTk


class LayerViewer(ttk.LabelFrame):
    def __init__(self, project, width, height, *args, **kwargs):
        ttk.LabelFrame.__init__(self, *args, **kwargs)
        self.configure(text="LayerViewer")
        self.project = project
        self.width, self.height = width, height

        self.delay = 1000
        self.index = 0

        self.outer_frame = ttk.Frame(self)
        self.outer_frame.pack(fill="both", expand=True, padx=4, pady=4)
        self.outer_frame.config(width=220, height=200)
        self.inner_frame = ttk.Frame(self)
        sttk.force_aspect(
            self.inner_frame, self.outer_frame, float(width) / float(height)
        )

        self.canvas = tk.Canvas(self.inner_frame, relief="sunken")
        self.canvas.config(
            width=50, height=50, highlightthickness=0  # Parent frame width
        )
        self.canvas.config()
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.canvas_frame, anchor="nw")
        self.canvas_frame.config(width=50, height=50)
        self.canvas.pack(fill="both", expand=True)

        self.playback_scale = ttk.Scale(
            self, orient="horizontal", from_=1, to=60, command=self.set_delay
        )
        self.playback_scale.set(int(self.delay / 1000))
        self.playback_scale.pack(fill="both", expand=False, padx=4, pady=4)

        self.display_loop()

    def set_delay(self, fps):
        if float(fps) < float(1.0):
            self.delay = None
            return
        self.delay = int(1000.0 / float(fps))

    def display_loop(self):
        if not self.project.frames or not self.delay:
            self.after(100, self.display_loop)
            return
        if self.index > len(self.project.frames) - 1:
            self.index = 0
        layer = self.project.frames[self.index]
        self.image = layer.export_composite_image().resize(
            (self.inner_frame.winfo_width(), self.inner_frame.winfo_height()), Image.BOX
        )
        self.displayed = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.displayed, anchor="nw")
        self.configure(text=f"Preview: {layer.id}")
        self.index += 1
        if self.delay < 10:
            delay = 10
        delay = self.delay or 1000
        self.after(delay, self.display_loop)
