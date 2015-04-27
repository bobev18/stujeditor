import xml.etree.cElementTree as ET

SCHEME_PREFIX = '{http://www.reflective.com}'


#         <DDITEM EXISTING="true" NAME="csrftoken" VALID="true">
#             <SOURCE TYPE="AUTOCORR"/>
#             <SELECTION TYPE="FIRST   "/>
#             <SCOPE TYPE="THREAD  "/>
#             <LIFECYCLE TYPE="C"/>
#             <DESCRIPTION/>
#             <ITEM CODE="ENCODE    ">true</ITEM>
#             <ITEM CODE="FIELDNAME ">csrftoken</ITEM>
#             <ITEM CODE="FIELDTYPE ">Known Fields</ITEM>
#             <ITEM CODE="INHEADERS ">true</ITEM>
#             <ITEM CODE="INPOST    ">true</ITEM>
#             <ITEM CODE="INURL     ">true</ITEM>
#         </DDITEM>
        # <DDITEM EXISTING="true" NAME="Update Purchase Order ID 26" VALID="true">
        #     <SOURCE TYPE="RESPONSE"/>
        #     <SELECTION TYPE="FIRST   "/>
        #     <SCOPE TYPE="THREAD  "/>
        #     <LIFECYCLE TYPE="T"/>
        #     <DESCRIPTION>Created to handle recorded Maximo identifier mx2924.</DESCRIPTION>
        #     <ITEM CODE="ENCODE    ">false</ITEM>
        #     <ITEM CODE="INDEX     ">1</ITEM>
        #     <ITEM CODE="STEPREF   ">23</ITEM>
        #     <SIPHONS>
        #         <SIPHON SEQUENCE="0" TYPE="R">
        #             <STARTTEXT>&lt;input  aria\-readonly="true"  role="textbox"  id="mx[\d]{1,8}" class="fld text text   ib readonlyfld fld_ro"     ctype="textbox"   li="mx[\d]{1,8}"  db="([^'"\[]*?)"   maxlength="[\d]{1,8}" style=";width:[\d]{1,8}\.[\d]{1,8}px;"      sue="[\d]{1,8}" tabindex="\-[\d]{1,8}" readonly="readonly" type="text" title="PO: (.+?)" value="\2" ov="\2" work="[\d]{1,8}"</STARTTEXT>
        #             <ENDTEXT/>
        #             <RFINDEX>1</RFINDEX>
        #         </SIPHON>
        #     </SIPHONS>
        # </DDITEM>


class Siphon():

    # def __init__(self, sequence, type_, start, end, rf_index):
    def __init__(self, element):
        self.sequence = element.get('SEQUENCE')
        self.type = element.get('TYPE')
        self.start = element.find(SCHEME_PREFIX+'STARTTEXT').text
        self.end = element.find(SCHEME_PREFIX+'ENDTEXT').text
        self.rf_index = element.find(SCHEME_PREFIX+'RFINDEX').text


class DynamicDataItem():

    # def __init__(self, name, type_, selection_type, scope, lifecycle, description, type_specific_items, siphons):
    def __init__(self, element):
        self.existing = element.get('EXISTING')
        self.name = element.get('NAME')
        self.valid = element.get('VALID')
        # self.valid = element.attrib['VALID']
        self.type = element.find(SCHEME_PREFIX+'SOURCE').attrib['TYPE']
        self.selection_type = element.find(SCHEME_PREFIX+'SELECTION').attrib['TYPE']
        self.scope = element.find(SCHEME_PREFIX+'SCOPE').attrib['TYPE']
        self.lifecycle = element.find(SCHEME_PREFIX+'LIFECYCLE').attrib['TYPE']
        self.description = element.find(SCHEME_PREFIX+'DESCRIPTION').text
        self.items = {}
        for item in element.findall(SCHEME_PREFIX+'ITEM'):
            self.items[item.get('CODE')] = item.text
        siphons_element = element.find(SCHEME_PREFIX+'SIPHONS')
        self.siphons = []
        if siphons_element:
            for siphon in siphons_element.findall(SCHEME_PREFIX+'SIPHON'):
                self.siphons.append(Siphon(siphon))







class UserJourney():

    def __init__(self, filename):
        # self.filename = filename
        with open(filename, 'r') as f:
            self.raw = f.read()
        self.tree = ET.ElementTree(file=filename)
        self.root = self.tree.getroot()
        self.name = self.root.attrib['NAME']

        dditems_element = self.root.find(SCHEME_PREFIX+'DYNAMICDATA')
        self.dditems = []
        for ddi in dditems_element.findall(SCHEME_PREFIX+'DDITEM'):
            self.dditems.append(DynamicDataItem(ddi))


    def list_ddi_names(self):
        return [z.name for z in self.dditems]



