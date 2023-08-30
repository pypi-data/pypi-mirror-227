from PyQt6.QtWidgets import QDialog, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout
from .SingleValueInputDialog import SingleValueInputDialog
from PyQt6.QtCore import QCoreApplication
from ...types.DBusValue import DBusValue
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ...types.DBusType import DBusType


class ArrayInputDialog(QDialog):
    def __init__(self, dbus_type: "DBusType") -> None:
        super().__init__()

        self._dbus_type = dbus_type
        self._array_content: list[DBusValue] = []

        self._array_list = QListWidget()
        add_button = QPushButton(QCoreApplication.translate("ArrayInput", "Add"))
        remove_button = QPushButton(QCoreApplication.translate("ArrayInput", "Remove"))
        ok_button = QPushButton(QCoreApplication.translate("ArrayInput", "OK"))

        add_button.clicked.connect(self._add_button_clicked)
        ok_button.clicked.connect(self.close)

        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(add_button)
        add_remove_layout.addWidget(remove_button)

        ok_layout = QHBoxLayout()
        ok_layout.addStretch(1)
        ok_layout.addWidget(ok_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._array_list)
        main_layout.addLayout(add_remove_layout)
        main_layout.addLayout(ok_layout)

        self.setLayout(main_layout)
        self.setWindowTitle(QCoreApplication.translate("ArrayInput", "Edit Array"))

    def _update_list_widget(self) -> None:
        self._array_list.clear()
        for value in self._array_content:
            self._array_list.addItem(value.get_printable_text())

    def _add_button_clicked(self) -> None:
        value, ok = SingleValueInputDialog(self, self._dbus_type).open_input_dialog()

        if not ok:
            return

        self._array_content.append(value)
        self._update_list_widget()

    def get_array(self) -> list[DBusValue]:
        return self._array_content


class EditArrayButton(QPushButton):
    def __init__(self, dbus_type: "DBusType") -> None:
        super().__init__(QCoreApplication.translate("ArrayInput", "Edit Array"))

        self._dbus_type = dbus_type
        self._array_input_dialog = ArrayInputDialog(dbus_type.array_type)

        self.clicked.connect(lambda: self._array_input_dialog.exec())

    def get_array(self) -> DBusValue:
        return DBusValue.create(self._dbus_type, self._array_input_dialog.get_array())
