import os
from userjourney import UserJourney
from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget, QButtonGroup,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLayout,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem)

DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}


class LabelLineEdit(QWidget):
    def __init__(self, label=''):
        super(LabelLineEdit, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.line_edit = QLineEdit()
        self.label = QLabel()
        self.label.setText(label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit, stretch = 1)

    def show(self):
        self.line_edit.show()
        self.label.show()

    def hide(self):
        self.line_edit.hide()
        self.label.hide()

    def set_text(self, text):
        self.line_edit.setText(text)

class LabelComboBox(QWidget):
    def __init__(self, label='', items = []):
        super(LabelComboBox, self).__init__()
        self.label = QLabel()
        self.label.setText(label)
        self.combo_box = QComboBox()
        self.combo_box.insertItems(0, items)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box, stretch = 1)

    def reset_items(self, items):
        # if self.combo_box.count() > 0:
        while self.combo_box.count() != 0:
            self.combo_box.removeItem(0)
        self.combo_box.addItems(items)

    def show(self):
        self.combo_box.show()
        self.label.show()

    def hide(self):
        self.combo_box.hide()
        self.label.hide()

    def set_text(self, text):
        self.combo_box.setCurrentText(text)

class LabelButtonGroup(QWidget):
    def __init__(self, label = '', buttons = {'UJ object reference value': 'Name to show'}):
        super(LabelButtonGroup, self).__init__()
        self.label = QLabel()
        self.label.setText(label)
        self.button_group = QButtonGroup()
        self.buttons = {}
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.label)
        for button_key in buttons.keys():
            self.buttons[button_key] = QRadioButton(buttons[button_key])
            self.button_group.addButton(self.buttons[button_key])
            self.layout.addWidget(self.buttons[button_key])

    def show(self):
        for button in self.buttons.values():
            button.show()
        self.label.show()

    def hide(self):
        for button in self.buttons.values():
            button.hide()
        self.label.hide()

    def set_text(self, key):
        if key != '':
            self.buttons[key].setChecked(1)

class OffsetRow(QWidget):
    def __init__(self):
        super(OffsetRow, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.sign = QComboBox()
        self.sign.addItems(['-', '+'])
        self.amount = QLineEdit()
        self.amount.setInputMask('99999999')
        self.unit = QComboBox()
        self.unit.addItems(['sec', 'min', 'hrs', 'day'])
        self.layout.addWidget(self.sign)
        self.layout.addWidget(self.amount, stretch = 1)
        self.layout.addWidget(self.unit)

    def show(self):
        self.sign.show()
        self.amount.show()
        self.unit.show()

    def hide(self):
        self.sign.hide()
        self.amount.hide()
        self.unit.hide()

    def set_values(self, sign, amount, unit):
        self.sign.setCurrentText(sign)
        self.amount.setText(str(amount))
        self.unit.setCurrentText(unit)


class DateFieldsGroup(QWidget):
    def __init__(self, starting_related_ddis = []):
        super(DateFieldsGroup, self).__init__()
        self.starting_point = LabelButtonGroup('Starting Point:', { z:z for z in ['now', 'today', 'fixed value', 'another date'] } )
        self.fixed_value_edit = LabelLineEdit('Fixed Value:')
        self.starting_point.buttons['fixed value'].toggled.connect(self.toggle_fixed_value_edit)
        self.related_ddi_box = LabelComboBox('Related Date DDI:', starting_related_ddis)
        self.starting_point.buttons['another date'].toggled.connect(self.toggle_another_date_dropbox)
        self.offset_type = LabelButtonGroup('Offset:', { z:z for z in ['none', 'fixed', 'random'] })
        self.offset1 = OffsetRow()
        self.offset2 = OffsetRow()
        self.offset_type.buttons['fixed'].toggled.connect(self.toggle_offset_details)
        self.offset_type.buttons['random'].toggled.connect(self.toggle_offset_details)
        self.format = LabelLineEdit('Format:')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addLayout(self.starting_point.layout)
        self.layout.addLayout(self.fixed_value_edit.layout)
        self.layout.addLayout(self.related_ddi_box.layout)
        self.layout.addLayout(self.offset_type.layout)
        self.layout.addLayout(self.offset1.layout)
        self.layout.addLayout(self.offset2.layout)
        self.layout.addLayout(self.format.layout)

    def toggle_fixed_value_edit(self):
        if self.starting_point.buttons['fixed value'].isChecked():
            self.fixed_value_edit.show()
        else:
            self.fixed_value_edit.hide()

    def toggle_another_date_dropbox(self):
        if self.starting_point.buttons['another date'].isChecked():
            self.related_ddi_box.show()
        else:
            self.related_ddi_box.hide()

    def toggle_offset_details(self):
        if self.offset_type.buttons['fixed'].isChecked():
            self.offset1.show()
            self.offset2.hide()
        elif self.offset_type.buttons['random'].isChecked():
            self.offset1.show()
            self.offset2.show()
        else:
            self.offset1.hide()
            self.offset2.hide()

    def show(self):
        self.starting_point.show()
        self.offset_type.show()
        self.format.show()
        self.toggle_fixed_value_edit()
        self.toggle_another_date_dropbox()
        self.toggle_offset_details()

    def hide(self):
        self.starting_point.hide()
        self.offset_type.hide()
        self.format.hide()
        self.fixed_value_edit.hide()
        self.related_ddi_box.hide()
        self.offset1.hide()
        self.offset2.hide()

    def set_values(self, starting_point, starting_fixed_edit, starting_related_ddi, offset, format_, sign1='', amount1='', unit1='', sign2='', amount2='', unit2=''):
        self.starting_point.set_text(starting_point)
        self.fixed_value_edit.set_text(starting_fixed_edit)
        self.related_ddi_box.set_text(starting_related_ddi)
        self.offset_type.set_text(offset)
        self.format.set_text(format_)
        self.offset1.set_values(sign1, amount1, unit1)
        self.offset2.set_values(sign2, amount2, unit2)

class MyTableWidget(QWidget):
    def __init__(self, items = [['']]):
        super(MyTableWidget, self).__init__()
        self.table = QTableWidget(len(items), len(items[0]))
        self.add_row_button = QPushButton('Add Row')
        self.add_row_button.clicked.connect(self.add_row)
        self.delete_row_button = QPushButton('Delete Row')
        self.delete_row_button.clicked.connect(self.delete_row)
        self.add_column_button = QPushButton('Add Column')
        self.add_column_button.clicked.connect(self.add_column)
        self.delete_column_button = QPushButton('Delete Column')
        self.delete_column_button.clicked.connect(self.delete_column)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.add_row_button)
        hbox.addWidget(self.delete_row_button)
        hbox.addWidget(self.add_column_button)
        hbox.addWidget(self.delete_column_button)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addLayout(hbox)
        self.layout.addWidget(self.table)

    def add_row(self):
        self.table.setRowCount(self.table.rowCount()+1)

    def delete_row(self):
        self.table.removeRow(self.table.currentRow())

    def add_column(self):
        self.table.setColumnCount(self.table.columnCount()+1)

    def delete_column(self):
        self.table.removeColumn(self.table.currentColumn())

    def show(self):
        self.table.show()
        self.add_row_button.show()
        self.delete_row_button.show()
        self.add_column_button.show()
        self.delete_column_button.show()

    def hide(self):
        self.table.hide()
        self.add_row_button.hide()
        self.delete_row_button.hide()
        self.add_column_button.hide()
        self.delete_column_button.hide()

    def set_values(self, items):
        self.table.setRowCount(len(items))
        self.table.setColumnCount(len(items[0]))
        for i, row in enumerate(items):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.table.setItem(i, j, item)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.create_top_group(), 0, 0)
        grid.addWidget(self.create_mid_group(), 1, 0)
        self.setLayout(grid)

        self.setWindowTitle("UJ Editor")
        self.resize(1280, 640)
        # self.create_actions()

    # def __wiggets_to_layout(self, layout, *widgets):
    #     for widget in widgets:
    #         layout.addWidget(widget)

    def __mix_to_layout(self, layout, *mix):
        for item in mix:
            if isinstance(item, QWidget):
                layout.addWidget(item)
            if isinstance(item, QLayout):
                layout.addLayout(item)

    def create_top_group(self):
        group_box = QGroupBox()
        import_button = QPushButton('&Import UJ')
        import_button.clicked.connect(self.import_uj)
        export_button = QPushButton('&Export UJ')
        export_button.clicked.connect(self.export_uj)
        self.uj_name = LabelLineEdit('UJ Name')
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(hbox, import_button, export_button, self.uj_name.layout)
        group_box.setLayout(hbox)

        return group_box

    def create_mid_group(self):
        group_box = QGroupBox()
        self.ddi_tree = QTreeWidget()
        self.ddi_tree.itemSelectionChanged.connect(self.show_ddi_details)

        ddi_details = QGroupBox()
        ddi_details_layout = QGridLayout()
        ddi_details_layout.setContentsMargins(0,0,0,0)
        ddi_details_layout.addWidget(self.create_common_ddi_details(), 0, 0, 1, 1)
        ddi_details_layout.addWidget(self.create_specific_ddi_details(), 1, 0, 3, 1)
        ddi_details.setLayout(ddi_details_layout)

        self.step_tree = QTreeWidget()
        self.step_tree.itemSelectionChanged.connect(self.show_step_details)
        step_details = QGroupBox()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(hbox, self.ddi_tree, ddi_details, self.step_tree, step_details)
        group_box.setLayout(hbox)
        return group_box

    def create_common_ddi_details(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        self.ddi_description = LabelLineEdit('Description')
        type_name_layout = QHBoxLayout()
        type_name_layout.setContentsMargins(0,0,0,0)
        self.ddi_name = LabelLineEdit('DDI Name')
        self.ddi_type = LabelComboBox('Type', DDI_TYPES.values())
        self.__mix_to_layout(type_name_layout, self.ddi_type.layout, self.ddi_name.layout)
        self.ddi_sharing = LabelButtonGroup('State Sharing', {'SCRIPT  ': '&Single User', 'THREAD  ': '&All Run Users'})
        self.ddi_refresh = LabelButtonGroup('Refresh Condition', {'C': 'Every Cycle', 'R': 'Once per Run', 'T': 'Every Time', 'U': 'Once per User'})
        vbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(vbox, type_name_layout, self.ddi_description.layout, self.ddi_sharing.layout, self.ddi_refresh.layout)
        group_box.setLayout(vbox)
        return group_box


    # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
    def create_specific_ddi_details(self):
        group_box = QGroupBox()
        self.ddi_specific_layout = QVBoxLayout()
        self.ddi_specific_layout.setContentsMargins(0,0,0,0)
        # self.value_layout = self.create_ddi_value()
        self.ddi_value_widget = LabelLineEdit('Value')
        self.ddi_selector_widget = LabelComboBox('Selector', SELECTOR_TYPES.values())
        # self.ddi_specific_layout.addWidget(self.ddi_value_widget)
        self.ddi_specific_layout.addLayout(self.ddi_value_widget.layout)
        self.ddi_specific_layout.addLayout(self.ddi_selector_widget.layout)

        self.ddi_date = DateFieldsGroup()
        self.ddi_specific_layout.addLayout(self.ddi_date.layout)

        self.ddi_delimiter_character_widget = LabelLineEdit('Delimiter:')
        self.ddi_delimiter_character_widget.line_edit.setMaxLength(1)
        self.ddi_delimited_filename_widget = LabelLineEdit('File Name:')
        self.ddi_delimited_file_picker_button = QPushButton('&Load Data File')
        self.ddi_delimited_file_picker_button.clicked.connect(self.load_data_file)
        delimited_layout = QHBoxLayout()
        delimited_layout.setContentsMargins(0,0,0,0)
        delimited_layout.addLayout(self.ddi_delimiter_character_widget.layout, stretch = 0)
        delimited_layout.addLayout(self.ddi_delimited_filename_widget.layout, stretch = 2)
        delimited_layout.addWidget(self.ddi_delimited_file_picker_button, stretch = 1)
        self.ddi_specific_layout.addLayout(delimited_layout)

        self.ddi_column_index_widget = LabelLineEdit('Column Index:')
        self.ddi_column_index_widget.line_edit.setInputMask('999')
        self.ddi_specific_layout.addLayout(self.ddi_column_index_widget.layout)

        self.ddi_list_table = MyTableWidget()
        self.ddi_specific_layout.addLayout(self.ddi_list_table.layout)




        group_box.setLayout(self.ddi_specific_layout)
        return group_box


# ------------------------------------------------------ end of creations ----------------------------------------------------------

    # def create_actions(self):
    #     self.import_act = QAction("&Import...", self, shortcut="Ctrl+I", triggered=self.import_uj)
    #     self.export_act = QAction("&Export...", self, shortcut="Ctrl+E", triggered=self.export_uj)

    def load_data_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.ddi_delimited_filename_widget.set_text(filename[0])
        self.selected_ddi.file_name = filename

    def import_uj(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.uj = UserJourney(filename[0])
        self.uj_name.set_text(self.uj.name)

        ddi_nodes = []
        for ddi in self.uj.dditems:
            new_ddi_node = QTreeWidgetItem()
            new_ddi_node.setText(0, ddi.name)
            ddi_nodes.append(new_ddi_node)

        self.ddi_tree.addTopLevelItems(ddi_nodes)

        date_type_ddis = self.uj.find_ddis_by_attribute('type', 'DATE    ')
        if date_type_ddis:
            self.ddi_date.related_ddi_box.reset_items([z.name for z in date_type_ddis])

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
        self.selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)

        # Common
        self.ddi_name.set_text(selected_ddi_name)
        self.ddi_description.set_text(self.selected_ddi.description)
        self.ddi_type.set_text(DDI_TYPES[self.selected_ddi.type])
        self.ddi_sharing.set_text(self.selected_ddi.scope)
        self.ddi_refresh.set_text(self.selected_ddi.lifecycle)

        # Specific
        ddi_specific_fields = [
            self.ddi_value_widget,
            self.ddi_selector_widget,
            self.ddi_delimiter_character_widget,
            self.ddi_delimited_filename_widget,
            self.ddi_delimited_file_picker_button,
            self.ddi_column_index_widget,
            self.ddi_date,
            self.ddi_list_table,
        ]

        ddi_type_mappings = {
            ConstantDDI: {self.ddi_value_widget: 'value'},
            DateDDI: {
                self.ddi_date: [
                                'starting_point',
                                'starting_value',
                                'starting_value',
                                'offset_type',
                                'format',
                                'first_offset_sign',
                                'first_offset_value',
                                'first_offset_unit',
                                'second_offset_sign',
                                'second_offset_value',
                                'second_offset_unit',
                                ]
            },
            DelimitedFileDDI: {
                self.ddi_delimiter_character_widget: 'delimiter',
                self.ddi_delimited_filename_widget: 'file_name',
                self.ddi_delimited_file_picker_button: '',
                self.ddi_column_index_widget: 'column',
                self.ddi_selector_widget: 'selection_type',
            },
            ListDDI: {self.ddi_selector_widget: 'selection_type', self.ddi_column_index_widget: 'column', self.ddi_list_table: ['table']},
            VariableDDI: {self.ddi_value_widget: 'value'},
            # RelatedDDI: {self.ddi_column_index: 'column'},
            # ResponseDDI: {self.ddi_column_index: 'column'},
            VariableDDI: {},
            RelatedDDI: {},
            ResponseDDI: {},
            AutoCorrelatedDDI: {},
            AutoIncrementDDI: {},
        }

        object_attribute_pairs = ddi_type_mappings[type(self.selected_ddi)]
        # print('obj', object_attribute_pairs )
        for field in ddi_specific_fields:
            # print('field', field, 'keys', object_attribute_pairs.keys())
            if field in object_attribute_pairs.keys():
                field.show()
                target_attribute_name = object_attribute_pairs[field]
                if isinstance(target_attribute_name, str):
                    if target_attribute_name != '':
                        value = str(getattr(self.selected_ddi, object_attribute_pairs[field]))
                        field.set_text(value)
                else:
                    values =[]
                    for attribute in target_attribute_name:
                        try:
                            # values.append(str(getattr(self.selected_ddi, attribute)))
                            values.append(getattr(self.selected_ddi, attribute))
                        except AttributeError:
                            pass
                        # print('values', values)
                    field.set_values(*values)
                    # where set_values(self, starting_point, starting_fixed_edit, starting_related_ddi, offset, sign1='', amount1=0, unit1='', sign2='', amount2=0, unit2=''):
                    #  i.e. the attributes that may be missing are set as optional arguments


            else:
                field.hide()



    def show_step_details(self):
        pass



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
