import io
from functools import lru_cache

from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon, QPainter
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from ModelIntegration import IntegrationModel
from PyQt6.QtWidgets import QMessageBox, QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate
import json


# -------------------------
# Renderer (matplotlib -> QPixmap)
# -------------------------
def latex_to_qpixmap(latex: str, fontsize: int = 18, dpi: int = 200) -> QPixmap:
    """
    Render a LaTeX math string (math mode) to a transparent QPixmap using matplotlib.
    """
    fig = Figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    canvas = FigureCanvas(fig)

    # Put formula in math mode
    fig.text(0, 0, f"${latex}$", fontsize=fontsize)
    canvas.draw()

    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=dpi,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    buf.seek(0)
    img_data = buf.read()
    qimg = QImage.fromData(img_data)
    pix = QPixmap.fromImage(qimg)
    return pix


# Cache rendered pixmaps (keyed by formula and fontsize/dpi)
@lru_cache(maxsize=512)
def cached_latex_to_qpixmap(latex: str, fontsize: int = 18, dpi: int = 200) -> QPixmap:
    return latex_to_qpixmap(latex, fontsize=fontsize, dpi=dpi)


class ModelListFonctions(QAbstractListModel):

    updatedSignal = pyqtSignal(bool)

    def __init__(self):

        super().__init__()

        self.__fonctions = []
        self.from_dict()

    def to_dict(self):
        dict = {}
        for i in range(len(self.__fonctions)):
            dict[str(i)] = self.__fonctions[i].__str__()
        return dict

    def from_dict(self):
        with open('data\listefonctions.json') as json_file:
            data = json.load(json_file)
        if data.__len__() == 0:
            pass
        else:
            for i in range(data.__len__()):
                self.addItem(IntegrationModel(data[str(i)]))

    def export(self):
        with open("data\listeFonctions.json", 'w') as file:
            json.dump(self.to_dict(), file)
            file.close()
        QMessageBox.information(QMessageBox(), "Message", "Liste de fonctions sauvegardée")

    def data(self, index, role=...):

        if not index.isValid():
            return None
        fonction = self.__fonctions[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            # Return empty so default drawing doesn't show raw text.
            return ""
        if role == Qt.ItemDataRole.UserRole:
            self.updatedSignal.emit(True)
            return fonction
        if role == Qt.ItemDataRole.DecorationRole:
            # Provide a tiny icon to keep compatibility; delegate will handle full render
            pix = cached_latex_to_qpixmap(fonction.latex(), fontsize=12, dpi=150)
            if not pix.isNull():
                return QIcon(pix)
            return None
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.__fonctions.append(item)
        (self.endInsertRows())

    def removeItem(self, index):
        if index < self.__fonctions.__len__():
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            item = self.__fonctions[index]
            self.__fonctions.remove(item)
            (self.endInsertRows())

    def fonction(self, row: int) -> str:
        return self.__fonctions[row]


# -------------------------
# Delegate (paints pixmaps on demand)
# -------------------------
class LatexDelegate(QStyledItemDelegate):
    """
    Delegate that paints a cached LaTeX pixmap (rendered with matplotlib).
    It draws selection/background using the view's style, then paints the pixmap
    centered vertically at a left padding. It avoids calling super().paint to
    prevent the default decoration (DecorationRole) from being drawn twice.
    """

    def __init__(self, parent=None, pixmap_fontsize: int = 20, desired_height: int = 84, padding: int = 8):
        super().__init__(parent)
        self.pixmap_fontsize = pixmap_fontsize
        self.desired_height = desired_height
        self.padding = padding

    def paint(self, painter: QPainter, option, index):
        # Instead of calling super().paint (which draws decoration/icon + text),
        # use initStyleOption to get a styled option and then draw only the
        # background/selection/focus via the style, but with text/icon cleared.
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        # Clear text and icon so the style doesn't draw them (prevents duplicates)
        opt.text = ""
        opt.icon = QIcon()

        # Draw background/selection/etc using the style so native look is preserved.
        style = option.widget.style() if option.widget else QApplication.style()
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, option.widget)

        # Now draw our LaTeX pixmap
        fonction = index.data(Qt.ItemDataRole.UserRole).latex()
        pix = None
        if fonction:
            orig = cached_latex_to_qpixmap(fonction.__str__(), fontsize=self.pixmap_fontsize, dpi=200)
            if not orig.isNull():
                pix = orig.scaledToHeight(self.desired_height, mode=Qt.TransformationMode.SmoothTransformation)

        painter.save()
        rect = option.rect
        if pix and not pix.isNull():
            x = rect.x() + self.padding
            y = rect.y() + (rect.height() - pix.height()) // 2
            painter.drawPixmap(x, y, pix)
        else:
            painter.setPen(option.palette.text().color())
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "…")

        # Draw focus rect if needed (optional subtle rectangle)
        if option.state & QStyle.StateFlag.State_HasFocus:
            pen = painter.pen()
            pen.setColor(option.palette.highlight().color())
            painter.setPen(pen)
            r = rect.adjusted(1, 1, -1, -1)
            painter.drawRect(r)

        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        formula = index.data(Qt.ItemDataRole.UserRole)
        if formula:
            orig = cached_latex_to_qpixmap(formula.__str__(), fontsize=self.pixmap_fontsize, dpi=200)
            if not orig.isNull():
                pix = orig.scaledToHeight(self.desired_height, mode=Qt.TransformationMode.SmoothTransformation)
                return QSize(pix.width() + 2 * self.padding, pix.height() + 2 * self.padding)
        return super().sizeHint(option, index)
