import logging
import pathlib
from typing import Any

import keyring
from PyQt6.QtCore import QSettings, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QWidget,
)

from ixontray.types.api import Agent
from ixontray.types.common import Command, Commands

logger = logging.getLogger("IXON_TRAY_SETTINGS")


class GeneralTab(QWidget):
    auto_start_path = pathlib.Path("~/.config/autostart/ixontray.desktop").expanduser()
    save_btn_clicked = pyqtSignal()

    def __init__(self, settings: QSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings

        self.cb_enable_autostart = QCheckBox("Enable auto start")
        self.cb_enable_autostart.stateChanged.connect(self.set_auto_start)
        self.cb_enable_autostart.setChecked(self.auto_start_path.exists())
        self.le_organization_id = QLineEdit()

        username, password = self.get_auth()
        self.le_email = QLineEdit(username)
        self.le_password = QLineEdit(password)
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.ch_2fa = QCheckBox()
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_auth)

        self._layout = QFormLayout()
        self._layout.addRow("Auto start application", self.cb_enable_autostart)
        # self._layout.addRow("Organization ID", self.le_organization_id)
        # self._layout.addRow("Application ID", self.le_application_id)

        self._layout.addRow("Email", self.le_email)
        self._layout.addRow("Password", self.le_password)
        self._layout.addRow("2fa require", self.ch_2fa)
        self._layout.addRow("", self.btn_save)

        self.setLayout(self._layout)

    def save_auth(self) -> None:
        """Store user name and password."""
        logging.info("Saved the login details.")
        username = self.le_email.text()
        password = self.le_password.text()
        self._settings.setValue("email", username)
        keyring.set_password("Ixontray", username, password)
        self.save_btn_clicked.emit()

    def get_auth(self) -> tuple[str, str]:
        """Returns user name and password."""
        username = self._settings.value("email", "")
        password = keyring.get_password("Ixontray", username)
        return username, password

    def set_auto_start(self, enabled: bool) -> None:
        if not enabled:
            self.auto_start_path.unlink(missing_ok=True)
            logger.info(f"Removed {self.auto_start_path}")
        else:
            template = """[Desktop Entry]
Type=Application
Exec=ixontray
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=ixontray
Name=ixontray
Comment[en_US]=ixontray
Comment=ixontray"""
            self.auto_start_path.write_text(template)
            logger.info(f"Created {self.auto_start_path}")


class CommandItem(QListWidgetItem):
    def __init__(self, command: Command, *args: Any, **kwargs: Any) -> None:
        super().__init__(command.name, *args, **kwargs)
        self._command = command

    def get_command(self) -> Command:
        return self._command

    def set_command(self, command: Command) -> None:
        self._command = command


class CommandsTab(QWidget):
    commands_updated = pyqtSignal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.commands_layout = QGridLayout()
        self.setLayout(self.commands_layout)

        row = 0
        # Commands
        self.commands_layout.addWidget(QLabel("Commands"), row, 0, 1, 1)
        row += 1
        self.lw_commands = QListWidget()
        self.lw_commands.currentItemChanged.connect(self.set_selected_command)
        self.commands_layout.addWidget(self.lw_commands, row, 0, 9, 1)

        # Edit _commands
        self.le_name = QLineEdit()
        self.commands_layout.addWidget(self.le_name, row, 1, 1, 2)
        row += 1
        self.le_cmd = QTextEdit()
        self.commands_layout.addWidget(self.le_cmd, row, 1, 1, 2)
        row += 1
        self.le_icon = QLineEdit()
        self.commands_layout.addWidget(self.le_icon, row, 1, 1, 1)
        #
        self.lbl_icon = QLabel("")
        self.commands_layout.addWidget(self.lbl_icon, row, 2, 1, 1)
        self.le_icon.textChanged.connect(self.set_icon)

        row += 1
        self.commands_layout.addWidget(
            QLabel(
                (
                    "See: "
                    "<a href=https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html> "
                    "icon specs</a>"
                ),
            ),
            row,
            1,
            1,
            2,
        )
        row += 1

        self.le_shortcut = QLineEdit()
        self.commands_layout.addWidget(self.le_shortcut, row, 1, 1, 2)
        row += 1

        self.cb_showin_connected = QCheckBox("Show in connected menu")
        self.commands_layout.addWidget(self.cb_showin_connected, row, 1, 1, 2)
        row += 1
        self.cb_showin_item = QCheckBox("Show in item menu")
        self.commands_layout.addWidget(self.cb_showin_item, row, 1, 1, 2)
        row += 1

        self.cb_showin_global = QCheckBox("Show in global menu")
        self.commands_layout.addWidget(self.cb_showin_global, row, 1, 1, 2)
        row += 1

        self.cb_force_connection = QCheckBox("Force Connection")
        self.commands_layout.addWidget(self.cb_force_connection, row, 1, 1, 2)
        row += 1

        row += 1
        self.btn_add_new = QPushButton("New")
        self.btn_add_new.clicked.connect(self.add_new_command)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_command)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.del_command)

        self.commands_layout.addWidget(self.btn_add_new, row, 0, 1, 1)
        self.commands_layout.addWidget(self.btn_delete, row, 1, 1, 1)
        self.commands_layout.addWidget(self.btn_save, row, 2, 1, 1)
        row += 1

    def add_new_command(self) -> None:
        cmd = Command(name="New Command", cmd="", icon="", shortcut="", force_connection=False, show_in=[])
        command_item = CommandItem(command=cmd)
        self.lw_commands.addItem(command_item)
        self.lw_commands.setCurrentItem(command_item)
        self.show_command(command=cmd)

    def show_command(
        self,
        command: Command,
    ) -> None:
        self.le_name.setText(command.name)
        self.le_cmd.setText(command.cmd)
        self.le_icon.setText(command.icon)
        self.lbl_icon.setPixmap(QIcon.fromTheme(command.icon).pixmap(QSize(16, 16)))
        self.le_shortcut.setText(command.shortcut)
        self.cb_showin_connected.setChecked("connected" in command.show_in)
        self.cb_showin_item.setChecked("item" in command.show_in)
        self.cb_showin_global.setChecked("global" in command.show_in)
        self.cb_force_connection.setChecked(command.force_connection)

    def save_command(self) -> None:
        show_in = []
        # SHow in
        if self.cb_showin_connected.isChecked():
            show_in.append("connected")
        if self.cb_showin_item.isChecked():
            show_in.append("item")
        if self.cb_showin_global.isChecked():
            show_in.append("global")
        command = Command(
            name=self.le_name.text(),
            cmd=self.le_cmd.toPlainText(),
            icon=self.le_icon.text(),
            shortcut=self.le_shortcut.text(),
            show_in=show_in,
            force_connection=self.cb_force_connection.isChecked(),
        )
        self.lw_commands.currentItem().set_command(command=command)
        self.commands_updated.emit(self.get_commands())

    def set_icon(self, _: str) -> None:
        self.lbl_icon.setPixmap(QIcon.fromTheme(self.le_icon.text()).pixmap(QSize(16, 16)))

    def set_selected_command(self) -> None:
        selected_cmd = self.lw_commands.currentItem().get_command()
        self.show_command(selected_cmd)

    def del_command(self) -> None:
        self.lw_commands.takeItem(self.lw_commands.currentIndex().row())

    def set_commands(self, commands: Commands) -> None:
        current_index = self.lw_commands.currentIndex()

        self.lw_commands.clear()
        commands.commands.sort(key=lambda cmd: cmd.name)

        for cmd in commands.commands:
            self.lw_commands.addItem(CommandItem(command=cmd))

        self.lw_commands.setCurrentIndex(current_index)

    def get_commands(self) -> Commands:
        return Commands(
            commands=[ci.get_command() for ci in self.lw_commands.findItems("*", Qt.MatchFlag.MatchWildcard)],
        )


class ClientsTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._all_agents: dict[str, Agent] = {}

        self.clients_layout = QGridLayout()
        self.setLayout(self.clients_layout)
        row = 0
        # Clients
        self.le_search_clients = QLineEdit()
        self.le_search_clients.textChanged.connect(self.search_clients)

        self.lw_selected_clients = QListWidget()
        self.lw_selected_clients.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lw_selected_clients.mouseDoubleClickEvent = lambda _: self.remove_from_selected_clients()

        self.lw_all_clients = QListWidget()
        self.lw_all_clients.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lw_all_clients.mouseDoubleClickEvent = lambda _: self.add_to_selected_clients()

        self.btn_move_left = QPushButton("<")
        self.btn_move_left.clicked.connect(self.remove_from_selected_clients)

        self.btn_move_right = QPushButton(">")
        self.btn_move_right.clicked.connect(self.add_to_selected_clients)

        self.lbl_all_clients = QLabel("All clients")
        self.lbl_all_clients.setMaximumHeight(50)
        self.lbl_fav_clients = QLabel("Favourite clients")

        self.clients_layout.addWidget(self.lbl_all_clients, row, 0, 1, 1)
        self.clients_layout.addWidget(self.lbl_fav_clients, row, 2, 1, 1)
        row += 1

        self.clients_layout.addWidget(
            self.le_search_clients,
            row,
            0,
            1,
            3,
        )
        row += 1
        #
        self.clients_layout.addWidget(
            self.lw_all_clients,
            row,
            0,
            3,
            1,
        )
        self.clients_layout.addWidget(
            self.btn_move_right,
            row,
            1,
            1,
            1,
        )
        self.clients_layout.addWidget(
            self.lw_selected_clients,
            row,
            2,
            3,
            1,
        )
        row += 1
        self.clients_layout.addWidget(
            self.btn_move_left,
            row,
            1,
            1,
            1,
        )
        row += 1

    def search_clients(self) -> None:
        search_text = self.le_search_clients.text()
        matched_items = self.lw_all_clients.findItems(search_text, Qt.MatchFlag.MatchContains)
        for i in range(self.lw_all_clients.count()):
            it = self.lw_all_clients.item(i)
            it.setHidden(it not in matched_items)
        if matched_items:
            self.lw_all_clients.setCurrentItem(matched_items[0])

    def set_all_clients(
        self,
        clients: dict[str, Agent],
        favourites: dict[str, Agent],
    ) -> None:
        self._all_agents = clients
        self.lw_all_clients.clear()
        self.lw_selected_clients.clear()
        for _id, data in clients.items():
            self.lw_all_clients.addItem(data.full_name)
        for _id, data in favourites.items():
            self.lw_selected_clients.addItem(data.full_name)

        self.inverted_mapping = {v.full_name: k for k, v in self._all_agents.items()}

    def add_to_selected_clients(self) -> None:
        for item in self.lw_all_clients.selectedItems():
            if len(self.lw_selected_clients.findItems(item.text(), Qt.MatchFlag.MatchExactly)) == 0:
                self.lw_selected_clients.addItem(item.text())
        self.lw_all_clients.clearSelection()

    def get_favourite_ixon_ids(self) -> dict[str, str]:
        return {
            self.inverted_mapping[i.text()]: i.text()
            for i in self.lw_selected_clients.findItems("*", Qt.MatchFlag.MatchWildcard)
        }

    def remove_from_selected_clients(self) -> None:
        selected_items = []
        all_items = [i.text() for i in self.lw_selected_clients.findItems("*", Qt.MatchFlag.MatchWildcard)]
        for item in self.lw_selected_clients.selectedItems():
            selected_items.append(item.text())
        self.lw_selected_clients.clear()
        for item in all_items:
            if item not in selected_items:
                self.lw_selected_clients.addItem(item)


class SettingsWindow(QTabWidget):
    def __init__(self, settings: QSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        # Setup tabs
        self.general_tab = GeneralTab(settings=settings, parent=self)
        self.general_tab.save_btn_clicked.connect(self.close)
        self.clients_tab = ClientsTab(parent=self)
        self.commands_tab = CommandsTab(parent=self)

        # General tab
        self.addTab(self.general_tab, "General")

        # Clients tab
        self.addTab(self.clients_tab, "Clients")

        # Commands tab
        self.addTab(self.commands_tab, "Commands")

        self.setCurrentWidget(self.clients_tab)
