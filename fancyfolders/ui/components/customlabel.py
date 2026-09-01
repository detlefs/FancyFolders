from typing import Optional

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QLabel


class CustomLabel(QLabel):
    """Represents a label with a custom colour and boldness state, defaults to
    the system label colour and bold.
    """

    def __init__(self, text: str, colour: Optional[QColor] = None,
                 is_bold: bool = True):
        """Constructs a new custom label

        :param text: Label text
        :param colour: Label colour, None to keep the system label colour
        :param is_bold: Is the font bold?
        """
        super().__init__(text)

        font = self.font()
        font.setBold(is_bold)
        self.setFont(font)

        if colour is not None:
            palette = self.palette()
            palette.setColor(QPalette.WindowText, colour)
            self.setPalette(palette)
