import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from userjourney import UserJourney

form_class = uic.loadUiType("uj_editor.ui")[0]                 # Load the UI

class MyWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.import_button.clicked.connect(self.import_uj)  # Bind the event handlers

        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###
        # http://pyqt.sourceforge.net/Docs/PyQt4/qtreewidget.html                    #
        # http://pyqt.sourceforge.net/Docs/PyQt4/qtreewidgetitem.html                #
        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###

        # self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)  #   to the buttons
        # cities = QtWidgets.QTreeWidgetItem()
        # cities.setText(0, 'Muahahaha')
        # osloItem = QtWidgets.QTreeWidgetItem(cities);
        # osloItem.setText(0, "Oslo");
        # osloItem.setText(1, "Yes");
        # self.uj_treeWidget.addTopLevelItem(cities)

    def import_uj(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        f = open(filename[0], 'r')
        filedata = f.read()
        self.xml_textEdit.setText(filedata)
        f.close()

        self.uj = UserJourney('Update Purchase Order User Journey.xml')
        groupnodes = []
        for stepgroup in self.uj.stepgroups:
            new_group_node = QtWidgets.QTreeWidgetItem()
            new_group_node.setText(0, stepgroup.name)
            stepnodes = []
            for step in stepgroup.steps:
                new_step_node = QtWidgets.QTreeWidgetItem(new_group_node)
                new_step_node.setText(0, step.name)
                stepnodes.append(new_step_node)

            groupnodes.append(new_group_node)


        self.uj_treeWidget.addTopLevelItems(groupnodes)


    # def btn_CtoF_clicked(self):                  # CtoF button event handler
    #     cel = float(self.editCel.text())         #
    #     fahr = cel * 9 / 5.0 + 32                #
    #     self.spinFahr.setValue(int(fahr + 0.5))  #

    # def btn_FtoC_clicked(self):                  # FtoC button event handler
    #     fahr = self.spinFahr.value()             #
    #     cel = (fahr - 32) *                      #
    #     self.editCel.setText(str(cel))           #

app = QtWidgets.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()