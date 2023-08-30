from PyQt6.QtWidgets import QWidget, QSpinBox, QComboBox, QLineEdit, QLabel
from ...Constants import SPIN_BOX_MINIMUM, SPIN_BOX_MAXIMUM
from ...types.DBusType import DBusTypeEnum, DBusType
from ...types.DBusValue import DBusValue


class InputHandler:
    def __init__(self) -> None:
        from .VariantEdit import VariantEdit
        self._variant_edit = VariantEdit

        from .ArrayInput import EditArrayButton
        self._array_button = EditArrayButton

        from .DictInput import EditDictButton
        self._dict_button = EditDictButton

    def generate_widget_for_type(self, dbus_type: DBusType) -> QWidget:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                spin_box = QSpinBox()
                spin_box.setMinimum(SPIN_BOX_MINIMUM)
                spin_box.setMaximum(SPIN_BOX_MAXIMUM)
                return spin_box
            case DBusTypeEnum.BOOLEAN:
                boolean_box = QComboBox()
                boolean_box.setCurrentIndex
                boolean_box.addItem("True", True)
                boolean_box.addItem("False", False)
                return boolean_box
            case DBusTypeEnum.STRING:
                return QLineEdit()
            case DBusTypeEnum.VARIANT:
                return self._variant_edit()
            case DBusTypeEnum.ARRAY:
                return self._array_button(dbus_type)
            case DBusTypeEnum.DICT:
                return self._dict_button()
            case _:
                return QLabel("Unsupported type")

    def set_widget_value(self, widget: QWidget, dbus_type: DBusType, value: DBusValue) -> None:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                widget.setValue(value.value)
            case DBusTypeEnum.BOOLEAN:
                if value.value is True:
                    widget.setCurrentIndex(0)
                elif value.value is False:
                    widget.setCurrentIndex(1)
            case DBusTypeEnum.STRING:
                widget.setText(value.value)

    def get_value_from_widget(self, widget: QWidget, dbus_type: DBusType) -> DBusValue:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                return DBusValue.create(dbus_type, widget.value())
            case DBusTypeEnum.BOOLEAN:
                return DBusValue.create(dbus_type, widget.currentData())
            case DBusTypeEnum.STRING:
                return DBusValue.create(dbus_type, widget.text())
            case DBusTypeEnum.VARIANT:
                return widget.get_value()
            case DBusTypeEnum.ARRAY:
                return widget.get_array()
            case DBusTypeEnum.DICT:
                return DBusValue.create(dbus_type, widget.get_dict())
            case _:
                raise NotImplementedError()
