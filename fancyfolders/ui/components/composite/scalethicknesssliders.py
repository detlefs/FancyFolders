from typing import Callable

from PySide6.QtWidgets import QHBoxLayout

from fancyfolders.constants import (
    DEFAULT_FONT, ICON_SCALE_SLIDER_MAX, MAXIMUM_ICON_SCALE_VALUE,
    MINIMUM_ICON_SCALE_VALUE, SFFont)
from fancyfolders.ui.components.horizontalslider import HorizontalSlider, TickStyle
from fancyfolders.utilities import interpolate_int_to_float_with_midpoint


def _centered_slider(label: str, total_num_ticks: int) -> HorizontalSlider:
    """Constructs a slider whose neutral value is its middle tick"""
    return HorizontalSlider(
        label=label, total_num_ticks=total_num_ticks,
        initial_value=_middle_tick(total_num_ticks), tick_style=TickStyle.CENTER)


def _middle_tick(total_num_ticks: int) -> int:
    return int((total_num_ticks - 1) / 2) + 1


class ScaleThicknessSliders(QHBoxLayout):
    """Represents a group of user input sliders to obtain icon scale and
    thickness
    """

    def __init__(self, on_change: Callable[[], None]) -> None:
        """Constructs a new widget containing scale and thickness sliders

        :param on_change: Callback to run whenever a change is made
        """
        super().__init__()

        # Icon scale slider
        self.scale_slider = _centered_slider("Scale", ICON_SCALE_SLIDER_MAX)

        # Thickness slider
        self.thickness_slider = HorizontalSlider(
            label="Thickness", total_num_ticks=len(SFFont),
            initial_value=DEFAULT_FONT.value, tick_style=TickStyle.EACH)

        for slider in (self.scale_slider, self.thickness_slider):
            slider.slider.valueChanged.connect(lambda _: on_change())
            self.addLayout(slider)

    def get_scale(self) -> float:
        """Gets the selected icon scale, normalized to predetermined range

        :return: The icon scale
        """
        return interpolate_int_to_float_with_midpoint(
            self.scale_slider.slider.value(), 1, ICON_SCALE_SLIDER_MAX,
            MINIMUM_ICON_SCALE_VALUE, 1.0, MAXIMUM_ICON_SCALE_VALUE)

    def get_thickness(self) -> SFFont:
        """Gets the selected thickness

        :return: Enum representing font thickness
        """
        return SFFont(self.thickness_slider.slider.value())

    def reset(self) -> None:
        self.scale_slider.setValue(_middle_tick(ICON_SCALE_SLIDER_MAX))
        self.thickness_slider.setValue(DEFAULT_FONT.value)
