from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QRadioButton, QComboBox, QSlider
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator, QAction, QIcon
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
from ViewListFonction import ViewListFonction
from ModelListFonctions import ModelListFonctions, cached_latex_to_qpixmap, LatexDelegate


class View(QMainWindow):
    calculerPushButton: QPushButton
    borneInfLineEdit: QLineEdit
    borneSupLineEdit: QLineEdit
    gaucheSumRadioButton: QRadioButton
    droiteSumRadioButton: QRadioButton
    plotWidget: QWidget
    fonctionComboBox: QComboBox
    nombreSlider: QSlider
    sumLineEdti: QLineEdit
    listeFonctionAction: QAction

    fonction: IntegrationModel

    signal_update = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        loadUi("ui/TP2MainWindow.ui", self)



        # setup model pour liste et combobox
        self.listeModel = ModelListFonctions()

        self.fonctionComboBox.setModel(self.listeModel)


        #make both cute
        self.delegate = LatexDelegate(self, pixmap_fontsize=22, desired_height=80, padding=8)

        # Populate DecorationRole with icons sized to delegate.desired_height so the closed QComboBox displays selection(from github copilot)(voir testWithCopilot.py)
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

        model_index = self.listeModel.index(0, 0)

        self.fonction = self.listeModel.data(model_index, Qt.ItemDataRole.UserRole)
        self.canvas = MPLCanvas(self.fonction)
        self.toolbar = NavigationToolbar(self.canvas)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(self.toolbar)
        self.plotWidget.layout().addWidget(self.canvas)

        self.fonctionComboBox.currentIndexChanged.connect(self.set_fonction)


        # fonctionnement
        self.validatorInf = QIntValidator(self)

        self.borneInfLineEdit.setValidator(self.validatorInf)

        self.validatorSup = QIntValidator(self)

        self.borneSupLineEdit.setValidator(self.validatorSup)

        self.calculerPushButton.setEnabled(False)


        self.borneSupLineEdit.textChanged.connect(self.validate_sup)
        self.borneInfLineEdit.textChanged.connect(self.validate_inf)

        self.listFonctionsAction.triggered.connect(self.getList)

        self.gaucheSumRadioButton.clicked.connect(self.set_gaucheSum)
        self.droiteSumRadioButton.clicked.connect(self.set_droiteSum)

        self.calculerPushButton.clicked.connect(self.affiche)

        self.nombreSlider.setRange(1, 100)
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif (event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return) and self.calculerPushButton.isEnabled():
            self.affiche()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_S:
            self.canvas.export()
        else:
            pass

    def affiche(self):
        #1: fix canvas model vs view model not being in sync
        self.canvas.set_fonction(self.fonction)
        self.canvas.plot()
        self.sumLineEdit.setText(str(self.fonction.sum()))
        self.integraleLineEdit.setText(str(self.fonction.integrate()))

    def set_nb_boites(self):
        self.fonction.nb_boites = self.nombreSlider.sliderPosition()

    def set_fonction(self, index):
        text = self.listeModel.fonction(index).__str__()
        print(text)
        self.fonction = IntegrationModel(text)
        self.validate_inf(self.borneInfLineEdit.text())
        self.validate_sup(self.borneSupLineEdit.text())

    def set_gaucheSum(self):
        self.fonction.is_gauche = True

    def set_droiteSum(self):
        self.fonction.is_gauche = False

    def validate_inf(self, texte):
        state, _, _ = self.validatorInf.validate(texte, 0)

        if state == QIntValidator.State.Acceptable and int(texte) < int(self.fonction.borne_sup):
            self.borneInfLineEdit.setStyleSheet("color: #233c67; background-color: white;")
            self.fonction.borne_inf = int(texte)
            state, _, _ = self.validatorSup.validate(self.borneSupLineEdit.text(), 0)
            if state == QIntValidator.State.Acceptable:
                self.calculerPushButton.setEnabled(True)
        else:
            self.borneInfLineEdit.setStyleSheet("color: black; background-color: lightcoral;")
            self.calculerPushButton.setEnabled(False)

    def validate_sup(self, texte):
        state, _, _ = self.validatorSup.validate(texte, 0)

        if state == QIntValidator.State.Acceptable and int(texte) > int(self.fonction.borne_inf):
            self.borneSupLineEdit.setStyleSheet("color: #233c67; background-color: white;")
            self.fonction.borne_sup = int(self.borneSupLineEdit.text())
            state, _, _ = self.validatorInf.validate(self.borneInfLineEdit.text(), 0)
            if state == QIntValidator.State.Acceptable:
                self.calculerPushButton.setEnabled(True)
        else:
            self.borneSupLineEdit.setStyleSheet("color: black; background-color: lightcoral;")
            self.calculerPushButton.setEnabled(False)
