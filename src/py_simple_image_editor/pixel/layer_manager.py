import platform
import tkinter as tk
import tkinter.simpledialog as tksimpledialog
import tkinter.messagebox as tkmessagebox
import tkinter.filedialog as tkfiledialog
from tkinter import ttk
import py_simple_ttk as sttk
from PIL import Image, ImageTk
from .base_tile import BaseTile

trash_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\x0e\xfe\xe3\x10g\xc4%\x80K\x03!\xc0\xc8D\xa6F\xea\x01t?\x11\xeb\x15\xb8>\x8a\xbd0j\xc0\xa8\x01\x83\xc3\x00\x00\xf2\xb9\x03\x1c\xd6\xd7\xf8 \x00\x00\x00\x00IEND\xaeB`\x82"
copy_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5\x93;\x0e\x00 \x08C\x8b\xf1\xfeW\xd6\t\x17\xc5V1\xb1#m^\x08\x1f\x03\xd0\xb0\x97\x11\x9f\x02\x98\xcf\x03,\xa3\x00\xc2\\=\x84z\xddVE\x050\xf9\x85\x04#\x99Cn\x01\x03\x92\x01 \xdb\xc1\x1b\x80\xafQ\xbd\x05Y\xf2q\xfd\x9fA\xf4\xaa\xf2L:6*\x12\x0b:\xd1\x01?\x00\x00\x00\x00IEND\xaeB`\x82"
copy_bytes_wide = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00_IDATx\x9c\xbd\x91A\x0e\x00!\x08\x03\x87\xcd\xfe\xff\xcb\xee\x89D\x8c\x05\xa3f{\x14R\xa7\xc5\x80\x86\x96%3\x00\x9eb\x9e\x99\x87%\xb5\x98\xcd\x96\x08<\x824y\x93\x9f\xd5[\xe8\xa5"(\xcd\x15\x81kv\x05\xef\xc5v\tB/;\x06A}\x84\xa5\x9b\x8f\xbaB\xa0\x8a\xfa\x87\xe0j\x893\x95Q\x8e\t>k\x92\x10\x1fW\xad\x10U\x00\x00\x00\x00IEND\xaeB`\x82'
new_from_image_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xbd\x90Q\n\x800\x0cC_\xc5\xfb_y\xfe8\xd1\x9a-s\xa8\x81\xc1(\xe9k\x9b\x00\n\xe3\nU,\x8d\x7f\xcfwh\x99\x00I@m\xc8+ZP\x05\xc4\xfe\x9e\xe4q\x01\xa8\xa9\xf9$\x19`6\xaa\xda\x19x\xf3\xaa\r2\xa89\x19`5[t\x9b\x190\xb8P\xc3\x9d\xf0\xaa\xa6B\xb4\xfa\xf5\x84o\xb4\x01\xb9\xd6\x17\x08\x7f~yJ\x00\x00\x00\x00IEND\xaeB`\x82"
up_arrow_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00JIDATx\x9cc`\xc0\x0f\xfeC1N\xc0D@366Q\x06`\xd3\x80\xd5\x10l\x06\xe0s2\x86\x1c\xba\x01x\xfd\x8bM\r\x13.\tb\raB\x17 \xd5\x10F25\xc3\x01#>\xd3\x89Q\x8f/\x1d\x10\x05F\r\x18\x0c\x06\x00\x00\x9f\xc8\x10\x0e\xae\xb1^D\x00\x00\x00\x00IEND\xaeB`\x82"
down_arrow_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00MIDATx\x9ccd\xc0\x0e\xfe\xe3\x10gD\x17`\xc2\xa1\x90h0j\xc0`0\x80\x91\x01w\x9c\x13\xed\x02\x8c\xc4A\x8a\x03`^ \xc7\x10F\x98\x0bP\x04H\xd1\x8cn\x00\xb1\x86\xa0\xa8\xc1\x16\x0b\xf8\x0c!:3a3\x84\xac\xc0\xfe\xcf@ \x9a\x01\x86\xa4\x04&EWG\x05\x00\x00\x00\x00IEND\xaeB`\x82"
name_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x11\x00\x00\x00\x10\x08\x06\x00\x00\x00\xf01\x94_\x00\x00\x00aIDATx\x9c\xad\x92Q\n\x00 \x08Cgt\xff+\xd7W`\xc5\x9cdB\x98d\xcf1\x04r1\x8eL\x1bTMAMM\xc8\xc4\x82X\x05\xd4\xdc\xbd\x04R\x1e\xb0?\xfe\xa4\xe1\xf4\xcd\x82&s9\x84\xf4H\x8a\x08&`\x9b\x12y#=Q\xcbG%U\x96\xcd\xaa\x00\x00\x18~\xd9\x98\x17*\xdf\xc5\x8b\x92/\x9eLo\xc5+\xeb\xbc\xec0\x94\x00\x00\x00\x00IEND\xaeB`\x82"
merge_down_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00VIDATx\x9c\xddQ1\x12\x00 \x08\xc2\xfe\xffg\xdb\xea\xce YZbT\xe0\x10\x03@\xe2D\x90\x19\x18w\xb8D1\x93\x06U@\xc5\xc0\x8e*\t\r\xa2\xde\xea\x1a-]=A\x95'9\xac\x83\x9b\xc9\xb1\xbb\x95hA\x19\xb0\x144\xd9\xb3\x046>~\xa3\xfd\x85\x0e\x89\xa6\x97\t\x0fz\x0b n\xf1\x8ds\x00\x00\x00\x00IEND\xaeB`\x82"
up_carrot_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00QIDATx\x9c\xed\x92\xc1\x0e\x00 \x08B\xd5\xff\xffg;\xb55\x02\xe6\xadK\x1c\xe5\x81[\x16\xf1\xf5^i\xbc\x9e\xb05\x0c\xab\x19-\xa0\xa0\xf2\xb0\xc0\x85)S\xca\x98\x96\x14\x0e@\x19\xfa\xa1{\x03.L\xb7\x9eRW`[\xc7gt\x7f\xe3\xf2\xb0\xc0\x85)\xb3\x00\xc8\xb0\r\x10{\x8cD\xc6\x00\x00\x00\x00IEND\xaeB`\x82"
down_carrot_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xed\x91\xb1\x12\x00\x10\x0cCS\xff\xff\xcf5qJBM\x16\x99J\x9awU\xc0\xd7{\x19\x00\x9f\xce\x19\xf5LQF&\xcc\x00'\xc8\xe21\x80\x82Pp\x81~\xb7\x8bz\x94Y\xa2I\xc9\xda\x04\xe1\xe2&<\x03\xb2\x90\xd0\xc3\x96\xb8\x83,\x9e\xfa\x05\x06\xa1\xe0\nPm\x0b\x14\xaa\x93\x9f.\x00\x00\x00\x00IEND\xaeB`\x82"
plus_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\r\xfe\xa3\xf1\x19\xb1)b\xc2c\x00Q`\xd4\x00H\xc8\xa2\x876}]0\xf0\x06`M]P0\x9a\x12\xe9e\x00\x00"\xd2\x03\x1d\x12\xb9\x81\x89\x00\x00\x00\x00IEND\xaeB`\x82'

TILE_X_OFFSET = 10
TILE_Y_OFFSET = 10
TILE_WIDTH = 80
TILE_HEIGHT = 80
Y_PADDING = 10


class LayerManager(ttk.LabelFrame):
    def __init__(self, app, parent: ttk.Frame, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.app = app
        self.thumbnails = []
        self.tiles = []
        self.canvas_height = 700
        self.trash_image = sttk.load_tk_image_from_bytes_array(trash_bytes)
        self.copy_image = sttk.load_tk_image_from_bytes_array(copy_bytes_wide)
        self.up_image = sttk.load_tk_image_from_bytes_array(up_arrow_bytes)
        self.down_image = sttk.load_tk_image_from_bytes_array(down_arrow_bytes)
        self.name_image = sttk.load_tk_image_from_bytes_array(name_symbol_bytes)
        self.merge_image = sttk.load_tk_image_from_bytes_array(merge_down_symbol_bytes)
        self.new_image = sttk.load_tk_image_from_bytes_array(plus_symbol_bytes)
        self.new_from_image = sttk.load_tk_image_from_bytes_array(new_from_image_bytes)
        self.up_carrot_image = sttk.load_tk_image_from_bytes_array(up_carrot_bytes)
        self.down_carrot_image = sttk.load_tk_image_from_bytes_array(down_carrot_bytes)

        self.configure(text="Frames")
        (frame_tools_frame := ttk.Frame(self)).pack(fill="x", expand="False")
        self.new_frame_icon = sttk.load_tk_image_from_bytes_array(plus_symbol_bytes)
        (l := ttk.Label(frame_tools_frame, image=self.new_frame_icon)).pack(side="left")
        l.bind("<Button-1>", self.new_frame)

        self.canvas = tk.Canvas(self, relief="sunken")
        self.canvas.config(width=200, height=700, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.config(command=self.on_scroll_bar)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", expand=True, fill="both")
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.canvas_frame, anchor="nw")
        self.canvas_frame.config(width=200, height=self.winfo_height())
        self.canvas.config(scrollregion=(0, 0, 200, self.canvas_height))
        sttk.bind_mousewheel(self.canvas)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)

    def new_frame(self, event=None):
        self.app.project.new_frame()
        self.app.refresh()

    def rename_frame(self, frame):
        if name := tksimpledialog.askstring(
            "Rename Frame", f"What would you like to rename Frame: {frame.id} to?"
        ):
            frame.set_id(name)
            self.app.refresh()

    def ask_delete_frame(self):
        if len(self.app.project.frames) == 1:
            tkmessagebox.showwarning("Warning", "Cannot delete last frame.")
            return
        return tkmessagebox.askyesno(
            "Delete",
            "Are you sure you wish to delete this frame?\nThis cannot be undone.",
        )

    def delete_frame(self, frame):
        if self.ask_delete_frame():
            self.app.project.del_frame(frame)
            self.app.project.selected_frame = self.app.project.frames[0]
            self.canvas.after_idle(self.app.refresh)

    def copy_frame(self, frame):
        self.app.project.copy_frame(frame)
        self.canvas.after_idle(self.app.refresh)

    def promote_frame(self, frame):
        self.app.project.promote_frame(frame)
        self.canvas.after_idle(self.app.refresh)

    def demote_frame(self, frame):
        self.app.project.demote_frame(frame)
        self.canvas.after_idle(self.app.refresh)

    def toggle_collapsed(self, frame):
        self.app.project.toggle_collapsed(frame)
        self.canvas.after_idle(self.app.refresh)

    def rename_layer(self, frame, layer):
        if name := tksimpledialog.askstring(
            "Rename Layer", f"What would you like to rename Layer: {layer.id} to?"
        ):
            layer.set_id(name)
            self.canvas.after_idle(self.app.refresh)

    def new_layer_from_image(self, frame):
        if path := tkfiledialog.askopenfilename():
            layer = frame.new_layer_from_image(Image.open(path))
            self.canvas.after_idle(self.app.refresh)

    def new_layer(self, frame):
        frame.selected_layer = frame.new_layer()
        self.canvas.after_idle(self.app.refresh)

    def ask_delete_layer(self, frame, layer):
        if len(frame.layers) == 1:
            tkmessagebox.showwarning("Warning", "Cannot delete last layer.")
            return
        return tkmessagebox.askyesno(
            "Delete Layer?", f"Are you sure you wish to delete this layer?\n{layer.id}"
        )

    def delete_layer(self, frame, layer):
        if self.ask_delete_layer(frame, layer):
            frame.del_layer(layer)
            frame.selected_layer = frame.layers[0]
            self.canvas.after_idle(self.app.refresh)

    def copy_layer(self, frame, layer):
        frame.copy_layer(layer)
        self.canvas.after_idle(self.app.refresh)

    def promote_layer(self, frame, layer):
        frame.promote_layer(layer)
        self.canvas.after_idle(self.app.refresh)

    def demote_layer(self, frame, layer):
        frame.demote_layer(layer)
        self.canvas.after_idle(self.app.refresh)

    def merge_layer_down(self, frame, layer):
        frame.merge_layer_down(layer)
        self.canvas.after_idle(self.app.refresh)

    def on_click(self, event):
        y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
        x = event.x
        for t in self.tiles:
            if not t.is_in_row(y):
                t.deactivate()
                continue
            mode = t.on_click(x, y)
            if not mode:
                t.activate()
                if type(t) is FrameTile:
                    self.app.project.selected_frame = t.frame
                elif type(t) is LayerTile:
                    self.app.project.selected_frame = t.frame
                    t.frame.selected_layer = t.layer
                self.app.refresh()

    def on_mouse_move(self, event):
        y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
        x = event.x
        for t in self.tiles:
            if t.active:
                if t.is_in_row(y):
                    continue
                else:
                    t.deactivate()
            elif t.is_in_row(y):
                t.activate()

    def refresh(self, event=None):
        self.winfo_toplevel().update_idletasks()
        self.canvas.delete("all")
        self.thumbnails = []
        self.tiles = []
        if not self.app.project.frames:
            return
        i = 0  # Counts placed Tiles
        child_offset = 0.5 * TILE_WIDTH
        for f in self.app.project.frames:
            y = i * (TILE_HEIGHT + Y_PADDING) + TILE_Y_OFFSET
            self.tiles.append(t := FrameTile(self, f))
            i += 1
            t.set_dimensions(TILE_X_OFFSET, y, TILE_WIDTH, TILE_HEIGHT)
            self.place_tile(t)
            firstlayer = True  # Track if drawing first layer

            if not f.layers:
                i += 1
                continue
            if f.collapsed:
                continue

            for l in f.layers:
                line_x = TILE_X_OFFSET + 0.5 * child_offset
                line_y = y + TILE_HEIGHT
                line_bottom = line_y + Y_PADDING + 0.5 * TILE_HEIGHT

                self.canvas.create_line(
                    line_x,
                    line_y if firstlayer else y + 0.5 * child_offset,
                    line_x,
                    line_bottom,
                )

                # An if statement here is slower than just setting it to false each loop
                firstlayer = False

                self.canvas.create_line(
                    line_x, line_bottom, TILE_X_OFFSET + child_offset, line_bottom
                )
                y = i * (TILE_HEIGHT + Y_PADDING) + TILE_Y_OFFSET
                (tile := LayerTile(self, l, f)).set_dimensions(
                    TILE_X_OFFSET + child_offset,
                    y,
                    TILE_WIDTH,
                    TILE_HEIGHT,
                )
                self.place_tile(tile)
                self.tiles.append(tile)
                i += 1

        canvas_height = i * (TILE_HEIGHT + Y_PADDING) + TILE_Y_OFFSET
        frameheight = self.canvas_frame.winfo_height()
        self.canvas_height = (
            canvas_height if canvas_height > frameheight else frameheight
        )
        self.canvas_frame.config(width=200, height=self.winfo_height())
        self.canvas.config(scrollregion=(0, 0, 200, self.canvas_height))

    def place_tile(self, tile):
        tn = ImageTk.PhotoImage(tile.get_thumbnail(tile.height - 8))
        self.thumbnails.append(tn)
        tile.references.append(
            self.canvas.create_image(
                tile.x + 0.5 * tile.width, tile.y + 0.5 * tile.height, image=tn
            )
        )

        sel = self.app.project.selected_frame
        if isinstance(tile, FrameTile):
            outline_thickness = (1, 3)[tile.frame is sel]
        else:
            outline_thickness = (1, 3)[tile.layer is sel.selected_layer]
        tile.references.append(
            self.canvas.create_rectangle(
                tile.x,
                tile.y,
                tile.x + tile.width,
                tile.y + tile.height,
                width=outline_thickness,
            )
        )
        if tile.active:
            self.activate_tile()
        tile.references.append(
            self.canvas.create_text(
                tile.x + tile.width + 10,
                tile.y,
                font="CourierNew 8",
                text=tile.id,
                anchor="nw",
            )
        )

    def activate_tile(self, tile):
        tile.active_references.extend(
            [
                self.canvas.create_image(
                    tile.trash_x, tile.trash_y, anchor="nw", image=self.trash_image
                ),
                self.canvas.create_image(
                    tile.copy_x, tile.copy_y, anchor="nw", image=self.copy_image
                ),
                self.canvas.create_image(
                    tile.up_x, tile.up_y, anchor="nw", image=self.up_image
                ),
                self.canvas.create_image(
                    tile.down_x, tile.down_y, anchor="nw", image=self.down_image
                ),
                self.canvas.create_image(
                    tile.name_x, tile.name_y, anchor="nw", image=self.name_image
                ),
            ]
        )

        if isinstance(tile, LayerTile):
            tile.active_references.append(
                self.canvas.create_image(
                    tile.merge_x, tile.merge_y, anchor="nw", image=self.merge_image
                )
            )
        elif isinstance(tile, FrameTile):
            carrot_image = [self.up_carrot_image, self.down_carrot_image][
                tile.frame.collapsed
            ]
            tile.active_references.extend(
                [
                    self.canvas.create_image(
                        tile.new_x, tile.new_y, anchor="nw", image=self.new_image
                    ),
                    self.canvas.create_image(
                        tile.new_from_image_x,
                        tile.new_from_image_y,
                        anchor="nw",
                        image=self.new_from_image,
                    ),
                    self.canvas.create_image(
                        tile.carrot_x, tile.carrot_y, anchor="nw", image=carrot_image
                    ),
                ]
            )

    def deactivate_tile(self, tile):
        for r in tile.active_references:
            self.canvas.delete(r)

    def on_scroll_bar(self, move_type, move_units, __=None):
        if move_type == "moveto":
            self.canvas.yview("moveto", move_units)


class FrameTile(BaseTile):
    def __init__(self, manager, frame):
        BaseTile.__init__(self, manager)
        self.frame = frame
        self.id = frame.id
        self.thumbnail = None
        self.references = []
        self.active = frame.active
        self.active_references = []

    def set_dimensions(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

        self.new_x, self.new_from_image_x = [
            self.x + self.width + 10 + (i * 20) for i in range(2)
        ]
        self.copy_x, self.name_x, self.trash_x = [
            self.x + self.width + 10 + (i * 20) for i in range(3)
        ]
        self.up_x, self.down_x, self.carrot_x = [
            self.x + self.width + 10 + (i * 20) for i in range(3)
        ]
        (self.new_y, self.new_from_image_y) = [self.y + 20] * 2
        self.copy_y, self.name_y, self.trash_y = [self.y + 40] * 3
        self.up_y, self.down_y, self.carrot_y = [self.y + 60] * 3

    def get_thumbnail(self, size):
        self.thumbnail = self.frame.export_composite_image().resize(
            (size, size), Image.BOX
        )
        return self.thumbnail

    def check_click_regions(self, pointer_x, pointer_y):
        mgr = self.manager
        for coords, callback in (
            ((self.new_x, self.new_y), mgr.new_layer),
            ((self.new_from_image_x, self.new_from_image_y), mgr.new_layer_from_image),
            ((self.trash_x, self.trash_y), mgr.delete_frame),
            ((self.copy_x, self.copy_y), mgr.copy_frame),
            ((self.up_x, self.up_y), mgr.promote_frame),
            ((self.down_x, self.down_y), mgr.demote_frame),
            ((self.name_x, self.name_y), mgr.rename_frame),
            ((self.carrot_x, self.carrot_y), mgr.toggle_collapsed),
        ):
            if sttk.check_in_bounds(
                (pointer_x, pointer_y),
                (coords[0], coords[1], coords[0] + 16, coords[1] + 16),
            ):
                callback(self.frame)
                return True


# This object holds both the layer data and the data for the layer panels for a respective layer
class LayerTile(BaseTile):
    def __init__(self, manager, layer, frame):
        BaseTile.__init__(self, manager)
        self.layer = layer
        self.frame = frame
        self.id = layer.id
        self.thumbnail = None
        self.references = []
        self.active = layer.active
        self.active_references = []

    def set_dimensions(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.copy_x, self.name_x, self.trash_x = [
            self.x + self.width + 10 + (i * 20) for i in range(3)
        ]
        self.up_x, self.down_x, self.merge_x = [
            self.x + self.width + 10 + (i * 20) for i in range(3)
        ]
        self.copy_y, self.name_y, self.trash_y = [self.y + 40] * 3
        self.up_y, self.down_y, self.merge_y = [self.y + 60] * 3

    def get_thumbnail(self, size):
        self.thumbnail = self.layer.export_image().resize((size, size), Image.BOX)
        return self.thumbnail

    def check_click_regions(self, pointer_x, pointer_y):
        mgr = self.manager
        for coords, callback in (
            ((self.trash_x, self.trash_y), mgr.delete_layer),
            ((self.copy_x, self.copy_y), mgr.copy_layer),
            ((self.up_x, self.up_y), mgr.promote_layer),
            ((self.down_x, self.down_y), mgr.demote_layer),
            ((self.name_x, self.name_y), mgr.rename_layer),
            ((self.merge_x, self.merge_y), mgr.merge_layer_down),
        ):
            if sttk.check_in_bounds(
                (pointer_x, pointer_y),
                (coords[0], coords[1], coords[0] + 16, coords[1] + 16),
            ):
                callback(self.frame, self.layer)
                return True
