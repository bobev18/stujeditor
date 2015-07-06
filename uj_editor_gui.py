import os
from userjourney import UserJourney
from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI
from gui_classes import LabelLineEdit, LabelComboBox, LabelButtonGroup, DateFieldsGroup, MyTableWidget, RowControlTableWidget, LabelCheckboxesGroup

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        # QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QWidget, QButtonGroup,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QSplitter,
    QPushButton, QLineEdit, QLabel, QRadioButton, QCheckBox, QTreeWidget, QComboBox, QFileDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QPlainTextEdit)

DDI_TYPES = {'AUTOCORR': 'Auto-Correlated', 'AUTOINCR': 'Auto-Incremented', 'CONSTANT': 'Constant', 'DATE    ': 'Date', 'FLATFILE': 'Delimited File', '        ': 'Java Class', 'LIST    ': 'List', 'SAMEAS  ': 'Related', 'RESPONSE': 'Response', 'VARIABLE': 'Variable'}
SELECTOR_TYPES = {'FIRST   ': 'First', 'LAST    ': 'Last', 'RANDOM  ': 'Random', 'RANDONCE': 'Random Unique', 'SEQUENTI': 'Sequential', 'SEQUONCE': 'Sequential Unique'}
STEP_REQUEST_TYPES = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']
# STEP_CONTENT_TYPES = {'form': ['application/x-www-form-urlencoded', 'multipart/form-data'], 'binary': ['application/octet-stream', 'binary/octet-stream'], 'XML': ['text/html'], 'other': ['text/plain', 'application/json']}
STEP_CONTENT_TYPES = ['application/x-www-form-urlencoded', 'multipart/form-data', 'application/octet-stream', 'binary/octet-stream', 'text/xml', 'text/plain', 'application/json']
SIPHON_TYPES = {'T': 'Text Substring', 'R': 'Regular Expression', 'D': 'Delimiter', 'I': 'Position', 'Y': 'Replace'}

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
        # step_details_layout.addWidget(self.create_specific_step_details(), 1, 0, 3, 1)
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

        self.ddi_siphon_table = RowControlTableWidget(['type', 'start', 'end', 'index'])
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
        self.content_type = LabelComboBox('Content-Type', { z:z for z in STEP_CONTENT_TYPES })
        request_type_content_type_layout.addLayout(self.content_type.layout)
        # self.content_type.combo_box.currentIndexChanged[str].connect(self.update_content_subtypes)
        # # what's the point of having type and subtypes? the one sent with headers is the subtype - it should be the only selection
        # self.content_subtype = LabelComboBox('', { z:z for z in STEP_CONTENT_TYPES['form'] })
        # request_type_content_type_layout.addLayout(self.content_subtype.layout)
        vbox.addLayout(request_type_content_type_layout)
        self.step_url = LabelLineEdit('URL')
        vbox.addLayout(self.step_url.layout)
        self.step_url_params_table = RowControlTableWidget(['Parameter', 'Value'])
        vbox.addLayout(self.step_url_params_table.layout)
        self.step_post_params_table = RowControlTableWidget(['Parameter', 'Value'])
        vbox.addLayout(self.step_post_params_table.layout)
        self.step_post_block = QPlainTextEdit()
        vbox.addWidget(self.step_post_block)
        success_validation_layout = QHBoxLayout()
        success_validation_layout.setContentsMargins(0,0,0,0)
        self.step_validation_type = LabelComboBox('Success Validation', {'PLAIN': 'Plain Text','REGEX': 'Regular Expression'})
        success_validation_layout.addLayout(self.step_validation_type.layout)
        self.step_validation_text = LabelLineEdit('')
        success_validation_layout.addLayout(self.step_validation_text.layout)
        self.max_response = LabelLineEdit('Max acceptable response time')
        success_validation_layout.addLayout(self.max_response.layout)
        vbox.addLayout(success_validation_layout)
        self.step_dynamic_content = LabelCheckboxesGroup('Select content types to be handled automatically', ['images', 'css', 'javaScript'])
        vbox.addLayout(self.step_dynamic_content.layout)

        flow_control_line1_layout = QHBoxLayout()
        self.step_flow_control_type = LabelComboBox('Flow Control', {'': 'GoTo', 'RESPONSE': 'Response Based', 'CONDTITIONAL': 'Conditional', 'PERCENTAGE': 'Percentage Based',
                                                                     'DDLOOP': 'Dynamic Data Loop', 'VARIABLELOOP': 'Variable Loop', 'FIXEDLOOP': 'Fixed Loop'})
        flow_control_line1_layout.addLayout(self.step_flow_control_type.layout)
        self.step_flow_target_plus = LabelComboBox('Step', {'NEXT_STEP': 'Next Step', 'END_CYCLE': 'End Cycle', 'END_USER': 'End User'})
        flow_control_line1_layout.addLayout(self.step_flow_target_plus.layout)
        self.step_flow_sleep = LabelLineEdit('Sleep Time (sec)')
        flow_control_line1_layout.addLayout(self.step_flow_sleep.layout)
        vbox.addLayout(flow_control_line1_layout)

        flow_control_line2_layout = QHBoxLayout()
        self.step_flow_ddl_ddi = LabelComboBox('Dynamic Data Item', {})
        flow_control_line2_layout.addLayout(self.step_flow_ddl_ddi.layout)
        self.step_flow_varloop_start = LabelLineEdit('Minimum Iterations')
        flow_control_line2_layout.addLayout(self.step_flow_varloop_start.layout)
        self.step_flow_varloop_end = LabelLineEdit('Maximum Iterations')
        flow_control_line2_layout.addLayout(self.step_flow_varloop_end.layout)
        self.step_flow_fixloop = LabelLineEdit('Iterations')
        flow_control_line2_layout.addLayout(self.step_flow_fixloop.layout)

        self.step_flow_conditional_true = LabelComboBox('If true, go to', {'NEXT_STEP': 'Next Step', 'END_CYCLE': 'End Cycle', 'END_USER': 'End User'})
        flow_control_line2_layout.addLayout(self.step_flow_conditional_true.layout)
        self.step_flow_conditional_false = LabelComboBox('otherwise, go to', {'NEXT_STEP': 'Next Step', 'END_CYCLE': 'End Cycle', 'END_USER': 'End User'})
        flow_control_line2_layout.addLayout(self.step_flow_conditional_false.layout)
        vbox.addLayout(flow_control_line2_layout)

        self.step_flow_response_table = RowControlTableWidget(['Response Step', 'Match Criteria', 'Step', 'Sleep Time'])
        vbox.addLayout(self.step_flow_response_table.layout)
        self.step_flow_percentage_table = RowControlTableWidget(['Percentage', 'Step', 'Sleep Time'])
        self.step_flow_percentage_table.set_text([['100', {'Next Step': ['Next Step', 'End Cycle', 'End User']}, '0.0']])
        vbox.addLayout(self.step_flow_percentage_table.layout)
        self.step_flow_conditional_table = RowControlTableWidget(['Phrase 1', 'Conditional', 'Phrase 2', 'Operator'])
        vbox.addLayout(self.step_flow_conditional_table.layout)


        group_box.setLayout(vbox)
        return group_box


    def create_specific_step_details(self):
        pass




# ------------------------------------------------------ end of creations ----------------------------------------------------------

    # def create_actions(self):
    #     self.import_act = QAction("&Import...", self, shortcut="Ctrl+I", triggered=self.import_uj)
    #     self.export_act = QAction("&Export...", self, shortcut="Ctrl+E", triggered=self.export_uj)

    # def update_content_subtypes(self, item):
    #     # item is supposed to be the text value of the combobox selection
    #     print('reached function update_content_subtypes with item=', item)



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
        # convert SIPHON_TYPES from full text to code before passing them to self.uj...

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
        selected_step_name = self.step_tree.selectedItems()[0].text(0)
        self.selected_step = self.uj.find_step_by_name(selected_step_name)

        # self.ddi_name.set_text(selected_ddi_name)
        # self.ddi_description.set_text(self.selected_ddi.description)
        # self.ddi_type.set_text(DDI_TYPES[self.selected_ddi.type])
        # self.ddi_sharing.set_text(self.selected_ddi.scope)
        # self.ddi_refresh.set_text(self.selected_ddi.lifecycle)

        self.step_name.set_text(selected_step_name)
        self.step_pre_time.set_text(self.selected_step.sleeptime)
        self.step_description.set_text(self.selected_step.description)
        # print(self.selected_step.first_cycle_only, self.selected_step.last_cycle_only, self.selected_step.count_as_transaction, self.selected_step.processresponse, self.selected_step.execute_separately)
        self.step_checkboxes.set_values(self.selected_step.first_cycle_only, self.selected_step.last_cycle_only, self.selected_step.count_as_transaction,
                                         self.selected_step.processresponse, self.selected_step.execute_separately)
        # ['Run First Cycle Only', 'Run Last Cycle Only', 'Count as Transaction', 'Process Response', 'Execute Separately'])
        self.request_type.set_text(self.selected_step.type)
        selected_step_content_type = ''
        for header in self.selected_step.headers:
            if header['name'] == 'Content-Type':
                selected_step_content_type = header['value']
        self.content_type.set_text(selected_step_content_type)
        self.step_url.set_text(self.selected_step.request)
        if self.selected_step.get_itmes == []:
            self.step_url_params_table.hide()
        else:
            self.step_url_params_table.show()
            get_params = []
            for item in self.selected_step.get_itmes:
                get_params.append([item['name'], item['value']])
            self.step_url_params_table.set_text(get_params)

        if self.selected_step.post_items == []:
            self.step_post_params_table.hide()
            self.step_post_block.hide()
        else:
            if self.selected_step.post_items[0]['name'] == '':
                self.step_post_params_table.hide()
                self.step_post_block.show()
                self.step_post_block.appendPlainText(self.selected_step.post_items[0]['value'])
            else:
                self.step_post_block.hide()
                self.step_post_params_table.show()
                self.step_post_params_table.set_text([ [z['name'], z['value']] for z in self.selected_step.post_items])

        selected_step_validation_type = ''
        for item in self.selected_step.items:
            if item['name'] == 'ValidationType':
                selected_step_validation_type = item['value']

        self.step_validation_type.set_text(selected_step_validation_type)
        self.step_validation_text.set_text(self.selected_step.success)

        selected_step_max_response = ''
        for item in self.selected_step.items:
            if item['name'] == 'MaxResponseTime':
                selected_step_max_response = item['value']
        if self.selected_step.is_lead():
            self.max_response.show()
            self.max_response.set_text(selected_step_max_response)
        else:
            self.max_response.hide()

        selected_step_dynamic_content = []
        for item in self.selected_step.items:
            if item['name'] == 'contentTypes':
                selected_step_dynamic_content = [ z in item['value'] for z in ['images', 'javaScript', 'css'] ]
        if self.selected_step.is_lead():
            self.step_dynamic_content.show()
            self.step_dynamic_content.set_values(*selected_step_dynamic_content)
        else:
            self.step_dynamic_content.hide()

        self.step_flow_target_plus.hide()
        self.step_flow_sleep.hide()
        self.step_flow_ddl_ddi.hide()
        self.step_flow_varloop_start.hide()
        self.step_flow_varloop_end.hide()
        self.step_flow_fixloop.hide()
        self.step_flow_conditional_true.hide()
        self.step_flow_conditional_false.hide()
        self.step_flow_response_table.hide()
        self.step_flow_percentage_table.hide()
        self.step_flow_conditional_table.hide()

        # need to update the step list every time because new steps might have been added after the initial import
        steps = self.uj.list_step_name_id_pairs()
        steps.update({'NEXT_STEP': 'Next Step', 'END_CYCLE': 'End Cycle', 'END_USER': 'End User'})
        self.step_flow_target_plus.reset_items(steps) # reset val even if hidden

        if not hasattr(self.selected_step, 'flow_type'):
            self.step_flow_control_type.set_text('GoTo')
            self.step_flow_target_plus.show()
            self.step_flow_target_plus.set_text('NEXT_STEP')
            self.step_flow_sleep.show()
            self.step_flow_sleep.set_text('0.0')
        else:                              # ==================================== ALL NON 'GOTO' FLOW CONTROL ====================================
            self.step_flow_control_type.set_text(self.selected_step.flow_type)

            selected_step_flow_target = ''
            selected_step_flow_sleep = ''
            selected_step_flow_ddi = ''
            selected_step_flow_miniter = ''
            selected_step_flow_maxiter = ''
            selected_step_flow_iter = ''
            selected_step_flow_conditional_true_target = ''
            selected_step_flow_conditional_false_target = ''
            for item in self.selected_step.flow_items:
                if item['name'] == 'DESTINATIONSTEP':
                    selected_step_flow_target = item['value']
                if item['name'] == 'SLEEPTIME':
                    selected_step_flow_sleep = str(float(item['value'])/1000)
                if item['name'] == 'DDITEM':
                    selected_step_flow_ddi = item['value']
                if item['name'] == 'MINITERCOUNT':
                    selected_step_flow_miniter = item['value']
                if item['name'] == 'MAXITERCOUNT':
                    selected_step_flow_maxiter = item['value']
                if item['name'] == 'ITERCOUNT':
                    selected_step_flow_iter = item['value']
                if item['name'] == 'TRUECONDITIONSTEP':
                    selected_step_flow_conditional_true_target = item['value']
                if item['name'] == 'FALSECONDITIONSTEP':
                    selected_step_flow_conditional_false_target = item['value']

            if self.selected_step.flow_type not in ['RESPONSE', 'CONDTITIONAL', 'PERCENTAGE']:
                self.step_flow_target_plus.show()
                self.step_flow_target_plus.set_text(selected_step_flow_target)

            if self.selected_step.flow_type not in ['RESPONSE', 'PERCENTAGE']:
                self.step_flow_sleep.show()
                self.step_flow_sleep.set_text(selected_step_flow_sleep)

            if self.selected_step.flow_type == 'DDLOOP':
                applicable_ddis_by_refresh = self.uj.find_ddis_by_attribute('lifecycle', 'T') # {'C': 'Cycle', 'R': 'Run', 'T': 'Time', 'U': 'User',}
                applicable_ddis_by_selection_randomunique = self.uj.find_ddis_by_attribute('selection_type', 'RANDONCE')
                applicable_ddis_by_selection_sequnique = self.uj.find_ddis_by_attribute('selection_type', 'SEQUONCE')
                applicable_ddis_by_selection = applicable_ddis_by_selection_randomunique + applicable_ddis_by_selection_sequnique
                applicable_ddis = { z.name:z.name for z in applicable_ddis_by_refresh if z in applicable_ddis_by_selection }
                if len(applicable_ddis):
                    self.step_flow_ddl_ddi.reset_items(applicable_ddis)
                    self.step_flow_ddl_ddi.set_text(selected_step_flow_ddi)
                self.step_flow_ddl_ddi.show()

            if self.selected_step.flow_type == 'VARIABLELOOP':
                self.step_flow_varloop_start.show()
                self.step_flow_varloop_end.show()
                self.step_flow_varloop_start.set_text(selected_step_flow_miniter)
                self.step_flow_varloop_end.set_text(selected_step_flow_maxiter)

            if self.selected_step.flow_type == 'FIXEDLOOP':
                self.step_flow_fixloop.show()
                self.step_flow_fixloop.set_text(selected_step_flow_iter)

            if self.selected_step.flow_type == 'RESPONSE':
                orders = list(set([ z['order'] for z in self.selected_step.flow_items]))
                orders.sort()
                if len(orders):
                    self.step_flow_response_table.show()
                    table = []
                    for order in orders:
                        destination = ''
                        match = ''
                        source = ''
                        sleep = ''
                        for item in self.selected_step.flow_items:
                            if item['name'] == 'DESTINATIONSTEP' and item['order'] == order:
                                destination = item['value']
                            if item['name'] == 'MATCHCRITERIA' and item['order'] == order:
                                match = item['value']
                            if item['name'] == 'RESPONSESTEP' and item['order'] == order:
                                source = item['value']
                            if item['name'] == 'SLEEPTIME' and item['order'] == order:
                                sleep = str(float(item['value'])/1000)

                        table.append([source, match, {destination: steps}, sleep])

                    self.step_flow_response_table.set_text(table)

            if self.selected_step.flow_type == 'PERCENTAGE':
                orders = list(set([ z['order'] for z in self.selected_step.flow_items]))
                orders.sort()
                if len(orders):
                    self.step_flow_percentage_table.show()
                    table = [['100', {'Next Step': ['Next Step']}, '0.0']]
                    extra_percentage = 0
                    for order in orders:
                        destination = ''
                        percentage = ''
                        sleep = ''
                        for item in self.selected_step.flow_items:
                            if item['name'] == 'DESTINATIONSTEP' and item['order'] == order:
                                destination = item['value']
                            if item['name'] == 'PERCENTAGE' and item['order'] == order:
                                percentage = item['value']
                                extra_percentage += int(percentage)
                            if item['name'] == 'SLEEPTIME' and item['order'] == order:
                                sleep = str(float(item['value'])/1000)

                        table.append([percentage, {destination: steps}, sleep])

                    table[0][0] = str(100 - extra_percentage)
                    self.step_flow_percentage_table.set_text(table)

            if self.selected_step.flow_type == 'CONDTITIONAL':

                self.step_flow_conditional_true.show()
                self.step_flow_conditional_true.reset_items(steps)
                self.step_flow_conditional_true.set_text(selected_step_flow_conditional_true_target)
                self.step_flow_conditional_false.show()
                self.step_flow_conditional_false.reset_items(steps)
                self.step_flow_conditional_false.set_text(selected_step_flow_conditional_false_target)

                orders = list(set([ z['order'] for z in self.selected_step.flow_items]))
                orders.sort()
                if len(orders):
                    self.step_flow_conditional_table.show()
                    table = []
                    for order in orders:
                        condition = ''
                        phrase1 = ''
                        operator = ''
                        phrase2 = ''
                        for item in self.selected_step.flow_items:
                            if item['name'] == 'CONDITION' and item['order'] == order:
                                condition = item['value']
                            if item['name'] == 'FIRSTPHRASE' and item['order'] == order:
                                phrase1 = item['value']
                            if item['name'] == 'OPERATOR' and item['order'] == order:
                                operator = item['value']
                            if item['name'] == 'SECONDPHRASE' and item['order'] == order:
                                phrase2 = item['value']

                        table.append([phrase1, {condition: ['<', '<=', '=', '=>', '>', '!=', 'in', 'not in']}, phrase2, {operator: ['AND', 'OR']}])

                    self.step_flow_conditional_table.set_text(table)

        #                          ====================================  END OF -- ALL NON 'GOTO' FLOW CONTROL ====================================





if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.exit(app.exec_())
