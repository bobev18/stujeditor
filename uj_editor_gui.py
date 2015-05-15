import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from userjourney import UserJourney

DDI_TYPES = {'Auto-Correlated': 'AUTOCORR', 'Auto-Incremented': 'AUTOINCR', 'Constant': 'CONSTANT', 'Date': 'DATE    ', 'Delimited File': 'FLATFILE', 'Java Class': '', 'List': 'LIST    ', 'Related': 'SAMEAS  ', 'Response': 'RESPONSE', 'Variable': 'VARIABLE'}

form_class = uic.loadUiType("uj_editor.ui")[0]                 # Load the UI

class MyWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.import_button.clicked.connect(self.import_uj)
        self.ddi_treeWidget.itemSelectionChanged.connect(self.load_item_details)
        self.steps_treeWidget.itemSelectionChanged.connect(self.load_item_details)

        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###
        # http://pyqt.sourceforge.net/Docs/PyQt4/qtreewidget.html                    #
        # http://pyqt.sourceforge.net/Docs/PyQt4/qtreewidgetitem.html                #
        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###

        # cities = QtWidgets.QTreeWidgetItem()
        # cities.setText(0, 'Muahahaha')
        # osloItem = QtWidgets.QTreeWidgetItem(cities);
        # osloItem.setText(0, "Oslo");
        # osloItem.setText(1, "Yes");
        # self.uj_treeWidget.addTopLevelItem(cities)

        layout = QtWidgets.QVBoxLayout()

        self.ddi_type = QtWidgets.QComboBox(self.ddi_groupBox)
        self.ddi_type.addItems(DDI_TYPES.values())
        self.ddi_type.setCurrentText('')

        layout.addWidget(self.ddi_type) # add widget
        # set my layout to make sure contents are correctly rendered
        self.ddi_groupBox.setLayout(layout)

    def load_item_details(self):
        selected_ddi_name = self.ddi_treeWidget.selectedItems()[0].text(0)
        self.element_name_lineEdit.setText(selected_ddi_name)
        selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)

        # print(self.ddi_groupBox.__dict__)
        # print(type(self.ddi_groupBox).__dict__)
        # layout = self.ddi_groupBox.layout # create layout out
        # layout = QtWidgets.QVBoxLayout()

        # self.ddi_type = QtWidgets.QComboBox(self.ddi_groupBox)
        # self.ddi_type.addItems(DDI_TYPES.values())
        self.ddi_type.setCurrentText(selected_ddi.type)

        # layout.addWidget(self.ddi_type) # add widget
        # # set my layout to make sure contents are correctly rendered
        # self.ddi_groupBox.clear()
        # self.ddi_groupBox.setLayout(layout)



        # self.ddi_groupBox.setCentralWidget(self.ddi_type)







        # self.element = element
        # self.existing = bool(element.get('EXISTING'))
        # self.name = element.get('NAME')
        # self.valid = bool(element.get('VALID'))
        # self.valid = element.attrib['VALID']
            # self.type = element.find(SCHEME_PREFIX+'SOURCE').attrib['TYPE']
            # self.selection_type = element.find(SCHEME_PREFIX+'SELECTION').attrib['TYPE']
            # self.scope = element.find(SCHEME_PREFIX+'SCOPE').attrib['TYPE']
            # self.lifecycle = element.find(SCHEME_PREFIX+'LIFECYCLE').attrib['TYPE']
            # self.description = element.find(SCHEME_PREFIX+'DESCRIPTION').text
            # self.items = {}
            # for item in element.findall(SCHEME_PREFIX+'ITEM'):
            #     self.items[item.get('CODE')] = item.text
            # siphons_element = element.find(SCHEME_PREFIX+'SIPHONS')
            # self.siphons = []
            # if siphons_element:
            #     for siphon in siphons_element.findall(SCHEME_PREFIX+'SIPHON'):
            #         self.siphons.append(Siphon(siphon))

    def import_uj(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        # f = open(filename[0], 'r')
        # filedata = f.read()
        # self.xml_textEdit.setText(filedata)
        # f.close()

        self.uj = UserJourney('Update Purchase Order User Journey.xml')

        self.uj_name.setText(self.uj.name)

        ddi_nodes = []
        for ddi in self.uj.dditems:
            new_ddi_node = QtWidgets.QTreeWidgetItem()
            new_ddi_node.setText(0, ddi.name)
            ddi_nodes.append(new_ddi_node)

        self.ddi_treeWidget.addTopLevelItems(ddi_nodes)

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


        self.steps_treeWidget.addTopLevelItems(groupnodes)


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