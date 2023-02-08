import tkinter as tk
import tkinter.messagebox as tkmessagebox
import tkinter.colorchooser as tkcolorchooser
from tkinter import ttk
import py_simple_ttk as sttk

from .tool_box import ToolBox
from .pixel import PixelProject
from .pixel_canvas import PixelCanvas
from .clipboard import ClipBoardBox

DRAW = "draw"
EYEDROPPER = "eyedropper"


PALLETE_WIDTH = 16
PALLETE_HEIGHT = 9


class Pallete(ttk.Frame):
    def __init__(self, parent: ttk.Frame, app):
        ttk.Frame.__init__(self, parent)

        self.app = app
        self.alpha = 255
        # Set up project object to hold selected colors
        self.project = PixelProject(PALLETE_WIDTH, PALLETE_HEIGHT)
        self.layer = self.project.selected_frame.selected_layer
        self.layer.selection = [f"{PALLETE_WIDTH - 1}x{PALLETE_HEIGHT - 1}"]

        (scale_box := ttk.Frame(self)).pack(anchor="n", fill="x")
        self.scale_label_var = tk.StringVar(value=self.app.tool_controller.get_color())
        (color_label := ttk.Label(scale_box, textvariable=self.scale_label_var)).pack(
            anchor="n"
        )
        self.alpha_scale = ttk.Scale(
            scale_box,
            orient="horizontal",
            from_=0,
            to=255,
            length=300,
            value=self.alpha,
        )
        self.alpha_scale.pack(side="bottom")

        self.canvas = PixelCanvas(self, self.project)
        self.canvas.pack(anchor="n", expand=True, fill="both")

        for cell, color in zip(
            self.canvas.itterate_canvas(),
            (
                *sttk.get_gradient(PALLETE_WIDTH),
                *sttk.get_rainbow(PALLETE_WIDTH * (PALLETE_HEIGHT - 1)),
            ),
        ):
            self.layer.set_pixel_color(cell, sttk.hex_to_rgba(color))

        self.app.tool_controller.set_color(
            tuple(self.layer.array[PALLETE_HEIGHT - 1][PALLETE_WIDTH - 1])
        )


class ToolColumn(ttk.Frame):
    def __init__(self, app, parent: ttk.Frame):
        ttk.Frame.__init__(self, parent)
        self.app = app
        (
            panes := tk.PanedWindow(
                self, orient="vertical", sashpad=3, sashrelief="sunken", borderwidth=0
            )
        ).pack(fill="both", expand=True, padx=4, pady=(0, 4))

        self.pallete = Pallete(panes, app)
        self.pallete.canvas.canvas.bind("<Button-1>", self.select_color)
        self.pallete.canvas.canvas.bind("<Double-Button-1>", self.change_color)
        self.pallete.alpha_scale.configure(command=self.set_alpha)
        panes.add(self.pallete)
        panes.paneconfigure(self.pallete, minsize=150)

        self.toolbox = ToolBox(panes, self.app.tool_controller)
        panes.add(self.toolbox)
        panes.paneconfigure(self.toolbox, minsize=150)

        self.clipboard_box = ClipBoardBox(self.app, self)
        self.clipboard_box.refresh()
        panes.add(self.clipboard_box)
        panes.paneconfigure(self.clipboard_box, minsize=150)

        self.update()

        self.bind("<Configure>", self.schedule_refresh)
        self.scheduled_refresh = None

    def schedule_refresh(self, event=None):
        if self.scheduled_refresh:
            self.after_cancel(self.scheduled_refresh)
        self.scheduled_refresh = self.after_idle(self.refresh)

    def refresh(self):
        self.scheduled_refresh = None
        self.clipboard_box.refresh()
        self.pallete.canvas.redraw()

    def select_color(self, event) -> None:
        if cell := self.pallete.canvas.get_cell_id(event.x, event.y):
            print(f"Selected id {cell}")
            x, y = (int(v) for v in cell.split("x"))
            self.pallete.layer.selection = [cell]
            self.app.tool_controller.set_color(self.pallete.layer.array[y][x])
            self.alpha = self.pallete.layer.array[y][x][3]
            self.pallete.alpha_scale.set(self.alpha)
            self.update()

    def change_color(self, event):
        if not (cell := self.pallete.canvas.get_cell_id(event.x, event.y)):
            return

        if not (color := tkcolorchooser.askcolor()[0]):
            return  # If no color was selected

        self.app.tool_controller.set_color((*color, self.alpha))
        self.pallete.layer.load_image(
            self.app.tool_controller.draw(self.pallete.layer, cell)
        )
        self.update()

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.app.tool_controller.set_color(
            [*self.app.tool_controller.get_color()[:3], alpha]
        )
        self.pallete.layer.load_image(
            self.app.tool_controller.draw(
                self.pallete.layer, self.pallete.layer.selection[0]
            )
        )
        self.update()

    def update(self):
        self.pallete.scale_label_var.set(self.app.tool_controller.get_color())
        self.pallete.canvas.redraw()
