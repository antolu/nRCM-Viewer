import logging
from typing import Optional, List

import numpy as np
from PIL import Image
from PyQt5.QtGui import QPen, QColorConstants as QColor, QBrush
from PyQt5.QtWidgets import QWidget, QMessageBox
from pyqtgraph import ImageItem, GraphicsView, ViewBox, PlotDataItem, TextItem

from .table_model import Sample
from ..data import ZipReader
from ..utils import run_in_main_thread

log = logging.getLogger(__name__)


class PlotWidget(GraphicsView):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.vb = ViewBox()
        self.vb.setAspectLocked()
        self.vb.invertY()
        self.setCentralItem(self.vb)

        self.item: ImageItem = ImageItem(axisOrder='row-major')

        self.boxes: List[PlotDataItem] = list()
        self.labels: List[TextItem] = list()

        self.pen_red = QPen(QColor.Red, 4)

        self.vb.addItem(self.item)

    @run_in_main_thread
    def show_image(self, sample: Sample, reader: ZipReader):
        try:
            image = Image.open(reader.open(sample.filepath))
        except OSError as e:
            QMessageBox.critical(
                self, 'Error',
                f'Error in loading image from {sample.filepath}\n{e}')
            return

        self.item.setImage(np.asarray(image))

        self.draw_boxes(sample)

    def draw_boxes(self, sample: Sample):
        if sample.num_detections > len(self.boxes):
            self.create_boxes(sample.num_detections - len(self.boxes))

        i = 0
        for i in range(sample.num_detections):
            box = np.array(sample.bbox[i].to_coords())
            label = sample.bbox[i].cls
            score = sample.bbox[i].score

            text = f'{label}: {score:.3f}'

            self.boxes[i].setData(box)
            self.labels[i].setText(text)
            self.labels[i].setPos(sample.bbox[i].x0, sample.bbox[i].y1 + 10)
            self.labels[i].setVisible(True)

        for j in range(i + 1, len(self.boxes)):
            self.boxes[j].clear()
            self.labels[j].setVisible(False)

    def create_boxes(self, num_boxes: int):
        for _ in range(num_boxes):
            self.boxes.append(
                PlotDataItem(pen=self.pen_red, connect='all', ))
            self.labels.append(TextItem(color=QColor.Black, fill=QColor.Red))
            self.labels[-1].fill = QBrush(QColor.Red)

            self.vb.addItem(self.boxes[-1])
            self.vb.addItem(self.labels[-1])
