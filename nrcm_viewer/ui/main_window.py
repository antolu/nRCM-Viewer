import logging
from os import path

from PyQt5.QtWidgets import QMainWindow, QFileDialog

from .main_widget import MainWidget
from ..data import WorkspaceReader, ZipReader
from ..generated.main_window_ui import Ui_MainWindow
from ..settings import app

log = logging.getLogger(__name__)


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionLoad_zip.triggered.connect(self.load_zip)
        self.actionLoad_Workspace.triggered.connect(self.load_workspace)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

    def load_zip(self):
        zip_file, ok = QFileDialog.getOpenFileName(
            self, 'Select .zip file', app.current_dir, '*.zip')

        if not ok or zip_file is None or zip_file == '':
            log.debug('No .zip file selected.')
            return

        app.current_dir = zip_file
        new_widget = MainWidget(ZipReader(zip_file), self.tabWidget)
        filename = path.split(zip_file)[-1]

        self.tabWidget.addTab(new_widget, filename)
        self.tabWidget.setCurrentWidget(new_widget)

    def load_workspace(self):
        workspace_path = QFileDialog.getExistingDirectory(
            self, 'Select workspace', app.current_dir)

        if workspace_path is None or workspace_path == '':
            log.debug(f'No workspace selected.')
            return

        app.current_dir = workspace_path

        new_widget = MainWidget(WorkspaceReader(workspace_path),
                                self.tabWidget)

        self.tabWidget.addTab(new_widget, path.split(workspace_path)[-1])
        self.tabWidget.setCurrentWidget(new_widget)

    def close_tab(self, index: int):
        self.tabWidget.removeTab(index)

    def update_menu_state(self):
        pass
