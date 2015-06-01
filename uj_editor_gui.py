import os
from userjourney import UserJourney
from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget, QButtonGroup,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLayout,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem)

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
        self.layout.addWidget(self.line_edit)

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
        self.layout.addWidget(self.combo_box)

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

    def hide(self):
        for button in self.buttons.values():
            button.hide()

    def set_text(self, key):
        if key != '':
            self.buttons[key].setChecked(1)




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
        vbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(vbox, self.create_ddi_type_and_name(), self.create_ddi_description(), self.create_ddi_shared(), self.create_ddi_refresh())
        group_box.setLayout(vbox)
        return group_box

    def create_ddi_description(self):
        self.ddi_description = LabelLineEdit('Description')
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addLayout(self.ddi_description.layout)
        return hbox

    def create_ddi_type_and_name(self):
        self.ddi_name = LabelLineEdit('DDI Name')
        self.ddi_type = LabelComboBox('Type', DDI_TYPES.values())
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(hbox, self.ddi_type.layout, self.ddi_name.layout)
        return hbox

    def create_ddi_shared(self):
        self.shared_button_group = LabelButtonGroup('State Sharing', {'SCRIPT  ': '&Single User', 'THREAD  ': '&All Run Users'})
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addLayout(self.shared_button_group.layout)
        return hbox

    def create_ddi_refresh(self):
        self.refresh_button_group = LabelButtonGroup('Refresh Condition', {'C': 'Every Cycle', 'R': 'Once per Run', 'T': 'Every Time', 'U': 'Once per User'})
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addLayout(self.refresh_button_group.layout)
        return hbox

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
        # self.__mix_to_layout(self.ddi_specific_layout, self.value_layout)
        # self.__mix_to_layout(self.ddi_specific_layout, self.value_layout, self.create_ddi_selector(), self.create_ddi_date_fields(), self.create_delimited_file_picker(),
                                 # self.create_column_index(), self.create_delimiter())
        group_box.setLayout(self.ddi_specific_layout)
        return group_box


    # def create_ddi_selector(self):
    #     self.ddi_selector = LabelComboBox('Selector')
    #     self.ddi_selector.addItems(SELECTOR_TYPES.values())
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_selector.label, self.ddi_selector)
    #     return hbox

    # def create_ddi_date_fields(self):
    #     # self.date_group_box = QGroupBox()
    #     vbox = QVBoxLayout()
    #     vbox.setContentsMargins(0,0,0,0)
    #     self.__mix_to_layout(vbox, self.create_date_starting_point(), self.create_date_fixed_edit(), self.create_date_offset_selector(),
    #                              self.create_date_offset_box1(), self.create_date_offset_box2(), self.create_date_format())
    #     # self.date_group_box.setLayout(vbox)
    #     # return self.date_group_box
    #     return vbox

    # def create_date_starting_point(self):
    #     # group_box = QGroupBox('Starting Point:')

    #     self.ddi_date_starting_now = QRadioButton('Now')
    #     self.ddi_date_starting_today = QRadioButton('Today')
    #     self.ddi_date_starting_fixed = QRadioButton('Fixed Value')
    #     self.ddi_date_starting_related = QRadioButton('Another Date DDI')
    #     date_starting_button_mapping = {'now': self.ddi_date_starting_now, 'today': self.ddi_date_starting_today,
    #                                          'fixed value': self.ddi_date_starting_fixed, 'another date': self.ddi_date_starting_related}

    #     self.ddi_date_starting_point = MyButtonGroup(date_starting_button_mapping)
    #     self.ddi_date_starting_point.addButton(self.ddi_date_starting_now)
    #     self.ddi_date_starting_point.addButton(self.ddi_date_starting_today)
    #     self.ddi_date_starting_point.addButton(self.ddi_date_starting_fixed)
    #     self.ddi_date_starting_point.addButton(self.ddi_date_starting_related)
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_starting_now, self.ddi_date_starting_today, self.ddi_date_starting_fixed, self.ddi_date_starting_related)
    #     # group_box.setLayout(hbox)
    #     # return group_box
    #     return hbox

    # def create_date_fixed_edit(self):
    #     self.ddi_date_starting_fixed_edit = LabelLineEdit('Fixed Date:')
    #     self.ddi_date_starting_related_edit = LabelComboBox('Another DDI:')
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_starting_fixed_edit.label, self.ddi_date_starting_fixed_edit, self.ddi_date_starting_related_edit.label, self.ddi_date_starting_related_edit)
    #     return hbox

    # def create_date_offset_selector(self):
    #     # group_box = QGroupBox('Offset:')

    #     self.ddi_date_offset_none = QRadioButton('None')
    #     self.ddi_date_offset_fixed = QRadioButton('Fixed')
    #     self.ddi_date_offset_random = QRadioButton('Random')
    #     ddi_date_offset_button_mapping = {'none': self.ddi_date_offset_none, 'fixed': self.ddi_date_offset_fixed, 'random': self.ddi_date_offset_random}

    #     self.ddi_date_offset = MyButtonGroup(ddi_date_offset_button_mapping)
    #     self.ddi_date_offset.addButton(self.ddi_date_offset_none)
    #     self.ddi_date_offset.addButton(self.ddi_date_offset_fixed)
    #     self.ddi_date_offset.addButton(self.ddi_date_offset_random)
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_offset_none, self.ddi_date_offset_fixed, self.ddi_date_offset_random)
    #     # group_box.setLayout(hbox)
    #     # return group_box
    #     return hbox

    # def create_date_offset_box1(self):
    #     # self.offset1_group_box = QGroupBox()

    #     self.ddi_date_offset1_sign = LabelComboBox('')
    #     self.ddi_date_offset1_sign.addItems(['+', '-'])
    #     self.ddi_date_offset1_amount = LabelLineEdit('')
    #     self.ddi_date_offset1_amount.setInputMask('99999999')
    #     self.ddi_date_offset1_unit = LabelComboBox('')
    #     self.ddi_date_offset1_unit.addItems(['sec', 'min', 'hrs', 'day'])

    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_offset1_sign, self.ddi_date_offset1_amount, self.ddi_date_offset1_unit)
    #     # self.offset1_group_box.setLayout(hbox)
    #     # return self.offset1_group_box
    #     return hbox

    # def create_date_offset_box2(self):
    #     # self.offset2_group_box = QGroupBox()

    #     self.ddi_date_offset2_sign = LabelComboBox('')
    #     self.ddi_date_offset2_sign.addItems(['+', '-'])
    #     self.ddi_date_offset2_amount = LabelLineEdit('')
    #     self.ddi_date_offset2_amount.setInputMask('99999999')
    #     self.ddi_date_offset2_unit = LabelComboBox('')
    #     self.ddi_date_offset2_unit.addItems(['sec', 'min', 'hrs', 'day'])

    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_offset2_sign, self.ddi_date_offset2_amount, self.ddi_date_offset2_unit)
    #     # self.offset2_group_box.setLayout(hbox)
    #     # return self.offset2_group_box
    #     return hbox

    # def create_date_format(self):
    #     self.ddi_date_format = LabelLineEdit('Date Format:')
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_date_format.label, self.ddi_date_format)
    #     return hbox

    # def create_delimited_file_picker(self):
    #     # self.file_picker_group_box = QGroupBox()
    #     self.ddi_delimited_filename = LabelLineEdit('File Name:')
    #     self.ddi_delimited_file_picker_button = QPushButton('&Load Data File')
    #     self.ddi_delimited_file_picker_button.clicked.connect(self.load_data_file)

    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_delimited_filename.label, self.ddi_delimited_filename, self.ddi_delimited_file_picker_button)
    #     # self.file_picker_group_box.setLayout(hbox)
    #     # return self.file_picker_group_box
    #     return hbox

    # def create_delimiter(self):
    #     # self.delimiter_group_box = QGroupBox()
    #     self.ddi_delimiter_character = LabelLineEdit('Delimiter:')
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_delimiter_character.label, self.ddi_delimiter_character)
    #     # self.delimiter_group_box.setLayout(hbox)
    #     # return self.delimiter_group_box
    #     return hbox

    # def create_column_index(self):
    #     # self.column_index_group_box = QGroupBox()
    #     self.ddi_column_index = LabelLineEdit('Column Index:')
    #     self.ddi_column_index.setInputMask('999')
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0,0,0,0)
    #     self.__wiggets_to_layout(hbox, self.ddi_column_index.label, self.ddi_column_index)
    #     # self.column_index_group_box.setLayout(hbox)
    #     # return self.column_index_group_box
    #     return hbox




# ------------------------------------------------------ end of creations ----------------------------------------------------------

    # def create_actions(self):
    #     self.import_act = QAction("&Import...", self, shortcut="Ctrl+I", triggered=self.import_uj)
    #     self.export_act = QAction("&Export...", self, shortcut="Ctrl+E", triggered=self.export_uj)

    def load_data_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.ddi_delimited_filename.setText(filename[0])
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
        self.ddi_name.set_text(selected_ddi_name)
        self.selected_ddi = self.uj.find_ddi_by_name(selected_ddi_name)

        self.ddi_description.set_text(self.selected_ddi.description)
        self.ddi_type.set_text(DDI_TYPES[self.selected_ddi.type])
        self.shared_button_group.set_text(self.selected_ddi.scope)
        self.refresh_button_group.set_text(self.selected_ddi.lifecycle)

        # Specific

        if isinstance(self.selected_ddi, ConstantDDI):
            self.ddi_value_widget.show()
            self.ddi_value_widget.set_text(self.selected_ddi.value)
        else:
            self.ddi_value_widget.hide()

        if isinstance(self.selected_ddi, ListDDI):
            self.ddi_selector_widget.show()
            self.ddi_selector_widget.set_text(self.selected_ddi.selection_type)
        else:
            self.ddi_selector_widget.hide()




        # ddi_specific_fields = [
        #     # self.ddi_date_offset,
        #     # self.ddi_date_starting_point,
        #     # self.ddi_date_format,
        #     # self.ddi_date_offset1_amount,
        #     # self.ddi_date_offset1_sign,
        #     # self.ddi_date_offset1_unit,
        #     # self.ddi_date_offset2_amount,
        #     # self.ddi_date_offset2_sign,
        #     # self.ddi_date_offset2_unit,
        #     # self.ddi_date_starting_fixed_edit,
        #     # self.ddi_date_starting_related_edit,
        #     self.value_widget,
        #     # self.ddi_selector,
        #     # self.ddi_column_index,
        #     # self.ddi_delimited_filename,
        #     # self.ddi_delimited_file_picker_button,
        #     # self.ddi_delimiter_character,
        # ]

        # print ('specific layout', self.ddi_specific_layout.children())
        # # ddi_specific_field_layouts = [
        # #     self.create_ddi_value(),
        # #     self.create_ddi_selector(),
        # #     self.create_ddi_date_fields(),
        # #     self.create_delimited_file_picker(),
        # #     self.create_column_index(),
        # #     self.create_delimiter(),
        # # ]

        # ddi_type_mappings = {
        #     # ConstantDDI: {'layout': '', 'vlaues': [(self.ddi_value, 'value')] },
        #     ConstantDDI: {self.value_widget: 'value'},
        #     DateDDI: {
        #         # self.ddi_date_starting_point: 'starting_point',
        #         # self.ddi_date_starting_fixed_edit: 'starting_value',
        #         # self.ddi_date_starting_related_edit: 'starting_value',
        #         # self.ddi_date_offset: 'offset_type',
        #         # self.ddi_date_offset1_sign: 'first_offset_sign',
        #         # self.ddi_date_offset1_amount: 'first_offset_value',
        #         # self.ddi_date_offset1_unit: 'first_offset_unit',
        #         # self.ddi_date_offset2_sign: 'second_offset_sign',
        #         # self.ddi_date_offset2_amount: 'second_offset_value',
        #         # self.ddi_date_offset2_unit: 'second_offset_unit',
        #         # self.ddi_date_format: 'format',
        #     },
        #     DelimitedFileDDI: {
        #         # self.ddi_delimited_filename: 'file_name', self.ddi_delimited_file_picker_button: 'None', self.ddi_column_index: 'column', self.ddi_delimiter_character: 'delimiter'
        #     },
        #     ListDDI: {},
        #     # VariableDDI: {self.ddi_value: 'value'},
        #     # RelatedDDI: {self.ddi_column_index: 'column'},
        #     # ResponseDDI: {self.ddi_column_index: 'column'},
        #     VariableDDI: {},
        #     RelatedDDI: {},
        #     ResponseDDI: {},
        #     AutoCorrelatedDDI: {},
        #     AutoIncrementDDI: {},
        # }

        # object_attribute_pairs = ddi_type_mappings[type(self.selected_ddi)]
        # # print('obj', object_attribute_pairs )
        # for field in ddi_specific_fields:
        #     # print('field', field, 'keys', object_attribute_pairs.keys())
        #     if field in object_attribute_pairs.keys():
        #         value = ''
        #         # if object_attribute_pairs[field] != None:
        #         if object_attribute_pairs[field] == 'value':
        #             self.ddi_specific_layout.addWidget(field)

        #         else:

        #             try:
        #                 value = str(getattr(self.selected_ddi, object_attribute_pairs[field]))
        #             except AttributeError:
        #                 pass
        #             field.set_text(value)
        #             if value != '':
        #                 field.show()
        #     else:
        #         # if isinstance(field, list):
        #         #     # self.ddi_date_offset_button_mapping[self.selected_ddi.offset_type].setChecked(1)
        #         #     field[getattr(self.selected_ddi, object_attribute_pairs[field])].setChecked(1)
        #         # else:
        #         #     field.set_text('')
        #         #     field.hide()

        #         # try:
        #         #     field.set_text('')
        #         #     field.hide()
        #         # except AttributeError:
        #         #     pass
        #         if not isinstance(field, QPushButton):
        #             self.ddi_specific_layout.removeWidget(field)
        #             self.ddi_specific_layout.update()
        #             # field.set_text('')
        #             # field.hide()



        # if self.selected_ddi.selection_type in SELECTOR_TYPES.keys():
        #     self.ddi_selector.show()
        #     # self.ddi_selector_label.show()
        #     self.ddi_selector.setCurrentText(SELECTOR_TYPES[self.selected_ddi.selection_type])
        # else:
        #     self.ddi_selector.hide()
        #     # self.ddi_selector_label.hide()

        # if 'VALUE     ' in self.selected_ddi.items.keys():
        #     self.ddi_value.show()
        #     # self.ddi_value_label.show()
        #     self.ddi_value.setText(self.selected_ddi.items['VALUE     '])
        # else:
        #     self.ddi_value.setText('')
        #     self.ddi_value.hide()
        #     # self.ddi_value_label.hide()


        # self.ddi_date_starting_fixed.hide()
        # self.ddi_date_starting_related.hide()
        # self.offset1_group_box.hide()
        # self.offset2_group_box.hide()
        # self.date_group_box.hide()
        # if isinstance(self.selected_ddi, DateDDI):
        #     self.date_group_box.show()
        #     self.date_starting_button_mapping[self.selected_ddi.starting_point].setChecked(1)
        #     self.ddi_date_offset_button_mapping[self.selected_ddi.offset_type].setChecked(1)
        #     self.ddi_date_format.setText(self.selected_ddi.format)

        #     if self.selected_ddi.starting_point == 'fixed value':
        #         self.ddi_date_starting_fixed.show()
        #     if self.selected_ddi.starting_point == 'another date':
        #         self.ddi_date_starting_related.show()

        #     if self.selected_ddi.offset_type != 'none':
        #         self.offset1_group_box.show()
        #         self.ddi_date_offset1_sign.setCurrentText(self.selected_ddi.first_offset_sign)
        #         self.ddi_date_offset1_amount.setText(str(self.selected_ddi.first_offset_value))
        #         self.ddi_date_offset1_unit.setCurrentText(self.selected_ddi.first_offset_unit[:-3])

        #     if self.selected_ddi.offset_type == 'random':
        #         self.offset2_group_box.show()
        #         self.ddi_date_offset2_sign.setCurrentText(self.selected_ddi.second_offset_sign)
        #         self.ddi_date_offset2_amount.setText(str(self.selected_ddi.second_offset_value))
        #         self.ddi_date_offset2_unit.setCurrentText(self.selected_ddi.second_offset_unit[:-3])


        # else:
        #     self.ddi_date_starting_point.setExclusive(False)
        #     self.ddi_date_offset.setExclusive(False)
        #     [ z.setChecked(False) for z in self.date_starting_button_mapping.values() ]
        #     [ z.setChecked(False) for z in self.ddi_date_offset_button_mapping.values() ]
        #     self.ddi_date_starting_point.setExclusive(True)
        #     self.ddi_date_offset.setExclusive(True)
        #     self.ddi_date_format.setText('')

        # self.file_picker_group_box.hide()
        # self.column_index_group_box.hide()
        # self.delimiter_group_box.hide()
        # if isinstance(self.selected_ddi, DelimitedFileDDI):
        #     self.ddi_delimited_filename.setText(self.selected_ddi.file_name)
        #     self.ddi_column_index.setText(str(self.selected_ddi.column))
        #     self.ddi_delimiter_character.setText(self.selected_ddi.delimiter)
        #     self.file_picker_group_box.show()
        #     self.column_index_group_box.show()
        #     self.delimiter_group_box.show()




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
