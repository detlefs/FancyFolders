import math
from typing import Optional

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBrush, QColor, QPaintEvent, QPainter, QPalette, QPen
from PySide6.QtWidgets import QLabel, QSizePolicy


class NonEditableLine(QLabel):
    """Represents a non-editable text field with background and
    placeholder text.
    """

    BACKGROUND_ALPHA = 20

    def __init__(self, placeholder_text: str) -> None:
        """Constructs a new non-editable text field

        :param placeholder_text: Light grey placeholder text when nothing is set
        """
        super().__init__()

        # Store a reference of placeholder to set when text is empty
        self.placeholderText = placeholder_text

        self.setMinimumHeight(20)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Minimum
        )

    def setText(self, text: Optional[str]) -> None:
        """Sets the text of the label, or clears if given None. When cleared
        the placeholder text is shown

        :param text: Text to display, or None
        :return:
        """
        super().setText(text if text is not None else self.placeholderText)

        palette = self.palette()
        self._set_text_colour(palette.color(
            QPalette.PlaceholderText if text is None else QPalette.Text))

    def _set_text_colour(self, colour: QColor) -> None:
        """Convenience method to set the colour of the displayed text

        :param colour: New text colour
        """
        palette = self.palette()
        palette.setColor(QPalette.WindowText, colour)
        self.setPalette(palette)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Overriden paint event to add a custom rounded rectangle background

        :param event: Paint event to pass through to superclass
        """
        width = self.size().width()
        height = self.size().height()
        corner_radius = math.floor(height / 2)

        max_rect = QRect(0, 0, width, height)

        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)

            # Subtle fill that works on both light and dark backgrounds
            background_colour = QColor(self.palette().color(QPalette.Text))
            background_colour.setAlpha(self.BACKGROUND_ALPHA)

            brush = QBrush(background_colour, Qt.SolidPattern)
            painter.setBrush(brush)
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(max_rect, corner_radius, corner_radius)

        # Call parent paint event to draw the text overtop the background
        super().paintEvent(event)
