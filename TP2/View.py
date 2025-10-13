from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QRadioButton, QComboBox, QSlider, QFileDialog, QDockWidget, QListView
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator, QAction

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
import sys
from PyQt6.QtWidgets import QApplication
from ViewListFonction import ViewListFonction
from ModelListFonctions import ModelListFonctions


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

    def __init__(self):
        super().__init__()

        loadUi("ui/TP2MainWindow.ui", self)

        # setup de base
        self.fonction = IntegrationModel()
        self.canvas = MPLCanvas(self.fonction)
        self.toolbar = NavigationToolbar(self.canvas)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(self.toolbar)
        self.plotWidget.layout().addWidget(self.canvas)

        self.listeModel = ModelListFonctions()

        self.fonctionComboBox.setModel(self.listeModel)

        self.fonctionComboBox.currentTextChanged.connect(self.set_fonction)


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

        self.nombreSlider.setRange(1,25)
        self.nombreSlider.setSingleStep(1)
        self.nombreSlider.setValue(1)

        self.nombreSlider.sliderMoved.connect(self.set_nb_boites)

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

    def set_nb_boites(self, value):
        self.fonction.nb_boites = int(value)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex3 = View()
    ex3.show()
    sys.exit(app.exec())