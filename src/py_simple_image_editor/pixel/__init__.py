from .clipboard import ClipBoardClass
from .tool_controller import ToolController, TOOLCONST


shared_clipboard = ClipBoardClass()
tool_controller = ToolController(shared_clipboard)
