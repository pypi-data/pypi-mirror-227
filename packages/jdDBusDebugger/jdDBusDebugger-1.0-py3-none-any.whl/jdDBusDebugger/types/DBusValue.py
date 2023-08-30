from PyQt6.QtDBus import QDBusVariant, QDBusArgument
from .DBusType import DBusTypeEnum, DBusType
from typing import Any


class DBusValue:
    def __init__(self) -> None:
        self.dbus_type = DBusType()
        self.value: Any = None

    @classmethod
    def create(cls: type["DBusValue"], dbus_type: DBusType, value: Any) -> "DBusValue":
        dbus_value = cls()

        dbus_value.dbus_type = dbus_type
        dbus_value.value = value

        return dbus_value

    @classmethod
    def from_json_data(obj, json_data: dict[str, Any]) -> "DBusValue":
        dbus_value = obj()

        dbus_value.dbus_type= DBusType.from_json_data(json_data["type"])

        match dbus_value.dbus_type.type_const:
            case DBusTypeEnum.DICT:
                dbus_value.value = {}
                for key, value in json_data["value"].items():
                    dbus_value.value[key] = obj.from_json_data(value)
            case _:
                dbus_value.value = json_data["value"]

        return dbus_value

    def get_json_data(self) -> dict[str, Any]:
        match self.dbus_type.type_const:
            case DBusTypeEnum.DICT:
                json_value = {}
                for key, value in self.value.items():
                    json_value[key] = value.get_json_data()
            case _:
                json_value = self.value

        return {
            "type": self.dbus_type.get_json_data(),
            "value": json_value
        }

    def get_value(self) -> Any:
        if self.dbus_type.is_simple_type():
            arg = QDBusArgument()
            arg.add(self.value, self.dbus_type.get_qmeta_type().id())
            return arg

        match self.dbus_type.type_const:
            case DBusTypeEnum.VARIANT:
                return QDBusVariant(self.value)
            case DBusTypeEnum.ARRAY:
                arg = QDBusArgument()
                arg.beginArray(self.dbus_type.array_type.get_qmeta_type())
                for value in self.value:
                    arg.add(value.get_value())
                arg.endArray()
                return arg
            case DBusTypeEnum.DICT:
                return_dict = {}
                for key, value in self.value.items():
                    return_dict[key] = value.get_value()
                return return_dict

    def get_printable_text(self) -> str:
        return str(self.value)
