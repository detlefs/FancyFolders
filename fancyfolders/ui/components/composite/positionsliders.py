from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSlider, QWidget

from fancyfolders.constants import (
    ICON_OFFSET_SLIDER_MAX, MAXIMUM_ICON_OFFSET_LIMIT,
    MAXIMUM_ICON_OFFSET_VALUE)
from fancyfolders.utilities import interpolate_int_to_float_with_midpoint

MIDDLE_TICK = int((ICON_OFFSET_SLIDER_MAX - 1) / 2) + 1


def _offset_slider(orientation: Qt.Orientation) -> QSlider:
    slider = QSlider(orientation)
    slider.setMinimum(1)
    slider.setMaximum(ICON_OFFSET_SLIDER_MAX)
    slider.setValue(MIDDLE_TICK)
    slider.setTracking(True)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setTickInterval(ICON_OFFSET_SLIDER_MAX + 1)
    return slider


class PositionSliders(QGridLayout):
    """Wraps the folder preview with icon position sliders: horizontal below
    the preview, vertical to its right
    """

    def __init__(self, preview: QWidget, on_change: Callable[[], None]) -> None:
        super().__init__()

        self.horizontal_slider = _offset_slider(Qt.Horizontal)
        self.vertical_slider = _offset_slider(Qt.Vertical)

        self.addWidget(preview, 0, 0)
        self.addWidget(self.vertical_slider, 0, 1)
        self.addWidget(self.horizontal_slider, 1, 0)

        for slider in (self.horizontal_slider, self.vertical_slider):
            slider.valueChanged.connect(lambda _: on_change())

    def get_offset(self, icon_scale: float = 1.0) -> tuple[float, float]:
        """Gets the selected icon position as an offset from the center, in
        percentages of the folder size. A smaller icon has more room to move,
        so the slider range grows as the icon scale shrinks

        :param icon_scale: The icon scale the offset applies to
        :return: The icon offset: x, y
        """
        def offset(slider: QSlider, axis: int) -> float:
            maximum = min(MAXIMUM_ICON_OFFSET_VALUE[axis] / icon_scale,
                          MAXIMUM_ICON_OFFSET_LIMIT[axis])
            return interpolate_int_to_float_with_midpoint(
                slider.value(), 1, ICON_OFFSET_SLIDER_MAX,
                -maximum, 0.0, maximum)

        # Vertical sliders count upwards from the bottom, but a positive
        # offset moves the icon down
        return offset(self.horizontal_slider, 0), -offset(self.vertical_slider, 1)

    def reset(self) -> None:
        self.horizontal_slider.setValue(MIDDLE_TICK)
        self.vertical_slider.setValue(MIDDLE_TICK)
