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

SIPHON_TYPES = {'T': 'Text Substring', 'R': 'Regular Expression',}


class Siphon():

    # def __init__(self, sequence, type_, start, end, match_number):
    def __init__(self, element):
        self.sequence = element.get('SEQUENCE')
        self.type = element.get('TYPE')
        self.start = element.find(SCHEME_PREFIX+'STARTTEXT').text
        self.end = element.find(SCHEME_PREFIX+'ENDTEXT').text
        self.match_number = element.find(SCHEME_PREFIX+'RFINDEX').text

    def __repr__(self):
        result = 'Type: ' + SIPHON_TYPES[self.type] + '\n'
        result+= 'Match: ' + self.match_number + '\n'
        result+= 'Start text: ' + self.start + '\n'
        if self.end: result+= 'End text  : ' + self.end + '\n'
        return result+'\n'



class DynamicDataItem():

    # def __init__(self, name, type_, selection_type, scope, lifecycle, description, type_specific_items, siphons):
    def __init__(self, element):
        self.element = element
        self.existing = bool(element.get('EXISTING'))
        self.name = element.get('NAME')
        self.valid = bool(element.get('VALID'))
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

    def rename(self, new_name):
        self.element.set('NAME', new_name)
        self.name = new_name
        # print('element', self.element)
        # print('name', self.element.)

#         <STEP COUNTASTRANSACTION="false" EXECUTESEPARATELY="false"
#             FIRSTCYCLEONLY="false" LASTCYCLEONLY="false"
#             NAME="Craft New Row" NAMEUSERDEFINED="true" ORDER="201"
#             PROCESSRESPONSE="false" TYPE="POST">
#             <REQUEST URL="https://max75rep.gasco.ae:443/maximo/ui/maximo.jsp"/>
#             <POST>
#                 <NVP NAME="csrftoken" VALUE="{{csrftoken}}"/>
#                 <NVP NAME="currentfocus" VALUE="{{Update Work Order ID 20}}"/>
#                 <NVP NAME="events" VALUE="[{&quot;type&quot;:&quot;click&quot;,&quot;targetId&quot;:&quot;{{Update Work Order ID 20}}&quot;,&quot;value&quot;:&quot;&quot;,&quot;requestType&quot;:&quot;SYNC&quot;,&quot;csrftokenholder&quot;:&quot;coo0mpa85vpkojtgmgmsgt7qs5&quot;}]"/>
#                 <NVP NAME="requesttype" VALUE="SYNC"/>
#                 <NVP NAME="responsetype" VALUE="text/xml"/>
#                 <NVP NAME="scrollleftpos" VALUE="0"/>
#                 <NVP NAME="scrolltoppos" VALUE="0"/>
#                 <NVP NAME="uisessionid" VALUE="{{uisessionid}}"/>
#             </POST>
#             <SUCCESS>Skill Level</SUCCESS>
#             <DESCRIPTION/>
#             <SLEEPTIME>3000</SLEEPTIME>
#             <NVP NAME="xhrseqnum" PLUGIN="1" TYPE="java.lang.String">{{xhrseqnum}}</NVP>
#             <NVP NAME="_QM_Try" PLUGIN="1" TYPE="java.lang.String">1</NVP>
#             <NVP NAME="X-Requested-With" PLUGIN="1" TYPE="java.lang.String">XMLHttpRequest</NVP>
#             <NVP NAME="Host" PLUGIN="1" TYPE="java.lang.String">max75rep.gasco.ae</NVP>
#             <NVP NAME="Referer" PLUGIN="1" TYPE="java.lang.String">https://max75rep.gasco.ae/maximo/ui/?event=loadapp&amp;value=wotrack&amp;uisessionid=323&amp;csrftoken=coo0mpa85vpkojtgmgmsgt7qs5</NVP>
#             <NVP NAME="Accept" PLUGIN="1" TYPE="java.lang.String">*/*</NVP>
#             <NVP NAME="Connection" PLUGIN="1" TYPE="java.lang.String">Keep-Alive</NVP>
#             <NVP NAME="Content-Type" PLUGIN="1" TYPE="java.lang.String">application/x-www-form-urlencoded;charset=UTF-8</NVP>
#             <NVP NAME="pageseqnum" PLUGIN="1" TYPE="java.lang.String">{{pageseqnum}}</NVP>
#             <NVP NAME="ValidationType" TYPE="java.lang.String">REGEX</NVP>
#             <NVP NAME="logResponse" TYPE="java.lang.Boolean">false</NVP>
#             <NVP NAME="applyOctetEncoding" TYPE="java.lang.Boolean">false</NVP>
#             <NVP NAME="logRequest" TYPE="java.lang.Boolean">false</NVP>
#             <STEPGROUP>201</STEPGROUP>
#         </STEP>

class Step():

    def __init__(self, element):

        def booleanize(element):
            if element.get('TYPE') == 'java.lang.Boolean':
                return bool(element.text)
            else:
                return element.text

        self.element = element
        self.countastransaction = bool(element.get('COUNTASTRANSACTION'))
        self.executeseparately = bool(element.get('EXECUTESEPARATELY'))
        self.firstcycleonly = bool(element.get('FIRSTCYCLEONLY'))
        self.lastcycleonly = bool(element.get('LASTCYCLEONLY'))
        self.name = element.get('NAME')
        self.nameuserdefined = bool(element.get('NAMEUSERDEFINED'))
        print('>>>>', element.tag, element.attrib)
        self.order = int(element.get('ORDER'))
        self.processresponse = bool(element.get('PROCESSRESPONSE'))
        self.type = element.get('TYPE')

        self.request = element.find(SCHEME_PREFIX+'REQUEST').get('URL')
        post_element = element.find(SCHEME_PREFIX+'POST')
        self.post_items = {}
        if post_element:
            for post_item in post_element.findall(SCHEME_PREFIX+'NVP'):
                self.post_items[post_item.get('NAME')] = post_item.get('VALUE')

        self.success = element.find(SCHEME_PREFIX+'SUCCESS').text
        self.description = element.find(SCHEME_PREFIX+'DESCRIPTION').text
        self.sleeptime = int(element.find(SCHEME_PREFIX+'SLEEPTIME').text)
        self.items = {}
        self.headers = {}
        for nvp_item in element.findall(SCHEME_PREFIX+'NVP'):
            if nvp_item.get('PLUGIN') == '1':
                self.headers[nvp_item.get('NAME')] = booleanize(nvp_item)
            else:
                self.items[nvp_item.get('NAME')] = booleanize(nvp_item)

        self.stepgroup = int(element.find(SCHEME_PREFIX+'STEPGROUP').text)


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

        steps_element = self.root.find(SCHEME_PREFIX+'STEPS')
        self.steps = []
        for step in dditems_element.findall(SCHEME_PREFIX+'STEP'):
            self.steps.append(Step(step))


    def list_ddi_names(self):
        return [z.name for z in self.dditems]

    def pull_ddi_by(self, attrib, value):
        result = []
        for ddi in self.dditems:
            if getattr(ddi, attrib) == value:
                result.append(ddi)

        if len(result) > 1:
            return result
        elif len(result) == 1:
            return result[0]
        else:
            return None

    def list_step_names(self):
        return [z.name for z in self.steps]

    def pull_step_by(self, attrib, value):
        result = []
        for step in self.steps:
            if getattr(step, attrib) == value:
                result.append(step)

        if len(result) > 1:
            return result
        elif len(result) == 1:
            return result[0]
        else:
            return None


    def __repr__(self):
        return str(ET.tostring(self.root))



