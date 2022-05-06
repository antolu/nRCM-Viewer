import logging
from typing import Optional, Any, List

from PyQt5.QtCore import QAbstractTableModel, QObject, QModelIndex, Qt
from PyQt5.QtWidgets import QAction, QTableView, QApplication

from ..data import Sample

log = logging.getLogger(__name__)

HEADER = ['Timestamp', 'Channel ID']
HEADER_TO_ATTR = {
    'Timestamp': 'timestamp',
    'Channel ID': 'channel_id'
}


class TableModel(QAbstractTableModel):
    def __init__(self, data: Optional[List[Sample]] = None,
                 parent: Optional[QObject] = None):
        super().__init__(parent)

        if data is None:
            data = list()

        self.samples = data

    @property
    def samples(self) -> List[Sample]:
        return self._data

    @samples.setter
    def samples(self, new: List[Sample]):
        self._data = new.copy()

        self.modelReset.emit()

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return getattr(self._data[index.row()],
                           HEADER_TO_ATTR[HEADER[index.column()]])

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(HEADER) if len(self._data) > 0 else 0

    def headerData(self, section: int,
                   orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return HEADER[section]
            elif orientation == Qt.Vertical:
                return f'{section}'

    def get_sample(self, row: int) -> Sample:
        return self._data[row]


class CopySelectedCellsAction(QAction):
    def __init__(self, table_widget):
        if not isinstance(table_widget, QTableView):
            raise ValueError(
                f'CopySelectedCellsAction must be initialised with a QTableView. A {type(table_widget)} was given.')
        super().__init__("Copy", table_widget)
        self.setShortcut('Ctrl+C')
        self.triggered.connect(self.copy_cells_to_clipboard)
        self.table = table_widget

    def copy_cells_to_clipboard(self):
        if len(self.table.selectionModel().selectedIndexes()) > 0:
            # sort select indexes into rows and columns
            previous = self.table.selectionModel().selectedIndexes()[0]
            columns = []
            rows = []
            for index in self.table.selectionModel().selectedIndexes():
                if previous.column() != index.column():
                    columns.append(rows)
                    rows = []
                rows.append(index.data())
                previous = index
            columns.append(rows)

            # add rows and columns to clipboard
            clipboard = ""
            nrows = len(columns[0])
            ncols = len(columns)
            for r in range(nrows):
                for c in range(ncols):
                    clipboard += columns[c][r]
                    if c != (ncols - 1):
                        clipboard += '\t'
                clipboard += '\n'

            # copy to the system clipboard
            sys_clip = QApplication.clipboard()
            sys_clip.setText(clipboard)

            log.debug(f'Copied to clipboard: {clipboard}')
