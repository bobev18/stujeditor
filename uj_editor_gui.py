import os
from userjourney import UserJourney

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem)

DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.create_top_group(), 0, 0)
        grid.addWidget(self.create_mid_group(), 1, 0)
        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        self.resize(1280, 640)
        # self.create_actions()

    def __wiggets_to_layout(self, layout, *widgets):
        for widget in widgets:
            layout.addWidget(widget)

    def create_top_group(self):
        group_box = QGroupBox()
        import_button = QPushButton('&Import UJ')
        import_button.clicked.connect(self.import_uj)
        export_button = QPushButton('&Export UJ')
        export_button.clicked.connect(self.export_uj)
        uj_name_label = QLabel('UJ Name')
        self.uj_name = QLineEdit()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, import_button, export_button, uj_name_label, self.uj_name)
        group_box.setLayout(hbox)

        return group_box

    def create_mid_group(self):
        group_box = QGroupBox()
        self.ddi_tree = QTreeWidget()
        self.ddi_tree.itemSelectionChanged.connect(self.show_ddi_details)
        ddi_details_layout = QGridLayout()
        ddi_details_layout.setContentsMargins(0,0,0,0)
        ddi_details_layout.addWidget(self.create_common_ddi_details())
        ddi_details_layout.addWidget(self.create_specific_ddi_details())
        ddi_details = QGroupBox()
        ddi_details.setLayout(ddi_details_layout)

        self.step_tree = QTreeWidget()
        self.step_tree.itemSelectionChanged.connect(self.show_step_details)
        step_details = QGroupBox()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, self.ddi_tree, ddi_details, self.step_tree, step_details)
        group_box.setLayout(hbox)
        return group_box

    def create_common_ddi_details(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(vbox, self.create_ddi_type_and_name(), self.create_ddi_description(), self.create_ddi_shared(), self.create_ddi_refresh())
        group_box.setLayout(vbox)
        return group_box

    def create_ddi_description(self):
        group_box = QGroupBox()
        ddi_description_label = QLabel()
        ddi_description_label.setText('Description')
        self.ddi_description = QLineEdit()
        # self.ddi_description.setFixedHeight(60)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(ddi_description_label)
        hbox.addWidget(self.ddi_description)
        group_box.setLayout(hbox)
        return group_box

    def create_ddi_type_and_name(self):
        group_box = QGroupBox()
        # DDI Name
        ddi_name_label = QLabel()
        ddi_name_label.setText('DDI Name')
        self.ddi_name = QLineEdit()
        # DDI Type
        ddi_type_label = QLabel()
        ddi_type_label.setText('Type')
        self.ddi_type = QComboBox()
        self.ddi_type.addItems(DDI_TYPES.values())
        self.ddi_type.setCurrentText('')

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, ddi_type_label, self.ddi_type, ddi_name_label, self.ddi_name)
        group_box.setLayout(hbox)
        return group_box

    def create_ddi_shared(self):
        group_box = QGroupBox('Sharing selector state:')
        self.ddi_shared_one = QRadioButton('&Single User')
        self.ddi_shared_all = QRadioButton('&All UJ Users')
        self.shared_button_mapping = {'SCRIPT  ': self.ddi_shared_one, 'THREAD  ': self.ddi_shared_all}
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, self.ddi_shared_one, self.ddi_shared_all)
        group_box.setLayout(hbox)
        return group_box

    def create_ddi_refresh(self):
        group_box = QGroupBox('Refresh triggers:')
        self.ddi_refresh_once_per_run = QRadioButton('Once per Run')
        self.ddi_refresh_once_per_user = QRadioButton('Once per User')
        self.ddi_refresh_every_cycle = QRadioButton('Every Cycle')
        self.ddi_refresh_every_time = QRadioButton('Every Time')
        self.refresh_button_mapping = {'C': self.ddi_refresh_every_cycle, 'R': self.ddi_refresh_once_per_run, 'T': self.ddi_refresh_every_time, 'U': self.ddi_refresh_once_per_user}
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, self.ddi_refresh_once_per_run, self.ddi_refresh_once_per_user, self.ddi_refresh_every_cycle, self.ddi_refresh_every_time)
        group_box.setLayout(hbox)
        return group_box

    def create_specific_ddi_details(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(vbox, self.create_ddi_value(), self.create_ddi_selector())
        group_box.setLayout(vbox)
        return group_box

    def create_ddi_value(self):
        group_box = QGroupBox()
        ddi_value_label = QLabel()
        ddi_value_label.setText('Value')
        self.ddi_value = QLineEdit()
        # self.ddi_value.setText('')

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, ddi_value_label, self.ddi_value)
        group_box.setLayout(hbox)
        return group_box

    def create_ddi_selector(self):
        group_box = QGroupBox()

        ddi_selector_label = QLabel()
        ddi_selector_label.setText('Selector')
        self.ddi_selector = QComboBox()
        self.ddi_selector.addItems(SELECTOR_TYPES.values())

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__wiggets_to_layout(hbox, ddi_selector_label, self.ddi_selector)
        group_box.setLayout(hbox)
        return group_box

    # def create_actions(self):
    #     self.import_act = QAction("&Import...", self, shortcut="Ctrl+I", triggered=self.import_uj)
    #     self.export_act = QAction("&Export...", self, shortcut="Ctrl+E", triggered=self.export_uj)

    def import_uj(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.uj = UserJourney('Update Purchase Order User Journey.xml')
        self.uj_name.setText(self.uj.name)

        ddi_nodes = []
        for ddi in self.uj.dditems:
            new_ddi_node = QTreeWidgetItem()
            new_ddi_node.setText(0, ddi.name)
            ddi_nodes.append(new_ddi_node)

        self.ddi_tree.addTopLevelItems(ddi_nodes)

        groupnodes = []
        for stepgroup in self.uj.stepgroups:
            new_group_node = QTreeWidgetItem()
            new_group_node.setText(0, stepgroup.name)
            stepnodes = []
            for step in stepgroup.steps:
                new_step_node = QTreeWidgetItem(new_group_node)
                new_step_node.setText(0, step.name)
                stepnodes.append(new_step_node)

            groupnodes.append(new_group_node)


        self.step_tree.addTopLevelItems(groupnodes)

    def export_uj(self):
        pass

    def show_ddi_details(self):
        selected_ddi_name = self.ddi_tree.selectedItems()[0].text(0)
        self.ddi_name.setText(selected_ddi_name)
        selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)

        self.ddi_description.setText(selected_ddi.description)
        self.ddi_type.setCurrentText(DDI_TYPES[selected_ddi.type])
        self.shared_button_mapping[selected_ddi.scope].setChecked(1)
        self.refresh_button_mapping[selected_ddi.lifecycle].setChecked(1)

        if selected_ddi.selection_type in SELECTOR_TYPES.keys():
            self.ddi_selector.show()
            # self.ddi_selector_label.show()
            self.ddi_selector.setCurrentText(SELECTOR_TYPES[selected_ddi.selection_type])
        else:
            self.ddi_selector.hide()
            # self.ddi_selector_label.hide()

        if 'VALUE     ' in selected_ddi.items.keys():
            self.ddi_value.show()
            # self.ddi_value_label.show()
            self.ddi_value.setText(selected_ddi.items['VALUE     '])
        else:
            self.ddi_value.setText('')
            self.ddi_value.hide()
            # self.ddi_value_label.hide()




        # for item in element.findall(SCHEME_PREFIX+'ITEM'):
        #    - VALUE
        #    -
        # self.existing = bool(element.get('EXISTING'))
        # self.valid = bool(element.get('VALID'))
        # for siphon in siphons_element.findall(SCHEME_PREFIX+'SIPHON'):



    def show_step_details(self):
        pass



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
