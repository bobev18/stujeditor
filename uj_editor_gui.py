import os
from userjourney import UserJourney
from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI
from gui_classes import LabelLineEdit, LabelComboBox, LabelButtonGroup, DateFieldsGroup, MyTableWidget, SiphonTableWidget, LabelCheckboxesGroup

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget, QButtonGroup,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QSplitter,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QPlainTextEdit)

DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}
STEP_REQUEST_TYPES = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']
STEP_CONTENT_TYPES = {'form': ['application/x-www-form-urlencoded', 'multipart/form-data'], 'binary': ['application/octet-stream', 'binary/octet-stream'], 'XML': ['text/html'], 'other': ['text/plain', 'application/json']}

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.create_top_group(), 0, 0)
        grid.addLayout(self.create_mid_group(), 1, 0)
        grid.addWidget(self.create_bottom_group(), 2, 0)
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
        self.import_button = QPushButton('&Import UJ')
        self.import_button.clicked.connect(self.import_uj)
        export_button = QPushButton('&Export UJ')
        export_button.clicked.connect(self.export_uj)
        self.uj_name = LabelLineEdit('UJ Name')
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.__mix_to_layout(hbox, self.import_button, export_button, self.uj_name.layout)
        group_box.setLayout(hbox)
        group_box.setMaximumHeight(60)
        return group_box

    def create_mid_group(self):
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
        step_details_layout = QGridLayout()
        step_details_layout.setContentsMargins(0,0,0,0)
        step_details_layout.addWidget(self.create_common_step_details(), 0, 0, 1, 1)
        step_details_layout.addWidget(self.create_specific_step_details(), 1, 0, 3, 1)
        step_details.setLayout(step_details_layout)

        splitter = QSplitter(self)
        splitter.addWidget(self.ddi_tree)
        splitter.addWidget(ddi_details)
        splitter.addWidget(self.step_tree)
        splitter.addWidget(step_details)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        # self.__mix_to_layout(hbox, self.ddi_tree, ddi_details, self.step_tree, step_details)
        hbox.addWidget(splitter)
        # group_box.setLayout(hbox)
        return hbox

    def create_bottom_group(self):
        group_box = QGroupBox()
        group_box.setMaximumHeight(200)
        self.debug_edit = QPlainTextEdit()
        self.debug_edit.setMaximumHeight(160)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        # hbox.setSizeConstraint(200)
        hbox.addWidget(self.debug_edit)
        group_box.setLayout(hbox)
        return group_box

    def create_common_ddi_details(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        self.ddi_description = LabelLineEdit('Description')
        type_name_layout = QHBoxLayout()
        type_name_layout.setContentsMargins(0,0,0,0)
        self.ddi_name = LabelLineEdit('DDI Name')
        self.ddi_type = LabelComboBox('Type', DDI_TYPES)
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
        self.ddi_selector_widget = LabelComboBox('Selector', SELECTOR_TYPES)
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

        self.ddi_related_ddi = LabelComboBox('Related to:')
        self.ddi_specific_layout.addLayout(self.ddi_related_ddi.layout)

        self.ddi_response_source_step = LabelComboBox('Source Step:')
        self.ddi_specific_layout.addLayout(self.ddi_response_source_step.layout)

        self.ddi_siphon_table = SiphonTableWidget()
        self.ddi_specific_layout.addLayout(self.ddi_siphon_table.layout)

        self.ddi_auto_correlate_type = LabelComboBox('Field Type:', { z:z for z in ['Repeated Fields', 'Known Fields'] })
        self.ddi_specific_layout.addLayout(self.ddi_auto_correlate_type.layout)
        self.ddi_auto_correlate_name = LabelComboBox('Field Name:')
        self.ddi_specific_layout.addLayout(self.ddi_auto_correlate_name.layout)
        self.ddi_auto_correlate_appears_in = LabelCheckboxesGroup('Appears In:', ['URL', 'Post', 'Headers'])
        self.ddi_specific_layout.addLayout(self.ddi_auto_correlate_appears_in.layout)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        self.ddi_auto_increment_starting_value = LabelLineEdit('Starting Value:')
        hbox.addLayout(self.ddi_auto_increment_starting_value.layout)
        self.ddi_auto_increment_increment = LabelLineEdit('Increment:')
        hbox.addLayout(self.ddi_auto_increment_increment.layout)
        self.ddi_auto_increment_prefix = LabelLineEdit('Prefix:')
        hbox.addLayout(self.ddi_auto_increment_prefix.layout)
        self.ddi_auto_increment_suffix = LabelLineEdit('Suffix:')
        hbox.addLayout(self.ddi_auto_increment_suffix.layout)
        self.ddi_auto_increment_min_lenght = LabelLineEdit('Minimum Length:')
        hbox.addLayout(self.ddi_auto_increment_min_lenght.layout)
        self.ddi_specific_layout.addLayout(hbox)

        group_box.setLayout(self.ddi_specific_layout)
        return group_box

    # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()

    def create_common_step_details(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        name_sleep_layout = QHBoxLayout()
        name_sleep_layout.setContentsMargins(0,0,0,0)
        self.step_name = LabelLineEdit('Name')
        name_sleep_layout.addLayout(self.step_name.layout)
        self.step_pre_time = LabelLineEdit('Sleep Time (sec)')
        name_sleep_layout.addLayout(self.step_pre_time.layout)
        vbox.addLayout(name_sleep_layout)
        self.step_description = LabelLineEdit('Description')
        vbox.addLayout(self.step_description.layout)
        self.step_checkboxes = LabelCheckboxesGroup('', ['Run First Cycle Only', 'Run Last Cycle Only', 'Count as Transaction', 'Process Response', 'Execute Separately'])
        vbox.addLayout(self.step_checkboxes.layout)
        request_type_content_type_layout = QHBoxLayout()
        self.request_type = LabelComboBox('Type', { z:z for z in STEP_REQUEST_TYPES })
        request_type_content_type_layout.addLayout(self.request_type.layout)
        self.content_type = LabelComboBox('Content-Type', { z:z for z in STEP_CONTENT_TYPES.keys() })
        request_type_content_type_layout.addLayout(self.content_type.layout)
        self.content_type.combo_box.currentIndexChanged[str].connect(self.update_content_subtypes)
        self.content_subtype = LabelComboBox('', { z:z for z in STEP_CONTENT_TYPES['form'] })
        request_type_content_type_layout.addLayout(self.content_subtype.layout)
        # what's the point of having type and subtypes? the one sent with headers is the subtype - it should be the only selection
        vbox.addLayout(request_type_content_type_layout)



        group_box.setLayout(vbox)
        return group_box


    def create_specific_step_details(self):
        pass




# ------------------------------------------------------ end of creations ----------------------------------------------------------

    # def create_actions(self):
    #     self.import_act = QAction("&Import...", self, shortcut="Ctrl+I", triggered=self.import_uj)
    #     self.export_act = QAction("&Export...", self, shortcut="Ctrl+E", triggered=self.export_uj)

    def update_content_subtypes(self, item):
        # item is supposed to be the text value of the combobox selection
        print('reached function update_content_subtypes with item=', item)


    def debug__(self, message):
        self.debug_edit.appendPlainText(message)

    def load_data_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.ddi_delimited_filename_widget.set_text(filename[0])
        self.selected_ddi.file_name = filename

    def import_uj(self, filename=[]):
        if not filename:
            filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.uj = UserJourney('')
        self.uj.import_uj(filename[0])
        self.uj_name.set_text(self.uj.name)

        ddi_nodes = []
        for ddi in self.uj.dditems:
            new_ddi_node = QTreeWidgetItem()
            new_ddi_node.setText(0, ddi.name)
            ddi_nodes.append(new_ddi_node)

        self.ddi_tree.addTopLevelItems(ddi_nodes)

        date_type_ddis = self.uj.find_ddis_by_attribute('type', 'DATE    ')
        if date_type_ddis:
            self.ddi_date.related_ddi_box.reset_items({z.name:z.name for z in date_type_ddis})

        relatable_type_ddis = []
        for type_ in ['FLATFILE', 'LIST    ', 'RESPONSE']:
            relatable_type_ddis.extend(self.uj.find_ddis_by_attribute('type', type_))
        if relatable_type_ddis:
            self.ddi_related_ddi.reset_items({z.name:z.name for z in relatable_type_ddis})

        sourceable_steps = self.uj.find_steps_by_attribute('name_user_defined', True)
        if sourceable_steps:
            self.ddi_response_source_step.reset_items({ str(z.id):z.name for z in sourceable_steps })

        self.correlated_names = { z.field_name:z.field_name for z in self.uj.find_ddis_by_attribute('type', 'AUTOCORR') } # if z.field_type == 'Repeated Fields' }
        self.ddi_auto_correlate_name.reset_items(self.correlated_names)

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
            self.ddi_related_ddi,
            self.ddi_response_source_step,
            self.ddi_siphon_table,
            self.ddi_auto_correlate_type,
            self.ddi_auto_correlate_name,
            self.ddi_auto_correlate_appears_in,
            self.ddi_auto_increment_starting_value,
            self.ddi_auto_increment_increment,
            self.ddi_auto_increment_prefix,
            self.ddi_auto_increment_suffix,
            self.ddi_auto_increment_min_lenght,
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
            RelatedDDI: {self.ddi_column_index_widget: 'column', self.ddi_related_ddi: 'associated'},
            ResponseDDI: {self.ddi_selector_widget: 'selection_type', self.ddi_column_index_widget: 'column', self.ddi_response_source_step: 'source_step_id', self.ddi_siphon_table: 'dict_siphons'},
            AutoCorrelatedDDI: {self.ddi_auto_correlate_type: 'field_type', self.ddi_auto_correlate_name: 'field_name', self.ddi_auto_correlate_appears_in: ['find_in_url', 'find_in_post', 'find_in_headers']},
            AutoIncrementDDI: {self.ddi_auto_increment_starting_value: 'starting_value', self.ddi_auto_increment_increment: 'increment', self.ddi_auto_increment_prefix: 'prefix',
                               self.ddi_auto_increment_suffix: 'suffix', self.ddi_auto_increment_min_lenght: 'minimum_length'},
        }

        object_attribute_pairs = ddi_type_mappings[type(self.selected_ddi)]
        # print('obj', object_attribute_pairs )
        # print('selected type', type(self.selected_ddi) ,'selected item expected attributes', object_attribute_pairs.values() )
        for field in ddi_specific_fields:
            debug_message = ''
            # print('field', field, 'values', object_attribute_pairs.values())
            if field in object_attribute_pairs.keys():
                field.show()
                target_attribute_name = object_attribute_pairs[field]
                # print('target attribute', target_attribute_name)
                if isinstance(target_attribute_name, str):
                    if target_attribute_name != '':
                        # print('ttt', type(getattr(self.selected_ddi, object_attribute_pairs[field])))
                        value = getattr(self.selected_ddi, object_attribute_pairs[field])
                        if callable(value):
                            value = value()
                        else:
                            value = str(value)
                        field.set_text(value)
                        # print('target attribute value', value)

                        # --- debug ---
                        if field == self.ddi_value_widget:
                            debug_message += 'field: '+str(field)+'; uj object value: '+ str(value) + '\n'
                else:
                    # currently this section covers for Date group & table widget
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

            # --- debug ---
            if field == self.ddi_response_source_step:
                debug_message += 'ui object value: ' + self.ddi_response_source_step.text() + '; visibility: ' + str(self.ddi_response_source_step.combo_box.isVisible()) + '\n'
                self.debug__(debug_message)



    def show_step_details(self):
        pass



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.exit(app.exec_())
