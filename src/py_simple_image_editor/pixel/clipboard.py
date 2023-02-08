import platform
import tkinter as tk
from tkinter import ttk
import py_simple_ttk as sttk
from PIL import Image, ImageTk

from .base_tile import BaseTile

trash_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\x0e\xfe\xe3\x10g\xc4%\x80K\x03!\xc0\xc8D\xa6F\xea\x01t?\x11\xeb\x15\xb8>\x8a\xbd0j\xc0\xa8\x01\x83\xc3\x00\x00\xf2\xb9\x03\x1c\xd6\xd7\xf8 \x00\x00\x00\x00IEND\xaeB`\x82"

Y_OFFSET = 10
Y_PADDING = 10
TILE_HEIGHT = 80
TILE_WIDTH = 80
TILE_X_OFFSET = 10


class ClipboardLayer:
    def __init__(self, id, image):
        self.id = id
        self.image = image
        self.width, self.height = self.image.size
        self.active = False

    def set_id(self, id):
        self.id = id


class ClipBoardClass:
    def __init__(self):
        self.layers = []
        self.selection = []
        self.selected_layer = None

    def set_id(self, id):
        self.id = id

    def copy_item(self, tkimage, name="Clip"):
        self.layers.append(l := ClipboardLayer(name, tkimage))
        self.selected_layer = l

    def del_layer(self, layer):
        self.layers.remove(layer)

    def select_layer(self, selection):
        self.selected_layer = self.layers[selection]

    def copy_layer(self, layer):
        (l := self.new_layer()).load_image(layer.image)
        l.set_id(f"Copy of {layer.id}")

    def get_layers(self):
        for layer in self.layers:
            yield layer

    def promote_layer(self, layer):
        if index := self.layers.index(layer):
            layer = self.layers.pop(index)
            self.layers.insert(index - 1, layer)

    def demote_layer(self, layer):
        if not (index := self.layers.index(layer)) == len(self.layers) - 1:
            layer = self.layers.pop(index)
            self.layers.insert(index + 1, layer)


class ClipBoardBox(ttk.Labelframe):
    def __init__(
        self,
        app,
        parent: ttk.Frame,
        *args,
    ):
        ttk.Labelframe.__init__(self, parent, *args, text="Clipboard")
        self.app = app

        self.thumbnails, self.tiles = [], []
        self.canvas_height = 0

        self.trash_image = sttk.load_tk_image_from_bytes_array(trash_bytes)

        self.canvas_frame = sttk.ScrolledCanvas(self)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = self.canvas_frame.canvas
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self.refresh, add="+")

        sttk.EasySizegrip(self)

    def on_click(self, event):
        y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
        x = event.x
        for t in self.tiles:
            if t.is_in_row(y):
                mode = t.on_click(x, y)
                if not mode:
                    self.app.tool_controller.clipboard.selected_layer = t.layer
                    t.layer.active = True
                    self.refresh()
            else:
                t.deactivate()

    def on_mouse_move(self, event):
        y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
        x = event.x
        for t in self.tiles:
            if t.active:
                if t.is_in_row(y):
                    continue
                else:
                    t.active = False
            elif t.is_in_row(y):
                t.active = True

    def refresh(self, event=None):
        self.winfo_toplevel().update_idletasks()
        self.canvas.delete("all")
        self.thumbnails = []
        self.tiles = []
        i = 0

        for c in self.app.tool_controller.clipboard.layers:
            y = i * (TILE_HEIGHT + Y_PADDING) + Y_OFFSET
            self.tiles.append(t := ClipTile(self, c))
            t.set_dimensions(TILE_X_OFFSET, y, TILE_WIDTH, TILE_HEIGHT)
            self.place_tile(t)
            if c is self.app.tool_controller.clipboard.selected_layer:
                self.select_tile(t)
            i += 1

        canvas_height = i * (TILE_HEIGHT + Y_PADDING) + Y_OFFSET
        frame_height = self.canvas_frame.winfo_height()
        self.canvas_height = (
            canvas_height if canvas_height > frame_height else frame_height
        )
        self.canvas_frame.config(width=200, height=self.canvas_height)
        self.canvas.config(scrollregion=(0, 0, 200, self.canvas_height))

    def place_tile(self, tile):
        tn = ImageTk.PhotoImage(tile.get_thumbnail(tile.height))
        scaling = self.winfo_toplevel().call("tk", "scaling")
        self.thumbnails.append(tn)
        tile.references.append(
            self.canvas.create_image(
                tile.x + 0.5 * tile.width, tile.y + 0.5 * tile.height, image=tn
            )
        )
        tile.references.append(
            self.canvas.create_rectangle(
                tile.x,
                tile.y,
                tile.x + tile.width,
                tile.y + tile.height,
                outline="#000000",
                width=1,
            )
        )
        tile.references.append(
            self.canvas.create_text(
                tile.x + tile.width + 10,
                tile.y,
                font="CourierNew 8",
                text=tile.id,
                anchor="nw",
            )
        )
        tile.references.append(
            self.canvas.create_text(
                tile.x + tile.width + 10,
                tile.y + 10 * scaling,
                font="CourierNew 8",
                text=f"Size: {tile.layer.width}px x {tile.layer.height}px",
                anchor="nw",
            )
        )

    def activate_tile(self, tile):
        tile.active_references.extend(
            [
                self.canvas.create_rectangle(
                    tile.x,
                    tile.y,
                    tile.x + tile.width,
                    tile.y + tile.height,
                    outline="#000000",
                    width=2,
                ),
                self.canvas.create_image(
                    tile.trash_x, tile.trash_y, anchor="nw", image=self.trash_image
                ),
            ]
        )

    def deactivate_tile(self, tile):
        self.canvas.create_rectangle(
            tile.x,
            tile.y,
            tile.x + tile.width,
            tile.y + tile.height,
            outline="#000000",
            width=1,
        )
        for r in tile.active_references:
            self.canvas.delete(r)

    def select_tile(self, tile):
        tile.references.append(
            self.canvas.create_rectangle(
                tile.x,
                tile.y,
                tile.x + tile.width,
                tile.y + tile.height,
                outline="#000000",
                width=3,
            )
        )

    def on_scroll_bar(self, move_type, move_units, __=None):
        if move_type == "moveto":
            self.canvas.yview("moveto", move_units)

    def delete_layer(self, layer):
        self.app.tool_controller.clipboard.del_layer(layer)
        self.app.tool_controller.clipboard.selected_layer = (
            self.app.tool_controller.clipboard.layers[0]
            if self.app.tool_controller.clipboard.layers
            else None
        )
        self.canvas.after_idle(self.refresh)


class ClipTile(BaseTile):
    def __init__(self, manager, cliplayer):
        BaseTile.__init__(self, manager)
        self.layer = cliplayer
        self.id = cliplayer.id
        self.thumbnail = None
        self.references = []
        self.active = cliplayer.active
        self.active_references = []

    def set_dimensions(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.trash_x, self.trash_y = self.x + self.width + 4, self.y + self.height - 16

    def get_thumbnail(self, size=50):
        self.thumbnail = self.layer.image.resize((70, 70), Image.BOX)
        return self.thumbnail

    def check_click_regions(self, pointer_x, pointer_y):
        def in_bounds(x, y, width, height):
            left_bound = x
            right_bound = x + width
            top_bound = y
            bottom_bound = y + height
            if pointer_x > left_bound and pointer_x < right_bound:
                if pointer_y > top_bound and pointer_y < bottom_bound:
                    return True

        def is_in_trash():
            return in_bounds(self.trash_x, self.trash_y, 16, 16)

        if is_in_trash():
            self.manager.delete_layer(self.layer)
            return True
