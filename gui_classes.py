# import os
# from userjourney import UserJourney
# from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget, QButtonGroup,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLayout,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem)

# DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
# SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}


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
    def __init__(self, label='', items = {'UJ object reference value': 'Name to show'}):
        super(LabelComboBox, self).__init__()
        self.label = QLabel()
        self.label.setText(label)
        self.items = items
        self.combo_box = QComboBox()
        self.combo_box.insertItems(0, self.items.values())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box, stretch = 1)

    def reset_items(self, items = {'UJ object reference value': 'Name to show'}):
        while self.combo_box.count() != 0:
            self.combo_box.removeItem(0)
        self.items = items
        self.combo_box.addItems(self.items.values())

    def show(self):
        self.combo_box.show()
        self.label.show()

    def hide(self):
        self.combo_box.hide()
        self.label.hide()

    def set_text(self, text):
        if text in self.items.values():
            self.combo_box.setCurrentText(text)

        if text in self.items.keys():
            self.combo_box.setCurrentText(self.items[text])

    def text(self):
        return self.combo_box.currentText()

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

    def text(self):
        return self.button_group.checkedButton().text()

    def checked(self):
        return self.button_group.checkedButton()


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
    def __init__(self, date_related_ddis = []):
        super(DateFieldsGroup, self).__init__()
        self.starting_point = LabelButtonGroup('Starting Point:', { z:z for z in ['now', 'today', 'fixed value', 'another date'] } )
        self.fixed_value_edit = LabelLineEdit('Fixed Value:')
        self.starting_point.buttons['fixed value'].toggled.connect(self.toggle_fixed_value_edit)
        self.related_ddi_box = LabelComboBox('Related Date DDI:', { z:z for z in date_related_ddis})
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

    def set_values(self, starting_point, starting_fixed_edit, date_related_ddi, offset, format_, sign1='', amount1='', unit1='', sign2='', amount2='', unit2=''):
        self.starting_point.set_text(starting_point)
        self.fixed_value_edit.set_text(starting_fixed_edit)
        self.related_ddi_box.set_text(date_related_ddi)
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

    def get_values(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        table = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(self.table.item(i, j).text())
            table.append(row)

        return table

