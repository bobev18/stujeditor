import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from userjourney import UserJourney

# DDI_TYPES = {'Auto-Correlated': 'AUTOCORR', 'Auto-Incremented': 'AUTOINCR', 'Constant': 'CONSTANT', 'Date': 'DATE    ', 'Delimited File': 'FLATFILE', 'Java Class': '', 'List': 'LIST    ', 'Related': 'SAMEAS  ', 'Response': 'RESPONSE', 'Variable': 'VARIABLE'}
DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
# SELECTOR_TYPES = {'Auto-Incremented': 'AUTOINCR', 'First': 'FIRST   ', 'Last': 'LAST    ', 'Random': 'RANDOM  ', 'Related': 'SAMEAS  ', 'Sequential': 'SEQUENTI', 'Date': 'DATE    ', 'Sequential Unique': 'SEQUONCE'}
# SELECTOR_TYPES = {'First': 'FIRST   ', 'Last': 'LAST    ', 'Random': 'RANDOM  ', 'Random Unique': 'RANDONCE', 'Sequential': 'SEQUENTI', 'Sequential Unique': 'SEQUONCE'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}


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

        layout = QtWidgets.QGridLayout()

        self.ddi_name_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_name_label.setText('DDI Name')
        self.ddi_name = QtWidgets.QLineEdit(self.ddi_groupBox)
        layout.addWidget(self.ddi_name_label, 0, 0)
        layout.addWidget(self.ddi_name, 1, 0, 1, 2)
        self.ddi_type_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_type_label.setText('Type')
        self.ddi_type = QtWidgets.QComboBox(self.ddi_groupBox)
        self.ddi_type.addItems(DDI_TYPES.values())
        self.ddi_type.setCurrentText('')
        layout.addWidget(self.ddi_type_label, 2, 0)
        layout.addWidget(self.ddi_type, 2, 1)


        self.ddi_description_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_description_label.setText('Description')
        self.ddi_description = QtWidgets.QTextEdit(self.ddi_groupBox)
        # self.ddi_description.setFixedHeight(60)
        self.ddi_description.setText('')
        layout.addWidget(self.ddi_description_label, 0, 2)
        layout.addWidget(self.ddi_description, 1, 2, 2, 3)


        self.ddi_shared_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_shared_label.setText('Sharing selector state:')
        self.shared_group = QtWidgets.QButtonGroup(self.ddi_groupBox)
        self.ddi_shared_one = QtWidgets.QRadioButton('Single User', self.ddi_groupBox)
        self.ddi_shared_all = QtWidgets.QRadioButton('All UJ Users', self.ddi_groupBox)
        self.shared_group.addButton(self.ddi_shared_one)
        self.shared_group.addButton(self.ddi_shared_all)
        layout.addWidget(self.ddi_shared_label, 4, 0, 1, 2)
        layout.addWidget(self.ddi_shared_one, 4, 2)
        layout.addWidget(self.ddi_shared_all, 4, 3)
        self.shared_button_mapping = {'SCRIPT  ': self.ddi_shared_one, 'THREAD  ': self.ddi_shared_all}

        self.ddi_refresh_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_refresh_label.setText('Refresh triggers:')
        self.refresh_group = QtWidgets.QButtonGroup(self.ddi_groupBox)
        self.ddi_refresh_once_per_run = QtWidgets.QRadioButton('Once per Run', self.ddi_groupBox)
        self.ddi_refresh_once_per_user = QtWidgets.QRadioButton('Once per User', self.ddi_groupBox)
        self.ddi_refresh_every_cycle = QtWidgets.QRadioButton('Every Cycle', self.ddi_groupBox)
        self.ddi_refresh_every_time = QtWidgets.QRadioButton('Every Time', self.ddi_groupBox)
        self.refresh_group.addButton(self.ddi_refresh_once_per_run)
        self.refresh_group.addButton(self.ddi_refresh_once_per_user)
        self.refresh_group.addButton(self.ddi_refresh_every_cycle)
        self.refresh_group.addButton(self.ddi_refresh_every_time)
        layout.addWidget(self.ddi_refresh_label, 5, 0)
        layout.addWidget(self.ddi_refresh_once_per_run, 5, 1)
        layout.addWidget(self.ddi_refresh_once_per_user, 5, 2)
        layout.addWidget(self.ddi_refresh_every_cycle, 5, 3)
        layout.addWidget(self.ddi_refresh_every_time, 5, 4)
        self.refresh_button_mapping = {'C': self.ddi_refresh_every_cycle, 'R': self.ddi_refresh_once_per_run, 'T': self.ddi_refresh_every_time, 'U': self.ddi_refresh_once_per_user}


        self.ddi_selector_label = QtWidgets.QLabel(self.ddi_groupBox)
        self.ddi_selector_label.setText('Selector')
        self.ddi_selector = QtWidgets.QComboBox(self.ddi_groupBox)
        self.ddi_selector.addItems(SELECTOR_TYPES.values())
        self.ddi_selector.setCurrentText('')
        layout.addWidget(self.ddi_selector_label, 6, 0)
        layout.addWidget(self.ddi_selector, 6, 1)


        layout.addWidget(self.ddi_type) # add widget
        # set my layout to make sure contents are correctly rendered
        self.ddi_groupBox.setLayout(layout)

    def load_item_details(self):
        selected_ddi_name = self.ddi_treeWidget.selectedItems()[0].text(0)
        self.ddi_name.setText(selected_ddi_name)
        selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)
        self.ddi_description.setText(selected_ddi.description)
        self.ddi_type.setCurrentText(DDI_TYPES[selected_ddi.type])
        # print(selected_ddi.scope, self.shared_button_mapping[selected_ddi.scope])
        # print(self..checkedButton())
        self.shared_button_mapping[selected_ddi.scope].setChecked(1)
        self.refresh_button_mapping[selected_ddi.lifecycle].setChecked(1)

        if selected_ddi.selection_type in SELECTOR_TYPES.keys():
            # self.ddi_selector.setEnabled(True)
            self.ddi_selector.show()
            self.ddi_selector.setCurrentText(SELECTOR_TYPES[selected_ddi.selection_type])
        else:
            # self.ddi_selector.setEnabled(False)
            self.ddi_selector.hide()

            # self.ddi_selector.setCurrentText(selected_ddi.selection_type)

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