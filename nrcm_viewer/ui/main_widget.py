import logging
from typing import Optional

from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex
from PyQt5.QtWidgets import QWidget

from .table_model import TableModel, CopySelectedCellsAction
from ..data import ZipReader, Reader, WorkspaceReader
from ..generated.main_widget_ui import Ui_MainWidget

log = logging.getLogger(__name__)


class MainWidget(Ui_MainWidget, QWidget):
    def __init__(self, reader: Reader, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        self._reader = reader
        self._table_model = TableModel(parent=self)

        proxy_model = QSortFilterProxyModel(self)
        proxy_model.setSourceModel(self._table_model)
        self.table.setModel(self._table_model)

        self.table.activated.connect(self.show_img)
        self.copy_action = CopySelectedCellsAction(self.table)

        self._table_model.samples = self._reader.samples

    def show_current_img(self):
        raise NotImplementedError

    def show_img(self, index: QModelIndex):
        sample = self._table_model.get_sample(index.row())

        self.widget.show_image(sample, self._reader)
