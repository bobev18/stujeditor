import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from userjourney import UserJourney

# DDI_TYPES = {'Auto-Correlated': 'AUTOCORR', 'Auto-Incremented': 'AUTOINCR', 'Constant': 'CONSTANT', 'Date': 'DATE    ', 'Delimited File': 'FLATFILE', 'Java Class': '', 'List': 'LIST    ', 'Related': 'SAMEAS  ', 'Response': 'RESPONSE', 'Variable': 'VARIABLE'}
DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
# SELECTOR_TYPES = {'Auto-Incremented': 'AUTOINCR', 'First': 'FIRST   ', 'Last': 'LAST    ', 'Random': 'RANDOM  ', 'Related': 'SAMEAS  ', 'Sequential': 'SEQUENTI', 'Date': 'DATE    ', 'Sequential Unique': 'SEQUONCE'}
# SELECTOR_TYPES = {'First': 'FIRST   ', 'Last': 'LAST    ', 'Random': 'RANDOM  ', 'Random Unique': 'RANDONCE', 'Sequential': 'SEQUENTI', 'Sequential Unique': 'SEQUONCE'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}

DDI_ITEM_CODES = ['ASSOCIATED', 'DELIMITER ', 'ENCODE    ', 'FIELDINDEX', 'FIELDNAME ', 'FIELDTYPE ', 'FILENAME  ', 'INCREMENT ', 'INDEX     ', 'INHEADERS ', 'INITALVALU', 'INPOST    ', 'INURL     ', 'MINLENGTH ', 'STARTVALUE', 'STEPREF   ', 'VALUE     ',]

form_class = uic.loadUiType("uj_editor.ui")[0]                 # Load the UI

class MyWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.import_button.clicked.connect(self.import_uj)
        self.ddi_treeWidget.itemSelectionChanged.connect(self.load_item_details)
        self.steps_treeWidget.itemSelectionChanged.connect(self.load_item_details)

        # self..ddi_groupBox = QtWidgets.QGroupBox(centralwidget)  <----- this comes from the ui file -- added as reference
        ddi_layout = QtWidgets.QGridLayout()
        common_ddi_groupbox = QtWidgets.QGroupBox(self.ddi_groupBox)
        common_ddi_layout = QtWidgets.QGridLayout()


        # DDI Name
        self.ddi_name_label = QtWidgets.QLabel(common_ddi_groupbox)
        self.ddi_name_label.setText('DDI Name')
        self.ddi_name = QtWidgets.QLineEdit(common_ddi_groupbox)
        common_ddi_layout.addWidget(self.ddi_name_label, 0, 0)
        common_ddi_layout.addWidget(self.ddi_name, 1, 0, 1, 2)

        # DDI Type
        self.ddi_type_label = QtWidgets.QLabel(common_ddi_groupbox)
        self.ddi_type_label.setText('Type')
        self.ddi_type = QtWidgets.QComboBox(common_ddi_groupbox)
        self.ddi_type.addItems(DDI_TYPES.values())
        self.ddi_type.setCurrentText('')
        common_ddi_layout.addWidget(self.ddi_type_label, 2, 0)
        common_ddi_layout.addWidget(self.ddi_type, 2, 1)

        # DDI Description
        self.ddi_description_label = QtWidgets.QLabel(common_ddi_groupbox)
        self.ddi_description_label.setText('Description')
        self.ddi_description = QtWidgets.QTextEdit(common_ddi_groupbox)
        # self.ddi_description.setFixedHeight(60)
        self.ddi_description.setText('')
        common_ddi_layout.addWidget(self.ddi_description_label, 0, 2)
        common_ddi_layout.addWidget(self.ddi_description, 1, 2, 2, 3)

        # DDI Shared
        self.ddi_shared_label = QtWidgets.QLabel(common_ddi_groupbox)
        self.ddi_shared_label.setText('Sharing selector state:')
        self.shared_group = QtWidgets.QButtonGroup(common_ddi_groupbox)
        self.ddi_shared_one = QtWidgets.QRadioButton('Single User', common_ddi_groupbox)
        self.ddi_shared_all = QtWidgets.QRadioButton('All UJ Users', common_ddi_groupbox)
        self.shared_group.addButton(self.ddi_shared_one)
        self.shared_group.addButton(self.ddi_shared_all)
        common_ddi_layout.addWidget(self.ddi_shared_label, 4, 0, 1, 2)
        common_ddi_layout.addWidget(self.ddi_shared_one, 4, 2)
        common_ddi_layout.addWidget(self.ddi_shared_all, 4, 3)
        self.shared_button_mapping = {'SCRIPT  ': self.ddi_shared_one, 'THREAD  ': self.ddi_shared_all}

        # DDI Refresh
        self.ddi_refresh_label = QtWidgets.QLabel(common_ddi_groupbox)
        self.ddi_refresh_label.setText('Refresh triggers:')
        self.refresh_group = QtWidgets.QButtonGroup(common_ddi_groupbox)
        self.ddi_refresh_once_per_run = QtWidgets.QRadioButton('Once per Run', common_ddi_groupbox)
        self.ddi_refresh_once_per_user = QtWidgets.QRadioButton('Once per User', common_ddi_groupbox)
        self.ddi_refresh_every_cycle = QtWidgets.QRadioButton('Every Cycle', common_ddi_groupbox)
        self.ddi_refresh_every_time = QtWidgets.QRadioButton('Every Time', common_ddi_groupbox)
        self.refresh_group.addButton(self.ddi_refresh_once_per_run)
        self.refresh_group.addButton(self.ddi_refresh_once_per_user)
        self.refresh_group.addButton(self.ddi_refresh_every_cycle)
        self.refresh_group.addButton(self.ddi_refresh_every_time)
        common_ddi_layout.addWidget(self.ddi_refresh_label, 5, 0)
        common_ddi_layout.addWidget(self.ddi_refresh_once_per_run, 5, 1)
        common_ddi_layout.addWidget(self.ddi_refresh_once_per_user, 5, 2)
        common_ddi_layout.addWidget(self.ddi_refresh_every_cycle, 5, 3)
        common_ddi_layout.addWidget(self.ddi_refresh_every_time, 5, 4)
        self.refresh_button_mapping = {'C': self.ddi_refresh_every_cycle, 'R': self.ddi_refresh_once_per_run, 'T': self.ddi_refresh_every_time, 'U': self.ddi_refresh_once_per_user}



        specific_ddi_groupbox = QtWidgets.QGroupBox(self.ddi_groupBox)
        specific_ddi_layout = QtWidgets.QGridLayout()


        # DDI Selector
        self.ddi_selector_label = QtWidgets.QLabel(specific_ddi_groupbox)
        self.ddi_selector_label.setText('Selector')
        self.ddi_selector = QtWidgets.QComboBox(specific_ddi_groupbox)
        self.ddi_selector.addItems(SELECTOR_TYPES.values())
        self.ddi_selector.setCurrentText('')
        specific_ddi_layout.addWidget(self.ddi_selector_label, 6, 0)
        specific_ddi_layout.addWidget(self.ddi_selector, 6, 1)

        # DDI Value
        self.ddi_value_label = QtWidgets.QLabel(specific_ddi_groupbox)
        self.ddi_value_label.setText('Value')
        self.ddi_value = QtWidgets.QLineEdit(specific_ddi_groupbox)
        self.ddi_value.setText('')
        specific_ddi_layout.addWidget(self.ddi_value_label, 7, 0)
        specific_ddi_layout.addWidget(self.ddi_value, 7, 1, 1, 4)



        # common_ddi_layout.addWidget(self.ddi_type) # add widget
        common_ddi_groupbox.setLayout(common_ddi_layout)
        specific_ddi_groupbox.setLayout(specific_ddi_layout)
        ddi_layout.addWidget(common_ddi_groupbox, 1, 1, 1, 1)
        ddi_layout.addWidget(specific_ddi_groupbox, 2, 1, 2, 1)
        # ddi_layout.addWidget(common_ddi_groupbox)
        # ddi_layout.addWidget(specific_ddi_groupbox)

        self.ddi_groupBox.setLayout(ddi_layout)


    def load_item_details(self):
        selected_ddi_name = self.ddi_treeWidget.selectedItems()[0].text(0)
        self.ddi_name.setText(selected_ddi_name)
        selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)

        self.ddi_description.setText(selected_ddi.description)
        self.ddi_type.setCurrentText(DDI_TYPES[selected_ddi.type])
        self.shared_button_mapping[selected_ddi.scope].setChecked(1)
        self.refresh_button_mapping[selected_ddi.lifecycle].setChecked(1)

        if selected_ddi.selection_type in SELECTOR_TYPES.keys():
            self.ddi_selector.show()
            self.ddi_selector_label.show()
            self.ddi_selector.setCurrentText(SELECTOR_TYPES[selected_ddi.selection_type])
        else:
            self.ddi_selector.hide()
            self.ddi_selector_label.hide()

        if 'VALUE     ' in selected_ddi.items.keys():
            self.ddi_value.show()
            self.ddi_value_label.show()
            self.ddi_value.setText(selected_ddi.items['VALUE     '])
        else:
            self.ddi_value.setText('')
            self.ddi_value.hide()
            self.ddi_value_label.hide()




        # for item in element.findall(SCHEME_PREFIX+'ITEM'):
        #    - VALUE
        #    -
        # self.existing = bool(element.get('EXISTING'))
        # self.valid = bool(element.get('VALID'))
        # for siphon in siphons_element.findall(SCHEME_PREFIX+'SIPHON'):

    def import_uj(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
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

app = QtWidgets.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()