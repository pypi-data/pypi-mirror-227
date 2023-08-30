from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
from .gui.WelcomeDialog import WelcomeDialog
from PyQt6.QtWidgets import QApplication
from .gui.MainWindow import MainWindow
from .Environment import Environment
import sys
import os


def main() -> None:
    app = QApplication(sys.argv)

    env = Environment()

    app.setWindowIcon(env.logo)
    app.setApplicationVersion(env.version)
    app.setApplicationName("jdDBusDebugger")
    app.setDesktopFileName("page.codeberg.JakobDev.jdDBusDebugger")

    if env.settings.get("language") == "default":
        current_locale = QLocale.system()
    else:
        current_locale = QLocale(env.settings.get("language"))

    app_translator = QTranslator()
    if app_translator.load(current_locale, "jdDBusDebugger", "_", os.path.join(env.program_dir, "translations")):
        app.installTranslator(app_translator)

    qt_translator = QTranslator()
    if qt_translator.load(current_locale, "qt", "_", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
        app.installTranslator(qt_translator)

    w = MainWindow(env)
    w.show()

    if env.settings.get("showWelcomeDialogStartup"):
        WelcomeDialog(env).open_dialog()

    sys.exit(app.exec())
