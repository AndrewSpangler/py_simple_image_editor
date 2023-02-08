import os
import sys
import shutil
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk

import py_simple_ttk as sttk
from PIL import Image, ImageTk

from .pixel import tool_controller, TOOLCONST
from .pixel.pallete_frame import ToolColumn
from .pixel.save_window import SaveMenu
from .pixel.layer_viewer import LayerViewer
from .pixel.pixel import PixelProject
from .pixel.pixel_canvas import PixelCanvas
from .pixel.layer_manager import LayerManager
from .pixel.tool_bar import ToolBar

from .version import __version__ as version

# fmt: off
floppy_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00YIDATx\x9c\xbd\x93A\n\x00 \x08\x04w\xa3\xff\x7f\xb9nb\x1bDj$t\x08\xb6q\x10#\x80\x81X\xd1_Z\xf01\xb4\xa1\x07P\x82tG3\x06\xc9\x18,\x90\x0c`\x81\xf4C\xe8j\xb8Y\x03+5\xd0A\xfe7\xb8]*3}n\xb0u\x90\xda\x0c\xcb\x06e\x00\x11\xff\x8do\r&2<\t)\xe6\x84\xac\xa0\x00\x00\x00\x00IEND\xaeB`\x82'
export_to_bytes_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5R\xcb\x0e\x00 \x08\xa2\xd6\xff\xff\xb2\x9d<\xf8\xc0Z[\x93#"S\x11\xe8\xc6\x00 \x84\xcf\x90i\x03\x99\x8aXm\x16\xe2+\xf4\x1b\xac\x87\x1es\x07f \x88Ih\xa3\xe1\xd9\n>\xde\xcc\xb0\x9c\xc0\x9b\xb0\xbf\xf8\x9b\x82\x8e\xcd\xbe\x158\x14\xaf\x8e\xd8\x8f\r^q\x0f\x17I\xca\t\xc4\x00\x00\x00\x00IEND\xaeB`\x82'
to_grayscale_bytes=  b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x8bIDATx\x9c\xad\x93K\x0e\xc40\x08C\xedjn\x04\xf7\xbf\x9a\xbbh'\x9f\x16JT\xd5\xd9$!<\x8cD(@HD\x80Y\xec\xaf\xdf\x94pG\xf5\x1b\xc6\xb0\xad\xaaP\xa9\x01\xdc\xec,\xd9\xd7\x8a(@\x1c\x1eK\x00\xc9s\xaf\xee\xfcM\x0b$K'7\x00yT^\x85\xb0\x1b\x9f5\xb6r\x9c'h\x0b\xa4\x80\x0cB\x12\x92\xe0\xeeq\x0bU;W-\xcd\x81b\x83\x00\xda$\x06\xe8!=\xaa|\x01\xe4r\xf7G\x07\xe5g1\xb3\xc7A\xf8\xee/\xbc\xd5\x0e\xfa38\x83C\xf0\x9e\x91\x00\x00\x00\x00IEND\xaeB`\x82"
flip_horizontal_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xb5\x92K\n\x00 \x08D\xc7\xe8\xfeW\xb6E\x10a\xa3)\xd1,\xfd\xbctL\x00(\xa6\x045)\x00\xb4b\xd3\xa1o\x00M\xc6(\x80\x16z9\x0b\x88\x0c\x15S\xb3\x82\x96z\xbb\xc6\x15P\xd2\xf3\x15:\x89\x95V\xd8'\xa0&9\xcd\xeb\x11\xbbB\x04\xa1\x17b\x1eD+\x1c9\xcf\xc4\xe8\x1f\xa4\x00i=\x03\x06R\x89\x10\x1d\x11\x13\xf1_\x00\x00\x00\x00IEND\xaeB`\x82"
flip_vertical_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00[IDATx\x9c\xcdS1\x12\x00 \x08\xc2\xfe\xffg\x9b\xba\xeb\x14tp(GQ\x025\x03\xe0\x18\xc4\x9a4\x03\x80\x15XTFk\x95\x02f\x8bZe\x04\xa7\xf0~\xd1\x02&\tXsKR\x85w\r\xe3-\xfcG\xd0yNx$\xa8&M7\xa4.Q\xa9H\xf5j\x06\xd5\x1d\xa4\xe4\xdb\xdf\xb8\x013\x0b\x12\x13\xd2\xdc\xdaE\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_right_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00fIDATx\x9c\xad\x93Q\x0e\xc0 \x08C[\xb2\xfb_\x99\xfdl\xc9\x82E\xa6\xd8\xc4\x1fy\x14A\x05\x9a\xe2$\xe6\x05\xeb\x00\xa8\x0cb\xa2*\xfa2\x83\x81\x07\xb02\xa6\t\x80"Y\x19\x02\x00Lm&\x92\xadY\x08fCM\xe7r\xfd\xac\x9e\xde\xd6J\x0b_\xf9\xb3\xb6\r\xe6\xae+\\\xfb\x04\xbb\x0f\x89\x19\x14\xc1\xb2h\xe73\x9d\xd1\r4\xaa\x14\x12L4\x91\xa7\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_left_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xadS[\x12\x00\x11\x0c\xeb\x1a\xf7\xbfr\xf7\x07S6\xad\xd0\xcd\x0f\xfaH\xc2\x94H\x12O[\xd5\xec\xc5\xc4P\xadK\xd0\xcfk\xa3\xd7\x03\t"EE\xb9\xc2\xa8\x98\xd8G\xd0#\xd8]c\xc0#\x88H&\x17u\t\x1e\xa3;\xd0@\x91"\xf8\x05\xac\x8b\xa9.\xed\x80\x1a\x96(\x87^\xffj\x94\x11\xa8\xcf\x94\xc6\x0b\xc0j\x14\x121\x82h\xc9\x00\x00\x00\x00IEND\xaeB`\x82'
selection_options_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00aIDATx\x9c\xed\x94K\n\xc0 \x0cD\x9f\xa5\xf7\xbf\xf2t\xd3H\x08\xfd\xa8\xd1\x9d\x0f\x04cd\x98\x0c"\x80\xeee\xa4\xea\x83\xc9\x94\x89Z\x82\x05\x0eMY\xbf\xb7\x1a\xd9\x19\xe6\xd9\x19\xe6Y\xe2\xb0\x97\xafi4\xea\xf0IT~\xd3\x9b\xe1\xeb\x9f8\xea\xd0\x9e\x9b\x17.\xbeAl4\xd4\xf1L\x00\xe7\xa0\xc3\xe8\xb4r\x01\xe1\r#\xfeK\xaa+`\x00\x00\x00\x00IEND\xaeB`\x82'
layers_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x88IDATx\x9c\xdd\x94Q\x0e\xc0 \x08C\xd5\xfb\xdf\x99\xfd\x0c3\xb1\xd4\xea\xf65\x13\x13E\xf6V\x1a\xb4\x94|\xd8=\xb7F%05w\x99\xb4RE\xc1\xf1p\xa7D\x08~\x06\xb7\xfdB`\xdf\x9c\xc2&V\xfb\x126,^\x80\x87\x92[8\x90Z\x03\xc0\xba\x18/\xd9B\x92\x02\x86\xfe\xd7\x18\x000\xd6\xe4\x16\xf6\xd4\xc3\x0c\x9c\xc2\xd0G\n8\x83W\x0f\xc0?\x110U\xfa\x7f\x0f'Q\xac\xdf\x14\x0f\xa7\xb5\xd2\xc0\xab\xc76S+\x81\xb3\xfb\xde\xe3\x17\xc0\xce,\x11\xce3\xde\x16\x00\x00\x00\x00IEND\xaeB`\x82"
folder_options_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00dIDATx\x9c\xa5RA\x0e\xc0 \x08\x03\xb3\xff\x7f\x99\x1d\x16\x17m\xc0\x96\xd8\x0bQ\xda\xda n\x1f\xc2j\xf8\xa1g\x83\x88\x99\xb9\xf9B\xc8^\n\xe0\xb6\rh\x82qj21&`\xbc\xd4\x9c%\xa8\xc4?\x1e\x95XAIpm\x803\xda\xcej\x82\x80\xda2\x98\xb3I\xf7EM\xe0P\xdb\x06\xa9x^*\x8bT\xe2\xfa\x1b_\xdd\xf7\x10\x1a%V\x92.\x00\x00\x00\x00IEND\xaeB`\x82'
effects_wand_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00dIDATx\x9c\x9d\x93\xc1\x12\x00 \x04D\xe3\xff\xffY\xa7\x1aE\xbb\xd4%\x8c\xb7\xb32\x8d\xc1\x8f\xa1\xba4`y\xd4[\x0eB\xcc\x1cP7\xfa\x01\x1fyE \x9b\xb7\xec\x00\xc1\xf4\r(\x8c\x1c@\xdb.\x96L\x80\xc1\xe6k\xb7@\x15NG`\xb0\xcf\xc3\x16*\xf0\xea;\x1ci\x03\xf6"\xfb\x0ek!0\xec\xed\xfc\xb0\xdd;\x01\xa1\x94 \n\xf4#\xf2;\x00\x00\x00\x00IEND\xaeB`\x82'
copy_options_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x81IDATx\x9c\xb5\x94Q\x0e\xc0 \x08C\xcb\xe2\xfd\xaf\xcc\xbefP\x11jd\xfd2b\xca\x93\x00\x02@\x11K\x92\xf8\xa0\x87x\x93%\\\xb2\xab9GF\x14)C\xf8\x19Q\xa4\x8c\xe1\x91i#\xccf\x93\xb0\x14,\xe1IB\xa8wI\xc4\xed}\x8fW\x10\x02\xa6[\x98\x1af\xb2\xf4ZE\xd8uC\xe8\x0e\xc2\xaf\x84G3\xbbS9!\xa3\xacO\x07\xdd\x12.cY9z\np;n\xf7]o\x03\xc9\r\xe1\xbc\x98\x05\x00^\x98\t\x1e\x18"\xcb\xe9\x0c\x00\x00\x00\x00IEND\xaeB`\x82'
undo_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00jIDATx\x9c\xed\xd21\x0e\xc0 \x0c\x03@\x87\xff\xff\x99n\x15DN\x130\x03C=\xd2\xe8b*\x00\x9e\x1e\x9c\xa7i'1\x06J\x98\x07e\x0c\x00l\x11\xb3\xca\xc0N\xb3\x10^m\x98\xc2\xe3\x81GY\x0b\xb6x\x9ak\xd1\x87\x8fF~nZ\xe2\x9fM\x05e\xf0\x8b\xb2\x87]E\xc3Mj\xc6+\x1bk(\xe5DC \xf9\x87R~\xf0B\xf0\x01\xe9\xd5\r!*\x08\x90\x91\x00\x00\x00\x00IEND\xaeB`\x82"
redo_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00cIDATx\x9c\xed\xd2\xb1\x0e\x80@\x08\x03\xd0b\xfc\xff_>\'\xd4\x0b\x8dr\xd0\xc1\xc1\x8e\xa4y0\x00\xd43\xd8pk\x80\x14\xed\x82\x01U\x80\x13j\x95+\x1ebo`\x16\xbaD\x15\xe4\x1e\x03\x19\x96\xe9\x19\x00\xec\x99R"g\xef\x0e\x0eVX\xc1\x80\xfe\xdb\x84\xc5>\xa8^\x17\xa2z\xec\t\x94]\xe7\xa04?\xf8A\xf0\x00\xc1\x1f\r$\x92}T\x8b\x00\x00\x00\x00IEND\xaeB`\x82'
# fmt: off

WIDTH = 1080
HEIGHT = 720
SIZE = 25

DEFAULT_CONFIG = {
    "application": "py_simple_image_editor",
    "icon": sttk.get_asset("ico.png"),
    "version": version,
    "enable_profiles": False,
    "conversations_enabled": False,
    "notes_enabled": False,
    "theme_textboxes": False,
    "ignored_themes": [],
    "width": 1280,
    "height": 720,
    "scaling": 2,
    "enable_themes_menu": True,
    "enable_sizegrip": True,
    "disable_notebook": True,
    "default_theme": "clam",
}

def bind_popup(binding, widget, menu):
    def popup(event):
        menu.post(
            widget.winfo_rootx(),
            widget.winfo_rooty() + widget.winfo_height()
        )
    widget.bind(binding, popup)


class Editor(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.file = None
        self.tool_controller = tool_controller
        self.project = PixelProject(SIZE, SIZE)
        self.drawtips_references = []

        # fmt: off
        self.floppy_image = sttk.load_tk_image_from_bytes_array(floppy_bytes)
        self.bytes_image = sttk.load_tk_image_from_bytes_array(export_to_bytes_bytes)
        self.horizontal_flip_image = sttk.load_tk_image_from_bytes_array(flip_horizontal_bytes)
        self.vertical_flip_image = sttk.load_tk_image_from_bytes_array(flip_vertical_bytes)
        self.rotate_left_image = sttk.load_tk_image_from_bytes_array(rotate_left_bytes)
        self.rotate_right_image = sttk.load_tk_image_from_bytes_array(rotate_right_bytes)
        self.to_grayscale_image = sttk.load_tk_image_from_bytes_array(to_grayscale_bytes)
        self.selection_options_image = sttk.load_tk_image_from_bytes_array(selection_options_bytes)
        self.layers_symbol_image = sttk.load_tk_image_from_bytes_array(layers_symbol_bytes)
        self.folder_options_symbol = sttk.load_tk_image_from_bytes_array(folder_options_symbol_bytes)
        self.effects_wand_symbol = sttk.load_tk_image_from_bytes_array(effects_wand_symbol_bytes)
        self.copy_options_symbol = sttk.load_tk_image_from_bytes_array(copy_options_symbol_bytes)
        self.undo_symbol = sttk.load_tk_image_from_bytes_array(undo_symbol_bytes)
        self.redo_symbol = sttk.load_tk_image_from_bytes_array(redo_symbol_bytes)
        # fmt: on

        (horizontal_panes := tk.PanedWindow(self, sashpad=3, sashrelief ="sunken", borderwidth = 0)).pack(fill = "both", expand = True)

        (left_side_frame := ttk.Frame(horizontal_panes)).pack(fill = "both", expand = True, side = "left")
        horizontal_panes.add(left_side_frame)

        (gif_tool_bar := ToolBar([], left_side_frame)).pack(fill = "x", pady = (0,2))

        (left_column_panes := tk.PanedWindow(left_side_frame, orient = "vertical", sashpad=3, sashrelief ="sunken", borderwidth = 0)).pack(fill = "both", expand = True, padx = 4, pady = (0,4))

        (gif_view := LayerViewer(self.project, SIZE, SIZE, left_column_panes)).pack(fill = "both", expand = True)
        left_column_panes.add(gif_view)
        
        self.frame_manager = LayerManager(self, left_column_panes)
        self.frame_manager.pack(side = "left", fill = "both", expand = True, pady = 0)
        left_column_panes.add(self.frame_manager)

        (middle_pane := ttk.Frame(horizontal_panes)).pack(fill = "both", expand = True, side = "right")
        horizontal_panes.add(middle_pane)

        tool_buttons = [
            (self.vertical_flip_image, self.flip_vertical),
            (self.horizontal_flip_image, self.flip_horizontal),
            (self.rotate_left_image, self.rotate_left),
            (self.rotate_right_image, self.rotate_right),
        ]
        (tool_bar := ToolBar(tool_buttons, middle_pane)).pack(fill = "x")

        horizontal_panes.add(right_column_panes := tk.PanedWindow(
            horizontal_panes,
            orient = "vertical",
            sashpad=3,
            sashrelief ="sunken",
            borderwidth = 0,
            )
        )
        horizontal_panes.paneconfigure(right_column_panes)
        # right_column_panes()s
        # .pack(fill = "both", expand = True, padx = 4, pady = (0,4))
        self.tool_column = ToolColumn(self, right_column_panes)
        self.tool_column.pack(fill="both", expand=True)

        
        # fmt: off
        menus = {
            gif_tool_bar: {
                self.floppy_image: (
                    ("Export Gif", self.export_gif),
                    ("Export Selected Frame", self.export_selected_layer),
                    ("Export Selected Layer", self.export_selected_frame),
                ),
                self.folder_options_symbol: (
                    ("Import Gif as Frames", self.import_gif),
                    ("Load Folder as Frames", self.load_folder_as_frames),
                )
            },
            tool_bar : {
                self.layers_symbol_image: (
                    ("Rename Current Layer", self.rename_selected_layer),
                    ("Export Current Layer", self.save),
                    ("Delete Current Layer", self.delete_selected_layer),
                    ("Duplicate Current Layer", self.copy_selected_layer),
                    ("Promote Current Layer", self.promote_selected_layer),
                    ("Demote Current Layer", self.demote_selected_layer),
                    ("Merge Layer Down", self.merge_selected_layer_down),
                    "separator",
                    ("Rename Current Frame", self.rename_selected_frame),
                    ("Export Current Frame", self.save_selected_frame),
                    ("Delete Current Frame", self.delete_selected_frame),
                    ("Duplicate Current Frame", self.copy_selected_frame),
                    ("Promote Current Frame", self.promote_selected_frame),
                    ("Demote Current Frame", self.demote_selected_frame),
                    ("New Layer in Current Frame", self.new_layer),
                    ("New Layer from Image in Current Frame", self.new_layer_from_image_in_selected_frame),
                ),
                self.selection_options_image: (
                    ("Flood Fill Selection", self.fill_selection),
                    ("Flip Selection Vertical", self.flip_selection_vertical),
                    ("Flip Selection Horizontal", self.flip_selection_horizontal),
                    ("Rotate Selection Right", self.rotate_selection_right),
                    ("Rotate Selection Left", self.rotate_seletion_left),
                    ("Export Selection", self.export_selection),
                    "separator",
                    ("Copy Selection to Clipboard", self.copy_selection_to_clipboard),
                    ("New Layer from Selection", self.new_layer_image_from_selection),
                    "separator",
                    ("Apply Blur Filter to Selection", self.effect_blur_selection),
                    ("Apply Contour Filter to Selection", self.effect_contour_selection),
                    ("Apply Detail Filter to Selection", self.effect_detail_selection),
                    ("Apply Edge Enhance Filter to Selection", self.effect_edge_enhance_selection),
                    ("Apply Edge Enhance More Filter to Selection", self.effect_edge_enhance_more_selection),
                    ("Apply Emboss Filter to Selection", self.effect_emboss_selection),
                    ("Apply Find Edges Filter to Selection", self.effect_find_edges_selection),
                    ("Apply Sharpen Filter to Selection", self.effect_sharpen_selection),
                    ("Apply Smooth Filter to Selection", self.effect_smooth_selection),
                    ("Apply Smooth More Filter to Selection", self.effect_smooth_more_selection),
                    ("Apply Gaussian Filter to Selection", self.effect_gaussian_selection),
                    ("Apply Box Blur Filter to Selection", self.effect_box_blur_selection),
                    ("Apply Median Filter to Selection", self.effect_median_filter_selection),
                    ("Apply Min Filter to Selection", self.effect_min_filter_selection),
                    ("Apply Max Filter to Selection", self.effect_max_filter_selection),
                    ("Apply Mode Filter to Selection", self.effect_mode_filter_selection),
                ),
                self.effects_wand_symbol: (
                    ("Apply Blur Filter", self.effect_blur_layer),
                    ("Apply Contour Filter", self.effect_contour_layer),
                    ("Apply Detail Filter", self.effect_detail_layer),
                    ("Apply Edge Enhance Filter", self.effect_edge_enhance_layer),
                    ("Apply Edge Enhance More Filter", self.effect_edge_enhance_more_layer),
                    ("Apply Emboss Filter", self.effect_emboss_layer),
                    ("Apply Find Edges Filter", self.effect_find_edges_layer),
                    ("Apply Sharpen Filter", self.effect_sharpen_layer),
                    ("Apply Smooth Filter", self.effect_smooth_layer),
                    ("Apply Smooth More Filter", self.effect_smooth_more_layer),
                    ("Apply Gaussian Filter", self.effect_gaussian_layer),
                    ("Apply Box Blur Filter", self.effect_box_blur_layer),
                    ("Apply Median Filter", self.effect_median_filter_layer),
                    ("Apply Min Filter", self.effect_min_filter_layer),
                    ("Apply Max Filter", self.effect_max_filter_layer),
                    ("Apply Mode Filter", self.effect_mode_filter_layer),
                ),
                self.copy_options_symbol : (
                    ("Copy Current Layer to Clipboard", self.copy_selected_layer_to_clipboard),
                    ("Copy Current Frame to Clipboard", self.copy_selected_frame_to_clipboard),
                    ("Copy Selection to Clipboard", self.copy_selection_to_clipboard),
                    "separator",
                    ("Paste As New Layer in Current Frame", self.paste_as_new_layer_in_current_frame),
                    ("Paste As New Layer in New Frame", self.paste_as_new_layer_in_new_frame),
                )
            },
        }
        # fmt: on

        for toolbar, items in menus.items():
            for icon, commands in items.items():
                menu = tk.Menu(self, tearoff=0)
                for element in commands:
                    if isinstance(element, tuple):
                        menu.add_command(label=element[0], command=element[1])
                    else:
                        menu.add_separator()
                (button := ttk.Label(toolbar, image = icon, font = "bold")).pack(side = "left")
                bind_popup("<Button-1>", button, menu)

        (undo_button := ttk.Label(tool_bar, image = self.undo_symbol)).pack(side = "left")
        undo_button.bind("<Button-1>", self.undo)

        (redo_button := ttk.Label(tool_bar, image = self.redo_symbol)).pack(side = "left")
        redo_button.bind("<Button-1>", self.redo)

        self.canvas_frame = ttk.LabelFrame(middle_pane)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = PixelCanvas(self.canvas_frame, self.project)
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.canvas.bind("<Button-2>", self.eyedrop)
        self.canvas.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.canvas.bind("<ButtonPress-3>", self.on_erase_start)
        self.canvas.canvas.bind("<B3-Motion>", self.on_erase)
        self.canvas.canvas.bind("<ButtonRelease-3>", self.on_erase_end)

        (footer := ttk.Frame(middle_pane)).pack(side = "bottom", fill = "x", expand = False, padx = 3)
        self.footer_var = tk.StringVar()
        ttk.Label(footer, textvariable = self.footer_var).pack(side = "left", expand = False, fill = "x")

        self.scheduled_canvas_resize = None
        self.bind("<Configure>", self.on_canvas_resize)

        self.after_idle(self.refresh)

    def undo(self, event = None):
        self.project.selected_frame.selected_layer.undo()
        self.refresh()

    def redo(self, event = None):
        self.project.selected_frame.selected_layer.redo()
        self.refresh()

    def load_folder_as_frames(self):
        if (path := tkfiledialog.askdirectory()):
            entries = os.scandir(path)
            files = [e for e in entries if e.is_file()]
            for f in files: self.project.new_frame_from_image(Image.open(f.path))
            self.refresh()

    def import_gif(self):
        if (path := tkfiledialog.askopenfilename()):
            self.load_gif(path)

    def load_gif(self, path):
        self.project.import_gif(path)
        self.refresh()

    def export_gif(self):
        SaveMenu(self, self.project.export_gif_frames(), gif = True)

    def export_selected_layer(self):
        SaveMenu(self, self.project.selected_frame.selected_layer.export_image())

    def export_selected_frame(self):
        SaveMenu(self, self.project.selected_frame.export_composite_image())

    def refresh(self):
        self.canvas.redraw()
        self.frame_manager.refresh()
        self.canvas_frame.configure(text=f"{self.project.selected_frame.id} - {self.project.selected_frame.selected_layer.id}")
        self.tool_column.refresh()

    def on_canvas_resize(self, event=None):
        if self.scheduled_canvas_resize:
            self.after_cancel(self.scheduled_canvas_resize)
        self.scheduled_canvas_resize = self.after_idle(self.do_resize)

    def do_resize(self):
        self.scheduled_canvas_resize = None
        self.canvas.refresh()

    def draw_canvas_draw_path(self, x1, y1, x2, y2):
        for r in self.drawtips_references:
            self.canvas.canvas.delete(r)
        if self.tool_controller.tool in [TOOLCONST.LINE, TOOLCONST.MOVE_SELECTION]:
            return self.canvas.canvas.create_line(x1, y1, x2, y2, fill = "#000000", width = 2)
        elif self.tool_controller.tool in [TOOLCONST.RECTANGLE, TOOLCONST.SELECT_BOX, TOOLCONST.FILLED_RECTANGLE]:
            return self.canvas.canvas.create_rectangle(x1, y1, x2, y2, fill = "", width = 2)
        elif self.tool_controller.tool in [TOOLCONST.ELLIPSE, TOOLCONST.FILLED_ELLIPSE]:
            return self.canvas.canvas.create_oval(x1, y1, x2, y2, fill = "", width = 2)

    def on_canvas_click(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            if self.tool_controller.handle_start(self.project.selected_frame.selected_layer, id): 
                self.refresh()
            if self.tool_controller.drag:
                x1, y1 = (int(v) for v in self.tool_controller.start_id.split("x"))
                x2, y2 = x1, y1
                self.drawtips_references.append(self.draw_canvas_draw_path(x1, y1, x2, y2))

    def on_canvas_drag(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            if self.tool_controller.handle_drag(self.project.selected_frame.selected_layer, id):
                self.refresh()
            if self.tool_controller.drag:
                x1, y1 = (int(v) for v in self.tool_controller.start_id.split("x"))
                x2, y2 = (int(v) for v in id.split("x"))
                cords = (x1, y1, x2, y2)
                x1, y1, x2, y2 = ((self.canvas.pixel_width * x + 0.5 * self.canvas.pixel_width) for x in cords)
                self.drawtips_references.append(self.draw_canvas_draw_path(x1, y1, x2, y2))

    def on_canvas_release(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            if self.tool_controller.handle_end(self.project.selected_frame.selected_layer, id):
                self.refresh()
            if self.tool_controller.drag:
                for r in self.drawtips_references:
                    self.canvas.canvas.delete(r)

    def on_erase_start(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            self.tool_controller.handle_erase_start(self.project.selected_frame.selected_layer, id)
            self.refresh()

    def on_erase(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            self.tool_controller.handle_erase(self.project.selected_frame.selected_layer, id)
            self.refresh()

    def on_erase_end(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            self.tool_controller.handle_erase_end(self.project.selected_frame.selected_layer, id)
            self.refresh()

    def eyedrop(self, event):
        color = self.project.selected_frame.selected_layer.get_pixel_color(self.canvas.get_cell_id(event.x, event.y))
        self.pallete_frame.set_color(color)

    def on_press(self, event):
        self.grip["cursor"] = "bottom_right_corner"

    def on_mouse_move(self, event):
        if (id := self.canvas.get_cell_id(event.x,event.y)):
            color = self.project.selected_frame.selected_layer.get_pixel_color(id)
            rgba = f"R: {color[0]}, G: {color[1]}, B: {color[2]}, A: {color[3]}"
            self.footer_var.set(f"{id}  |  {rgba}")

    def on_release(self, event):
        self.grip["cursor"] = "arrow"
        self.refresh()

    def save(self):
        SaveMenu(self, self.project.selected_frame.selected_layer.export_image())

    def new_layer_from_image(self, event = None):
        path = tkfiledialog.askopenfilename()
        if path:
            image = Image.open(path).convert("RGBA")
            layer = self.project.selected_frame.new_layer_from_image(image)
        self.refresh()

    def new_layer(self, event = None):
        layer = self.project.selected_frame.new_layer()
        self.project.selected_frame.selected_layer = layer
        self.refresh()

    def load_image(self, tkimage):
        self.project.selected_frame.new_layer().load_image(tkimage)
        self.refresh()

    def load_blank(self):
        self.project.select_frame(0)
        self.project.selected_frame.select_layer(0)
        self.refresh()

    def flip_vertical(self):
        self.tool_controller.flip_layer_vertical(self.project.selected_frame.selected_layer)
        self.refresh()

    def flip_horizontal(self):
        self.tool_controller.flip_layer_horizontal(self.project.selected_frame.selected_layer)
        self.refresh()

    def rotate_left(self):
        self.tool_controller.rotate_layer_left(self.project.selected_frame.selected_layer)
        self.refresh()

    def rotate_right(self):
        self.tool_controller.rotate_layer_right(self.project.selected_frame.selected_layer)
        self.refresh()

    def to_grayscale(self):
        self.canvas.to_grayscale()
        self.refresh()

    def effect_blur_layer(self):
        self.tool_controller.effect_blur_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_contour_layer(self):
        self.tool_controller.effect_contour_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_detail_layer(self):
        self.tool_controller.effect_detail_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_edge_enhance_layer(self):
        self.tool_controller.effect_edge_enhance_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_edge_enhance_more_layer(self):
        self.tool_controller.effect_edge_enhance_more_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_emboss_layer(self):
        self.tool_controller.effect_emboss_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_find_edges_layer(self):
        self.tool_controller.effect_find_edges_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_sharpen_layer(self):
        self.tool_controller.effect_sharpen_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_smooth_layer(self):
        self.tool_controller.effect_smooth_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_smooth_more_layer(self):
        self.tool_controller.effect_smooth_more_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_gaussian_layer(self):
        if (radius := tksimpledialog.askinteger("Gaussian Blur Filter", "Filter Radius:", parent=self.window)):
            self.tool_controller.effect_gaussian_layer(self.project.selected_frame.selected_layer)
            self.refresh()

    def effect_box_blur_layer(self):
        if (radius := tksimpledialog.askinteger("Box Blur Filter", "Filter Radius:", parent=self.window)):
            self.tool_controller.effect_box_blur_layer(self.project.selected_frame.selected_layer)
            self.refresh()

    def effect_median_filter_layer(self):
        if (size := tksimpledialog.askinteger("Median Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_median_filter_layer(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_min_filter_layer(self):
        if (size := tksimpledialog.askinteger("Min Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_min_filter_layer(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_max_filter_layer(self):
        if (size := tksimpledialog.askinteger("Max Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_max_filter_layer(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_mode_filter_layer(self):
        if (size := tksimpledialog.askinteger("Mode Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_mode_filter_layer(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_blur_selection(self):
        self.tool_controller.effect_blur_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_contour_selection(self):
        self.tool_controller.effect_contour_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_detail_selection(self):
        self.tool_controller.effect_detail_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_edge_enhance_selection(self):
        self.tool_controller.effect_edge_enhance_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_edge_enhance_more_selection(self):
        self.tool_controller.effect_edge_enhance_more_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_emboss_selection(self):
        self.tool_controller.effect_emboss_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_find_edges_selection(self):
        self.tool_controller.effect_find_edges_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_sharpen_selection(self):
        self.tool_controller.effect_sharpen_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_smooth_selection(self):
        self.tool_controller.effect_smooth_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_smooth_more_selection(self):
        self.tool_controller.effect_smooth_more_selection(self.project.selected_frame.selected_layer)
        self.refresh()

    def effect_gaussian_selection(self):
        if (radius := tksimpledialog.askinteger("Gaussian Blur Filter", "Filter Radius:", parent=self.window)):
            self.tool_controller.effect_gaussian_selection(self.project.selected_frame.selected_layer)
            self.refresh()

    def effect_box_blur_selection(self):
        if (radius := tksimpledialog.askinteger("Box Blur Filter", "Filter Radius:", parent=self.window)):
            self.tool_controller.effect_box_blur_selection(self.project.selected_frame.selected_layer)
            self.refresh()

    def effect_median_filter_selection(self):
        if (size := tksimpledialog.askinteger("Median Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_median_filter_selection(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_min_filter_selection(self):
        if (size := tksimpledialog.askinteger("Min Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_min_filter_selection(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_max_filter_selection(self):
        if (size := tksimpledialog.askinteger("Max Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_max_filter_selection(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def effect_mode_filter_selection(self):
        if (size := tksimpledialog.askinteger("Mode Blur Filter", "Filter Size:", parent=self.window)):
            self.tool_controller.effect_mode_filter_selection(self.project.selected_frame.selected_layer, size)
            self.refresh()

    def fill_selection(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            self.tool_controller.fill_selection(layer, layer.start_selection, layer.end_selection)
            self.refresh()

    def flip_selection_vertical(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            self.tool_controller.flip_selection_vertical(layer, layer.start_selection, layer.end_selection)
            self.refresh()

    def flip_selection_horizontal(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            self.tool_controller.flip_selection_horizontal(layer, layer.start_selection, layer.end_selection)
            self.refresh()

    def rotate_selection_right(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            self.tool_controller.rotate_selection_right(layer, layer.start_selection, layer.end_selection)
            self.refresh()

    def rotate_seletion_left(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            self.tool_controller.rotate_selection_left(layer, layer.start_selection, layer.end_selection)
            self.refresh()

    def export_selection(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            SaveMenu(self, self.tool_controller.crop_to_selection(layer, layer.start_selection, layer.end_selection))
            self.refresh()

    def copy_selection_to_clipboard(self):
        layer = self.project.selected_frame.selected_layer
        if layer.start_selection and layer.end_selection:
            image = self.tool_controller.copy_selection_to_clipboard(layer)
            self.refresh()

    def copy_selected_layer_to_clipboard(self):
        self.tool_controller.copy_layer_to_clipboard(self.project.selected_frame.selected_layer)
        self.refresh()

    def copy_selected_frame_to_clipboard(self):
        self.tool_controller.copy_frame_to_clipboard(self.project.selected_frame)
        self.refresh()

    def paste_as_new_layer_in_current_frame(self):
        self.tool_controller.paste(self.project.selected_frame.new_layer(), "0x0")
        self.refresh()

    def paste_as_new_layer_in_new_frame(self):
        self.tool_controller.paste(self.project.new_frame().new_layer(), "0x0")
        self.refresh()

    def new_layer_from_image_in_selected_frame(self):
        if (path := tkfiledialog.askopenfilename()):
            image = Image.open(path)
            layer = self.project.selected_frame.new_layer_from_image(image)
            self.refresh()

    def ask_delete_layer(self, frame, layer):
        if len(frame.layers) == 1:
            tkmessagebox.showwarning("Warning", "Cannot delete last layer.")
            return None
        return tkmessagebox.askyesno("Delete Layer?", f"Are you sure you wish to delete this layer?\n{layer.id}")

    def delete_selected_layer(self):
        frame = self.project.selected_frame
        layer = self.project.selected_frame.selected_layer
        if self.ask_delete_layer(frame, layer):
            frame.del_layer(layer)
            frame.selected_layer = frame.layers[0]
        self.refresh()

    def copy_selected_layer(self):
        self.project.selected_frame.copy_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def promote_selected_layer(self):
        self.project.selected_frame.promote_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def demote_selected_layer(self):
        self.project.selected_frame.demote_layer(self.project.selected_frame.selected_layer)
        self.refresh()

    def merge_selected_layer_down(self):
        self.project.selected_frame.merge_layer_down(self.project.selected_frame.selected_layer)
        self.refresh()

    def rename_selected_frame(self):
        frame = self.project.selected_frame
        if (name := tksimpledialog.askstring("Rename Frame", f"What would you like to rename Frame: {frame.id} to?")):
            frame.set_id(name)
            self.refresh()

    def rename_selected_layer(self):
        layer = self.project.selected_frame.selected_layer
        if (name := tksimpledialog.askstring("Rename Layer", f"What would you like to rename Layer: {layer.id} to?")):
            layer.set_id(name)
            self.refresh()

    def save_selected_frame(self):
        SaveMenu(self, self.project.selected_frame.export_composite_image())

    def ask_delete_frame(self):
        if len(self.project.frames) == 1:
            return tkmessagebox.showwarning("Warning", "Cannot delete last frame.")
        return tkmessagebox.askyesno("Delete", "Are you sure you wish to delete this frame?\nThis cannot be undone.")

    def delete_selected_frame(self):
        if self.ask_delete_frame():
            self.project.del_frame(self.project.selected_frame)
            self.project.selected_frame = self.project.frames[0]
            self.refresh()

    def copy_selected_frame(self):
        self.project.copy_frame(self.project.selected_frame)
        self.refresh()

    def promote_selected_frame(self):
        self.project.promote_frame(self.project.selected_frame)
        self.refresh()

    def demote_selected_frame(self):
        self.project.demote_frame(self.project.selected_frame)
        self.refresh()

    def new_layer_image_from_selection(self):
        if not self.project.selected_frame.selected_layer.selection: return
        image = self.tool_controller.new_layer_image_from_selection(self.project.selected_frame.selected_layer, self.tool_controller.start_selection, self.tool_controller.end_selection)
        self.project.selected_frame.new_layer_from_image(image)
        self.refresh()

    def exit(self):
        if tkmessagebox.askyesno("Exit?", f"Are you sure you wish to exit?\nAll unsaved work will be lost."):
            self.destroy()


class LoadedImageEditor(Editor):
    def __init__(self, *arg, **kwargs):
        Editor.__init__(self, *arg, **kwargs)

class App(sttk.App):
    def __init__(self):
        if not os.path.isfile("config.json"):
            temp = sttk.make_temp_config_file(DEFAULT_CONFIG)
        sttk.App.__init__(self, temp)
        Editor(self.window).pack(fill="both", expand=True)
        self.window.after_idle(lambda:sttk.tcl_center_window(self.window))

    def use_theme(self, theme: str = None, verbose: bool = False) -> str:
        """Updates the app to use a certain theme. `Returns the current theme as a String`"""
        super().use_theme(theme, verbose)
        widgets = sttk.complex_widget_search(self.window, (tk.PanedWindow, tk.Canvas))

        bg = self.style.lookup("TFrame", "background") or "#ffffff"

        for w in widgets.get(tk.PanedWindow, []):
            w.configure(bg=bg, handlesize=10, showhandle=True, sashwidth=4)

        for w in widgets.get(tk.Canvas, []):
            w.configure(bg="#ffffff")

        return theme

def main():
    print("Running py_simple_image_editor...")
    App().mainloop()
    sys.exit("Exited.")


if __name__ == "__main__":
    main()
