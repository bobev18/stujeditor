from siphon import Siphon

SCHEME_PREFIX = '{http://www.reflective.com}'

class DynamicDataItem():

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
        # common
        self.format = self.items['FORMAT    ']
        self.offset_type = self.items['OFFSETTYPE']
        self.starting_point = self.items['START     ']
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
        self.column = int(self.items['COLUMNID  '])
        # self.table =  # this one gets initialized in the parent class
        # self.column_count = int(self.items['COLUMNSCNT'])  # this one gets initialized in the parent class

class VariableDDI(DynamicDataItem):
    def __init__(self, element):
        super().__init__(element)
        self.value = self.items['INITALVALU']

class RelatedDDI(DynamicDataItem):
    def __init__(self, element):
        super().__init__(element)
        # associated is name of another DDI ; UI lists only relevant DDIs; relevance is determined by only by DDI type, not number of data columns
        self.associated = self.items['ASSOCIATED']
        self.column = int(self.items['FIELDINDEX'])

class ResponseDDI(DynamicDataItem):
    def __init__(self, element):
        super().__init__(element)
        self.column = int(self.items['INDEX     '])
        self.source_step_id = int(self.items['STEPREF   '])
        # siphons are covered in parent

class AutoCorrelatedDDI(DynamicDataItem):
    def __init__(self, element):
        super().__init__(element)
        self.field_name = self.items['FIELDNAME ']
        self.field_type = self.items['FIELDTYPE ']
        self.find_in_headers = self.items['INHEADERS '] == 'true'
        self.find_in_post = self.items['INPOST    '] == 'true'
        self.find_in_url = self.items['INURL     '] == 'true'

class AutoIncrementDDI(DynamicDataItem):
    def __init__(self, element):
        super().__init__(element)
        self.starting_value = int(self.items['STARTVALUE'])
        self.increment = int(self.items['INCREMENT '])
        self.minimum_length = int(self.items['MINLENGTH '])
        self.prefix = self.items['PREFIX    ']
        self.suffix = self.items['SUFFIX    ']
