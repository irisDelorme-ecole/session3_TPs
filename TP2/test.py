
# import matplotlib.pyplot as plt
# import sympy
#
# x = sympy.symbols('x')
# y = 1 + sympy.sin(sympy.sqrt(x**2 + 20))
# lat = sympy.latex(y)
#
# #add text
# plt.text(0, 0.6, r"$%s$" % lat, fontsize = 12)
#
# #hide axes
# fig = plt.gca()
# fig.axes.get_xaxis().set_visible(False)
# fig.axes.get_yaxis().set_visible(False)
# plt.draw() #or savefig
# plt.show()
import sys

import sympy
from PIL.ImageQt import ImageQt
from PyQt6.QtWidgets import QApplication, QListView, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon, QStandardItem, QStandardItemModel
from PyQt6.QtCore import QByteArray
import matplotlib.pyplot as plt
from io import BytesIO



import sys
from PyQt6.QtWidgets import QApplication, QListView,  QStyledItemDelegate, QStyleOptionViewItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QModelIndex, QAbstractListModel
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Function to create a Matplotlib plot and convert it to QPixmap
def create_plot_as_pixmap():
    # Create a simple plot
    plt.figure(figsize=(2, 1))
    x = sympy.symbols('x')
    y = 1 + sympy.sin(sympy.sqrt(x**2 + 20))
    lat = sympy.latex(y)

    #add text
    plt.text(0, 0.6, r"$%s$" % lat, fontsize = 12)

    #hide axes
    fig = plt.gca()
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.spines.clear()
    # plt.draw() #or savefig
    # plt.show()

    plt.tight_layout()

    # Save the plot to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Convert the buffer to a QPixmap
    image = Image.open(buffer)
    return QPixmap.fromImage(ImageQt(image))

# Custom List Model
class PlotListModel(QAbstractListModel):
    def __init__(self, plots, parent=None):
        super().__init__(parent)
        self.plots = plots

    def rowCount(self, parent=QModelIndex()):
        return len(self.plots)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DecorationRole:
            return self.plots[index.row()]
        return None

# Custom Delegate to render the pixmap
class PlotDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        pixmap = index.data(Qt.ItemDataRole.DecorationRole)
        if pixmap:
            painter.drawPixmap(option.rect, pixmap)

# Main Application
app = QApplication(sys.argv)

# Create a list of plots
plots = [create_plot_as_pixmap() for _ in range(5)]

# Set up the QListView
list_view = QListView()
model = PlotListModel(plots)
delegate = PlotDelegate()

list_view.setModel(model)
list_view.setItemDelegate(delegate)
list_view.setSpacing(10)
list_view.show()

sys.exit(app.exec())
