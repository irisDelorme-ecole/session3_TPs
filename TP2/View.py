from PyQt6.QtCore import pyqtSignal, QModelIndex, Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QRadioButton, QComboBox, QSlider, QFileDialog, QDockWidget, QListView
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator, QAction, QIcon
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
from ViewListFonction import ViewListFonction
from ModelListFonctions import ModelListFonctions, cached_latex_to_qpixmap, LatexDelegate


class View(QMainWindow):

    calculerPushButton:QPushButton
    borneInfLineEdit:QLineEdit
    borneSupLineEdit:QLineEdit
    gaucheSumRadioButton:QRadioButton
    droiteSumRadioButton: QRadioButton
    plotWidget:QWidget
    fonctionComboBox:QComboBox
    nombreSlider:QSlider
    sumLineEdti: QLineEdit
    listeFonctionAction:QAction


    fonction:IntegrationModel

    signal_update = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        loadUi("ui/TP2MainWindow.ui", self)

        # setup de base
        self.listeModel = ModelListFonctions()

        self.fonctionComboBox.setModel(self.listeModel)


        self.fonctionComboBox.currentTextChanged.connect(self.set_fonction)

        self.delegate = LatexDelegate(self, pixmap_fontsize=22, desired_height=80, padding=8)

        # Populate DecorationRole with icons sized to delegate.desired_height so the closed QComboBox displays selection
        max_w = 0
        max_h = 0
        icons = []
        for row in range(self.listeModel.rowCount()):
            fonction = self.listeModel.fonction(row)
            orig = cached_latex_to_qpixmap(fonction.__str__(), fontsize=self.delegate.pixmap_fontsize, dpi=200)
            if not orig.isNull():
                pix = orig.scaledToHeight(self.delegate.desired_height, mode=Qt.TransformationMode.SmoothTransformation)
                icons.append((row, QIcon(pix), pix))
                max_w = max(max_w, pix.width())
                max_h = max(max_h, pix.height())

        for row, icon, pix in icons:
            # set the DecorationRole only for combo's use
            self.fonctionComboBox.setItemData(row, icon, role=Qt.ItemDataRole.DecorationRole)

        if max_w > 0 and max_h > 0:
            self.fonctionComboBox.setIconSize(QSize(max_w, max_h))
            self.fonctionComboBox.setMinimumHeight(max_h + 12)

        model_index = self.listeModel.index(0,0)

        self.fonction = self.listeModel.data(model_index, Qt.ItemDataRole.UserRole)
        self.canvas = MPLCanvas(self.fonction)
        self.toolbar = NavigationToolbar(self.canvas)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(self.toolbar)
        self.plotWidget.layout().addWidget(self.canvas)




        #self.viewListFonctions.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        #fonctionnement
        self.validatorInf = QIntValidator(self)

        self.borneInfLineEdit.setValidator(self.validatorInf)


        self.validatorSup = QIntValidator(self)

        self.borneSupLineEdit.setValidator(self.validatorSup)


        self.borneSupLineEdit.textChanged.connect(self.validate_sup)
        self.borneInfLineEdit.textChanged.connect(self.validate_inf)

        self.listFonctionsAction.triggered.connect(self.getList)

        self.gaucheSumRadioButton.clicked.connect(self.set_gaucheSum)
        self.droiteSumRadioButton.clicked.connect(self.set_droiteSum)


        self.calculerPushButton.clicked.connect(self.affiche)

        self.nombreSlider.setRange(1,100)
        self.nombreSlider.setSingleStep(1)
        self.nombreSlider.setValue(1)


        self.nombreSlider.valueChanged.connect(self.set_nb_boites)


        self.quitterAction.triggered.connect(self.close)
        self.exporterAction.triggered.connect(self.exporter)


    def getList(self):
        self.viewListFonctions = ViewListFonction(self.listeModel, self)
        self.viewListFonctions.show()

    def exporter(self):
        self.canvas.exporter()

    def affiche(self):
        self.canvas.plot()
        self.sumLineEdit.setText(str(self.fonction.sum()))
        self.integraleLineEdit.setText(str(self.fonction.integrate()))

    def set_nb_boites(self):
        self.fonction.nb_boites = self.nombreSlider.sliderPosition()


    def set_fonction(self, value):
        self.fonction.fonction = value

    def set_gaucheSum(self):
        self.fonction.is_gauche = True

    def set_droiteSum(self):
        self.fonction.is_gauche = False


    def validate_inf(self, texte):
        state, _, _ = self.validatorInf.validate(texte, 0)

        if state == QIntValidator.State.Acceptable:
            self.borneInfLineEdit.setStyleSheet("color: black; background-color: white;")
            self.fonction.borne_inf = int(texte)

        else:
            self.borneInfLineEdit.setStyleSheet("color: black; background-color: lightcoral;")

    def validate_sup(self, texte):
        state, _, _ = self.validatorSup.validate(texte, 0)

        if state == QIntValidator.State.Acceptable and int(texte) > int(self.fonction.borne_inf):
            self.borneSupLineEdit.setStyleSheet("color: black; background-color: white;")
            self.fonction.borne_sup = int(self.borneSupLineEdit.text())
        else:
            self.borneSupLineEdit.setStyleSheet("color: black; background-color: lightcoral;")

