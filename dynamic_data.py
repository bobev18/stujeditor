from siphon import Siphon

SCHEME_PREFIX = '{http://www.reflective.com}'

class DynamicDataItem():

    # def __init__(self, name, type_, selection_type, scope, lifecycle, description, type_specific_items, siphons):
    def __init__(self, element):
        self.element = element
        # common attributes
        self.name = element.get('NAME')
        self.description = element.find(SCHEME_PREFIX+'DESCRIPTION').text
        self.existing = bool(element.get('EXISTING'))
        self.valid = bool(element.get('VALID'))
        # common sub-elements
        self.type = element.find(SCHEME_PREFIX+'SOURCE').attrib['TYPE']
        self.scope = element.find(SCHEME_PREFIX+'SCOPE').attrib['TYPE']
        self.lifecycle = element.find(SCHEME_PREFIX+'LIFECYCLE').attrib['TYPE']
        self.selection_type = element.find(SCHEME_PREFIX+'SELECTION').attrib['TYPE']

        # partially common - i.e. there are such elements, but they have inconsistent inner content
        self.items = {}
        for item in element.findall(SCHEME_PREFIX+'ITEM'):
            self.items[item.get('CODE')] = item.text

        # print('proceesing ENCODE for step', self.name)
        if 'ENCODE    ' in self.items.keys():
            self.encode = bool(self.items['ENCODE    '])
        else:
            self.encode = None

        # optional
        self.table = []
        table_element = element.find(SCHEME_PREFIX+'TABLE')
        if table_element:
            self.column_count = int(self.items['COLUMNSCNT'])
            for row in table_element.findall(SCHEME_PREFIX+'ROW'):
                row_values = [ row.get('COLUMN' + str(z)) for z in range(self.column_count) ]        # <ROW COLUMN0="5" COLUMN1="55" ROWNUM="1"/>
                self.table.append(row_values)

        self.siphons = []
        siphons_element = element.find(SCHEME_PREFIX+'SIPHONS')
        if siphons_element:
            for siphon in siphons_element.findall(SCHEME_PREFIX+'SIPHON'):
                self.siphons.append(Siphon(siphon))

    def rename(self, new_name):
        self.element.set('NAME', new_name)
        self.name = new_name

    def dict_siphons(self):
        table = []
        for siphon in self.siphons:
            table.append({'type': siphon.type, 'start': siphon.start, 'end': siphon.end, 'match_number': siphon.match_number})

        return table



class ConstantDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        self.value = self.items['VALUE     ']

class DateDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # example 1
            # <ITEM CODE="ENCODE    ">false</ITEM>
            # <ITEM CODE="FORMAT    ">dd/MM/yyyy HH:mm</ITEM>
            # <ITEM CODE="OFFSETTYPE">none</ITEM>
            # <ITEM CODE="START     ">now</ITEM>
            # <ITEM CODE="STARTVALUE"/>
        # example 2
            # <ITEM CODE="ENCODE    ">false</ITEM>
            # <ITEM CODE="FORMAT    ">dd/MM/yyyy HH:mm</ITEM>
            # <ITEM CODE="OFFSETSIG2">+</ITEM>
            # <ITEM CODE="OFFSETSIGN">-</ITEM>
            # <ITEM CODE="OFFSETTYPE">random</ITEM>
            # <ITEM CODE="OFFSETUNI2">hour(s)</ITEM>
            # <ITEM CODE="OFFSETUNIT">hour(s)</ITEM>
            # <ITEM CODE="OFFSETVAL ">3</ITEM>
            # <ITEM CODE="OFFSETVAL2">4</ITEM>
            # <ITEM CODE="START     ">fixed value</ITEM>
            # <ITEM CODE="STARTVALUE">21/05/2015 12:00</ITEM>
        # example 3
            # <ITEM CODE="ENCODE    ">false</ITEM>
            # <ITEM CODE="FORMAT    ">dd/MM/yyyy HH:mm mm:HH</ITEM>
            # <ITEM CODE="OFFSETSIGN">+</ITEM>
            # <ITEM CODE="OFFSETTYPE">fixed</ITEM>
            # <ITEM CODE="OFFSETUNIT">day(s)</ITEM>
            # <ITEM CODE="OFFSETVAL ">33</ITEM>
            # <ITEM CODE="START     ">another date</ITEM>
            # <ITEM CODE="STARTVALUE">date</ITEM>

        # common
        self.format = self.items['FORMAT    ']
        self.offset_type = self.items['OFFSETTYPE']
        self.starting_point = self.items['START     ']
                                       # >START     <

        # starting_value is always listed, but it's given value only for offset types 'fixed' and 'another date'
        #   - for fixed, datetime format is enforced by the UI
        #   - for another date - drop down with relevant DDIs is given
        if self.starting_point in ['fixed value', 'another date']:
            self.starting_value = self.items['STARTVALUE']
        else:
            self.starting_value = None


        # optional
        if self.offset_type != 'none':
            self.first_offset_sign = self.items['OFFSETSIGN']
            self.first_offset_unit = self.items['OFFSETUNIT']
            self.first_offset_value = int(self.items['OFFSETVAL '])
        if self.offset_type == 'random':
            self.second_offset_sign = self.items['OFFSETSIG2']
            self.second_offset_unit = self.items['OFFSETUNI2']
            self.second_offset_value = int(self.items['OFFSETVAL2'])

class DelimitedFileDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        self.file_name = self.items['FILENAME  ']
        self.column = int(self.items['FIELDINDEX'])
        self.delimiter = self.items['DELIMITER ']

class ListDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # <ITEM CODE="COLUMNID  ">1</ITEM>
        # <ITEM CODE="COLUMNSCNT">2</ITEM>
        # <ITEM CODE="ENCODE    ">false</ITEM>
        # <TABLE>
        #     <ROW COLUMN0="2" COLUMN1="a" ROWNUM="0"/>
        #     <ROW COLUMN0="5" COLUMN1="55" ROWNUM="1"/>
        # </TABLE>
        self.column = int(self.items['COLUMNID  '])

        # self.table =  # this one gets initialized in the parent class
        # self.column_count = int(self.items['COLUMNSCNT'])  # this one gets initialized in the parent class
        # self.delimiter = self.items['DELIMITER ']

class VariableDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        self.value = self.items['INITALVALU']

class RelatedDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # <ITEM CODE="ASSOCIATED">list</ITEM>
        # <ITEM CODE="FIELDINDEX">33</ITEM>
        # associated is name of another DDI ; UI lists only relevant DDIs; relevance is determined by only by DDI type, not number of data columns
        self.associated = self.items['ASSOCIATED']
        self.column = int(self.items['FIELDINDEX'])

class ResponseDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # <ITEM CODE="INDEX     ">1</ITEM>
        # <ITEM CODE="STEPREF   ">13</ITEM>
        self.column = int(self.items['INDEX     '])
        self.source_step_id = int(self.items['STEPREF   '])
        # siphons are covered in parent

class AutoCorrelatedDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # <ITEM CODE="ENCODE    ">false</ITEM>
        #     <ITEM CODE="FIELDNAME ">Host</ITEM>
        #     <ITEM CODE="FIELDTYPE ">Repeated Fields</ITEM>
        #     <ITEM CODE="INHEADERS ">false</ITEM>
        #     <ITEM CODE="INPOST    ">false</ITEM>
        #     <ITEM CODE="INURL     ">true</ITEM>
        # <ITEM CODE="ENCODE    ">true</ITEM>
        #     <ITEM CODE="FIELDNAME ">csrftoken</ITEM>
        #     <ITEM CODE="FIELDTYPE ">Known Fields</ITEM>
        #     <ITEM CODE="INHEADERS ">true</ITEM>
        #     <ITEM CODE="INPOST    ">true</ITEM>
        #     <ITEM CODE="INURL     ">true</ITEM>
        self.field_name = self.items['FIELDNAME ']
        self.field_type = self.items['FIELDTYPE ']
        self.find_in_headers = bool(self.items['INHEADERS '])
        self.find_in_post = bool(self.items['INPOST    '])
        self.find_in_url = bool(self.items['INURL     '])

class AutoIncrementDDI(DynamicDataItem):

    def __init__(self, element):
        super().__init__(element)
        # <ITEM CODE="INCREMENT ">43</ITEM>
        #     <ITEM CODE="MINLENGTH ">2</ITEM>
        #     <ITEM CODE="STARTVALUE">55</ITEM>
        #     <ITEM CODE="PREFIX    ">asda</ITEM>
        #     <ITEM CODE="SUFFIX    ">342sdf</ITEM>
        self.starting_value = int(self.items['STARTVALUE'])
        self.increment = int(self.items['INCREMENT '])
        self.minimum_length = int(self.items['MINLENGTH '])
        self.prefix = self.items['PREFIX    ']
        self.suffix = self.items['SUFFIX    ']






