from typing import Iterable

try:
    from Qt.QtGui import QColor, QPaintEvent, QPen, QPainter
    from Qt.QtWidgets import QFrame
except ImportError:
    from qtpy.QtGui import QColor, QPaintEvent, QPen, QPainter
    from qtpy.QtWidgets import QFrame


class PlaceHolder(QFrame):
    """
    QSugar Place Holder
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.color = QColor("#000000")
        self.pen_width = 10

    def setColor(self, color):
        if isinstance(color, QColor):
            self.color = color
        elif isinstance(color, Iterable):
            self.color = QColor(*color)
        else:
            self.color = QColor(color)

    def setPenWidth(self, width):
        self.pen_width = width

    def paintEvent(self, event: QPaintEvent) -> None:
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(self.pen_width)

        painter = QPainter(self)
        if self.objectName():
            painter.drawText(self.width() // 8, self.height() // 2, self.objectName())

        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.drawLine(0, 0, self.width() - 1, self.height() - 1)
        painter.drawLine(self.width(), 0, 0, self.height() - 1)