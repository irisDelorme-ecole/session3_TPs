"""
dans ce fichier se trouve tout le code généré par github Copilot le samedi 25 octobre.
il porte uniquement sur l'affichage du combobox et du listview et sert à
afficher les fonctions en utilisant les fonctionnalités LaTeX
implementées par matplotlib.

"""
"""
PyQt6 demo: QAbstractListModel + QStyledItemDelegate to render LaTeX formulas.

- Uses matplotlib to render LaTeX into QPixmap (cached).
- Delegate paints pixmaps on demand and provides sizeHint.
- The same delegate is installed on QListView and QComboBox.view() so the
  popup uses identical rendering.

Requirements:
    pip install PyQt6 matplotlib
"""
import sys
import io
from functools import lru_cache

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from PyQt6.QtCore import (
    Qt,
    QSize,
    QAbstractListModel,
    QModelIndex,
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListView,
    QComboBox,
    QLabel,
    QSizePolicy,
    QStyledItemDelegate,
    QStyle,
    QStyleOptionViewItem,
)


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
        pad_inches=0.0,
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


# -------------------------
# Model (stores LaTeX strings)
# -------------------------
class LatexListModel(QAbstractListModel):
    """
    Simple list model storing LaTeX formula strings.
    The model exposes the formula under Qt.ItemDataRole.UserRole.
    DisplayRole intentionally returns an empty string so views don't show raw text.
    """

    def __init__(self, formulas: list[str], parent=None):
        super().__init__(parent)
        self._formulas = list(formulas)

    def rowCount(self, parent=QModelIndex()):
        return len(self._formulas)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        if row < 0 or row >= len(self._formulas):
            return None
        formula = self._formulas[row]
        if role == Qt.ItemDataRole.DisplayRole:
            # Return empty so default drawing doesn't show raw text.
            return ""
        if role == Qt.ItemDataRole.UserRole:
            # Return the LaTeX string for delegates/consumers
            return formula
        # For convenience, also return a small icon for tools that expect DecorationRole
        if role == Qt.ItemDataRole.DecorationRole:
            # Provide a tiny icon to keep compatibility; delegate will handle full render
            pix = cached_latex_to_qpixmap(formula, fontsize=12, dpi=150)
            if not pix.isNull():
                return QIcon(pix)
            return None
        return None

    def formula(self, row: int) -> str:
        return self._formulas[row]


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

    def __init__(self, parent=None, pixmap_fontsize: int = 20, desired_height: int = 72, padding: int = 8):
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
        formula = index.data(Qt.ItemDataRole.UserRole)
        pix = None
        if formula:
            orig = cached_latex_to_qpixmap(formula, fontsize=self.pixmap_fontsize, dpi=200)
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
            orig = cached_latex_to_qpixmap(formula, fontsize=self.pixmap_fontsize, dpi=200)
            if not orig.isNull():
                pix = orig.scaledToHeight(self.desired_height, mode=Qt.TransformationMode.SmoothTransformation)
                return QSize(pix.width() + 2 * self.padding, pix.height() + 2 * self.padding)
        return super().sizeHint(option, index)


# -------------------------
# Demo UI
# -------------------------
class DemoWindow(QWidget):
    def __init__(self, formulas):
        super().__init__()
        self.setWindowTitle("LaTeX Delegate demo (PyQt6)")
        self.resize(900, 600)
        layout = QVBoxLayout(self)

        label = QLabel("Model + QStyledItemDelegate rendering LaTeX formulas (icons only).")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Model
        self.model = LatexListModel(formulas, parent=self)

        # Delegate: tune desired_height to control rendered size
        self.delegate = LatexDelegate(self, pixmap_fontsize=22, desired_height=80, padding=8)

        # QListView
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(self.delegate)
        self.list_view.setSpacing(6)
        layout.addWidget(self.list_view)

        # QComboBox which uses same model & delegate for popup
        self.combo = QComboBox()
        self.combo.setModel(self.model)

        # Install delegate on popup view (so the popup is rendered by our delegate).
        self.combo.view().setItemDelegate(self.delegate)
        # We DO NOT set combo.setItemDelegate(self.delegate) here to avoid having the same
        # delegate draw the closed-area (which uses DecorationRole) unless you want that.
        # Instead, we populate DecorationRole icons below so the closed combo shows an icon.
        layout.addWidget(self.combo)

        # Populate DecorationRole with icons sized to delegate.desired_height so the closed QComboBox displays selection
        max_w = 0
        max_h = 0
        icons = []
        for row in range(self.model.rowCount()):
            formula = self.model.formula(row)
            orig = cached_latex_to_qpixmap(formula, fontsize=self.delegate.pixmap_fontsize, dpi=200)
            if not orig.isNull():
                pix = orig.scaledToHeight(self.delegate.desired_height, mode=Qt.TransformationMode.SmoothTransformation)
                icons.append((row, QIcon(pix), pix))
                max_w = max(max_w, pix.width())
                max_h = max(max_h, pix.height())

        for row, icon, pix in icons:
            # set the DecorationRole only for combo's use
            self.combo.setItemData(row, icon, role=Qt.ItemDataRole.DecorationRole)

        if max_w > 0 and max_h > 0:
            self.combo.setIconSize(QSize(max_w, max_h))
            self.combo.setMinimumHeight(max_h + 12)

        # Optional: set first selection
        if self.model.rowCount() > 0:
            self.list_view.setCurrentIndex(self.model.index(0, 0))
            self.combo.setCurrentIndex(0)

        # Preview label
        self.preview = QLabel()
        self.preview.setWordWrap(True)
        layout.addWidget(self.preview)

        self.list_view.selectionModel().currentChanged.connect(self.on_selection_changed)
        self.combo.currentIndexChanged.connect(self.on_combo_changed)
        self.update_preview_from_index(self.list_view.currentIndex())

    def on_selection_changed(self, current: QModelIndex, previous: QModelIndex):
        self.update_preview_from_index(current)

    def on_combo_changed(self, idx: int):
        idxm = self.model.index(idx, 0)
        self.update_preview_from_index(idxm)

    def update_preview_from_index(self, index: QModelIndex):
        if not index or not index.isValid():
            self.preview.setText("")
            return
        formula = index.data(Qt.ItemDataRole.UserRole)
        self.preview.setText(f"Selected LaTeX: {formula}")


def main():
    app = QApplication(sys.argv)

    formulas = [
        r"\alpha, \beta, \gamma",
        r"\int_{0}^{\infty} e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}",
        r"\frac{d}{dx} \sin x = \cos x",
        r"\sum_{n=0}^{\infty} \frac{x^n}{n!} = e^x",
        r"\mathcal{L}\{f(t)\} = \int_0^\infty e^{-st} f(t)\,dt",
        r"\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}",
        r"\frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
    ]

    demo = DemoWindow(formulas)
    demo.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()