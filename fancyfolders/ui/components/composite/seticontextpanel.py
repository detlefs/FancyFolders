from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLineEdit

from fancyfolders.constants import PANEL1_COLOUR, SFFont
from fancyfolders.ui.components.customlabel import CustomLabel
from fancyfolders.ui.components.instructionpanel import InstructionPanel
from fancyfolders.utilities import get_internal_font_location


class SetIconTextPanel(InstructionPanel):
    """Represents the 1st instruction panel, containing user input to set
    icon text
    """

    def __init__(self, on_change: Callable[[], None],
                 on_colour_mode_change: Callable[[], None]) -> None:
        """Constructs a new text instruction panel

        :param on_change: Callback to run whenever the text is edited
        :param on_colour_mode_change: Callback to run whenever the original
            colours checkbox is toggled
        """
        super().__init__(1, PANEL1_COLOUR,
                         "Set folder icon",
                         extra_spacing=True)

        self.on_change = on_change

        # Text icon input
        self.icon_text_input = QLineEdit()

        # Custom font to support symbols
        font_filepath = get_internal_font_location(SFFont.regular.filename())
        font_id = QFontDatabase.addApplicationFont(font_filepath)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = self.icon_text_input.font()
        font.setFamily(font_family)
        self.icon_text_input.setFont(font)

        self.icon_text_input.setMaxLength(25)
        self.icon_text_input.setPlaceholderText("Icon text")
        self.icon_text_input.setAlignment(Qt.AlignCenter)
        self.icon_text_input.textChanged.connect(lambda _: on_change())

        container = QHBoxLayout()
        container.addWidget(CustomLabel(
            "Drag SF Symbol / image above, or type text or emoji(s):",
            is_bold=False))
        container.addSpacing(5)
        container.addWidget(self.icon_text_input)

        # Keep the dragged image in its own colours instead of engraving it
        self.original_colours_checkbox = QCheckBox("Keep original image colours")
        self.original_colours_checkbox.toggled.connect(
            lambda _: on_colour_mode_change())

        checkbox_container = QHBoxLayout()
        checkbox_container.addWidget(self.original_colours_checkbox)
        checkbox_container.addStretch()

        # Add main container to instruction panel
        self.addLayout(container)
        self.addLayout(checkbox_container)

    def get_icon_text(self) -> str:
        return self.icon_text_input.text()

    def set_icon_text(self, text: str) -> None:
        self.icon_text_input.setText(text)
        self.on_change()

    def clear_icon_text(self) -> None:
        """Empties the text field without regenerating the icon, the caller
        updates the folder icon itself
        """
        self.icon_text_input.blockSignals(True)
        self.icon_text_input.setText("")
        self.icon_text_input.blockSignals(False)

    def set_colour_mode_enabled(self, enabled: bool) -> None:
        """Enables the original colours checkbox, which only has an effect on
        a dragged image. Its state is kept so that it applies again once an
        image is dropped

        :param enabled: Whether the checkbox can be used
        """
        self.original_colours_checkbox.setEnabled(enabled)

    def keep_original_image_colours(self) -> bool:
        return self.original_colours_checkbox.isChecked()

    def set_keep_original_image_colours(self, keep: bool) -> None:
        """Sets the checkbox without regenerating the icon, the caller updates
        the folder icon itself

        :param keep: Whether to keep the original colours
        """
        self.original_colours_checkbox.blockSignals(True)
        self.original_colours_checkbox.setChecked(keep)
        self.original_colours_checkbox.blockSignals(False)

    def reset(self) -> None:
        self.icon_text_input.setText("")
        self.original_colours_checkbox.setChecked(False)
