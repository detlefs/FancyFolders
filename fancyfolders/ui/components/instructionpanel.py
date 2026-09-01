import math

from PySide6.QtCore import QPoint, QRect, QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPaintEvent, QPainter, QPalette, QPen
from PySide6.QtWidgets import QLayout, QVBoxLayout, QWidget

from fancyfolders.ui.components.customlabel import CustomLabel


class InstructionPanel(QWidget):
    """Represents a panel containing a layout with a custom background and
    index number
    """

    CIRCLE_RADIUS = 11
    CORNER_RADIUS = 10
    SPACING = 6

    def __init__(self, index: int, colour: tuple[int, int, int],
                 title: str = None, extra_spacing=False) -> None:
        """Constructs a new InstructionPanel with the given index number, colour,
        and layout object containing children elements to hold within the panel

        :param index: Number to show in circle on the left
        :param colour: Accent colour of the step badge (r, g, b)
        :param title: Optional title of the panel
        :param extra_spacing: Should there be extra spacing on bottom?
        """
        super().__init__()

        self.index = index
        self.colour = colour

        # Wrapping layout to add title if desired
        self.wrap_layout = QVBoxLayout()
        self.wrap_layout.setContentsMargins(
            self.SPACING * 2,
            math.floor(self.SPACING * 1.5),
            self.SPACING * 2,
            math.floor(self.SPACING * (1.8 if extra_spacing else 1.5)))
        self.wrap_layout.setSpacing(0)

        if title is not None:
            self.wrap_layout.addWidget(CustomLabel(title))
            self.wrap_layout.addSpacing(math.floor(self.SPACING * 1.2))

        self.setLayout(self.wrap_layout)

        # Ensure child elements are not overlapping the circle on the left
        self.setContentsMargins(math.floor(self.CIRCLE_RADIUS * 2), 0, 0, 0)

    def addLayout(self, layout: QLayout) -> None:
        """Passthrough method to add a layout to the container

        :param layout: Child layout to add
        """
        self.wrap_layout.addLayout(layout)

    def paintEvent(self, _: QPaintEvent) -> None:
        """Override paint event to draw the panel as a grouped content box
        with a coloured step badge on its left edge

        :param _: Unused paint event object
        """
        width = self.size().width()
        height = self.size().height()

        max_rect = QRect(0, 0, width, height)
        inset_rect = max_rect.adjusted(self.CIRCLE_RADIUS + 2, 1, -1, -1)
        circle_bounds = QRect(QPoint(2, math.floor(height / 2) - self.CIRCLE_RADIUS),
                              QSize(self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2))

        palette = self.palette()
        # Hairline separator, subtle in both light and dark appearance
        border_colour = QColor(palette.color(QPalette.Text))
        border_colour.setAlpha(30)

        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)

            # Grouped content box, one hairline inset to keep the stroke crisp
            painter.setBrush(QBrush(palette.color(QPalette.Base), Qt.SolidPattern))
            painter.setPen(QPen(border_colour, 1))
            painter.drawRoundedRect(
                QRectF(inset_rect).adjusted(0.5, 0.5, -0.5, -0.5),
                self.CORNER_RADIUS, self.CORNER_RADIUS)

            # Filled accent badge on the left edge of the box
            painter.setPen(QPen(Qt.NoPen))
            painter.setBrush(QBrush(QColor.fromRgb(*self.colour), Qt.SolidPattern))
            painter.drawEllipse(circle_bounds)

            # Index number in the center of the badge
            font = QFont()
            font.setStyleHint(QFont.SansSerif)
            font.setBold(True)
            font.setPointSize(math.floor(self.CIRCLE_RADIUS * 1.1))
            painter.setFont(font)
            painter.setPen(QPen(Qt.white))
            painter.drawText(circle_bounds, Qt.AlignHCenter |
                             Qt.AlignVCenter, str(self.index))
