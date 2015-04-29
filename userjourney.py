import xml.etree.cElementTree as ET
import re

SCHEME_PREFIX = '{http://www.reflective.com}'
DDI_PATTERN = r'\{\{(.+?)\}\}'

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
#         <STEP COUNTASTRANSACTION="false" EXECUTESEPARATELY="false"
#             FIRSTCYCLEONLY="false" LASTCYCLEONLY="false"
#             NAME="Work Order Tracking" NAMEUSERDEFINED="true"
#             ORDER="132" PROCESSRESPONSE="false" TYPE="POST">
#             <REQUEST URL="https://max75rep.gasco.ae:443/maximo/ui/maximo.jsp"/>
#             <POST>
#                 <TEXTDATA>currentfocus={{Update Work Order ID 8}}&amp;csrftoken={{csrftoken}}&amp;events=%5B%7B%22type%22%3A%22changeapp%22%2C%22targetId%22%3A%22{{Update Work Order ID 8}}%22%2C%22value%22%3A%22WOTRACK%22%2C%22requestType%22%3A%22SYNC%22%2C%22csrftokenholder%22%3A%22coo0mpa85vpkojtgmgmsgt7qs5%22%7D%5D&amp;responsetype=text%2Fxml&amp;scrolltoppos=0&amp;uisessionid={{uisessionid}}&amp;scrollleftpos=0&amp;requesttype=SYNC</TEXTDATA>
#             </POST>
#             <SUCCESS/>
#             <DESCRIPTION/>
#             <SLEEPTIME>4000</SLEEPTIME>
#             <NVP NAME="xhrseqnum" PLUGIN="1" TYPE="java.lang.String">{{xhrseqnum}}</NVP>
#             <NVP NAME="_QM_Try" PLUGIN="1" TYPE="java.lang.String">1</NVP>
#             <NVP NAME="X-Requested-With" PLUGIN="1" TYPE="java.lang.String">XMLHttpRequest</NVP>
#             <NVP NAME="Host" PLUGIN="1" TYPE="java.lang.String">max75rep.gasco.ae</NVP>
#             <NVP NAME="Referer" PLUGIN="1" TYPE="java.lang.String">https://max75rep.gasco.ae/maximo/ui/login</NVP>
#             <NVP NAME="Accept" PLUGIN="1" TYPE="java.lang.String">*/*</NVP>
#             <NVP NAME="Connection" PLUGIN="1" TYPE="java.lang.String">Keep-Alive</NVP>
#             <NVP NAME="Content-Type" PLUGIN="1" TYPE="java.lang.String">application/x-www-form-urlencoded;charset=UTF-8</NVP>
#             <NVP NAME="pageseqnum" PLUGIN="1" TYPE="java.lang.String">{{pageseqnum}}</NVP>
#             <NVP NAME="logResponse" TYPE="java.lang.Boolean">false</NVP>
#             <NVP NAME="applyOctetEncoding" TYPE="java.lang.Boolean">false</NVP>
#             <NVP NAME="logRequest" TYPE="java.lang.Boolean">false</NVP>
#             <STEPGROUP>132</STEPGROUP>


class UJLoadException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

class Step():

    def __init__(self, element):

        def booleanize(element):
            if element.get('TYPE') == 'java.lang.Boolean':
                return bool(element.text)
            else:
                return element.text


        self.element = element
        self.count_as_transaction = bool(element.get('COUNTASTRANSACTION'))
        self.execute_separately = bool(element.get('EXECUTESEPARATELY'))
        self.first_cycle_only = bool(element.get('FIRSTCYCLEONLY'))
        self.last_cycle_only = bool(element.get('LASTCYCLEONLY'))
        self.name = element.get('NAME')
        self.name_user_defined = bool(element.get('NAMEUSERDEFINED'))
        self.nameuserdefined = bool(element.get('NAMEUSERDEFINED'))
        # print('>>>>', element.tag, element.attrib)
        self.order = int(element.get('ORDER'))
        self.processresponse = bool(element.get('PROCESSRESPONSE'))
        self.type = element.get('TYPE')

        self.request_element = element.find(SCHEME_PREFIX+'REQUEST')
        self.request = self.request_element.get('URL')
        self.description_element = element.find(SCHEME_PREFIX+'DESCRIPTION')
        self.description = self.description_element.text
        self.sleeptime_element = element.find(SCHEME_PREFIX+'SLEEPTIME')
        self.sleeptime = int(self.sleeptime_element.text)

        self.success_element = element.find(SCHEME_PREFIX+'SUCCESS')
        if self.success_element != None:
            self.success = self.success_element.text
        else:
            self.success = None
        self.stepgroup_element = element.find(SCHEME_PREFIX+'STEPGROUP')
        if self.stepgroup_element != None:
            self.stepgroup = int(self.stepgroup_element.text)
        else:
            self.stepgroup = None

        self.post_element = element.find(SCHEME_PREFIX+'POST')
        self.post_items = []
        if self.post_element:
            if len(self.post_element.findall(SCHEME_PREFIX+'NVP')):
                for post_item in self.post_element.findall(SCHEME_PREFIX+'NVP'):
                    self.post_items.append({'element': post_item, 'name': post_item.get('NAME'), 'value': post_item.get('VALUE')})
            if len(self.post_element.findall(SCHEME_PREFIX+'TEXTDATA')):
                self.post_items.append({'element': self.post_element.find(SCHEME_PREFIX+'TEXTDATA'), 'name': '', 'value': self.post_element.find(SCHEME_PREFIX+'TEXTDATA').text})

            if len(self.post_items) == 0:
                raise UJLoadException('found POST Element, but no NVP or TEXTDATA subElements')

        self.items = []
        self.headers = []
        for nvp_item in element.findall(SCHEME_PREFIX+'NVP'):
            record = {'element': nvp_item, 'name': nvp_item.get('NAME'), 'type': nvp_item.get('TYPE'), 'value': booleanize(nvp_item)}
            if nvp_item.get('PLUGIN') == '1':
                self.headers.append(record)
            else:
                self.items.append(record)

        self.referenced_ddis = self.find_ddi_references()

    def __repr__(self):
        return self.name


    def find_ddi_references(self):
        # possible places for DDIs: URL, POST data, Validation, Headers, JS
        referenced_ddis = []
        # URL
        matches = re.findall(DDI_PATTERN, self.request)
        if len(matches):
            referenced_ddis.extend(matches)
        # POST data
        matches = re.findall(DDI_PATTERN, str([ z['name']+z['value'] for z in self.post_items ]))
        if len(matches):
            referenced_ddis.extend(matches)
        # Validation
        if self.success:
            matches = re.findall(DDI_PATTERN, self.success)
            if len(matches):
                referenced_ddis.extend(matches)
        # Headers
        matches = re.findall(DDI_PATTERN, str([ z['name']+z['value'] for z in self.headers ]))
        if len(matches):
            referenced_ddis.extend(matches)

        return set(referenced_ddis)


    def find_ddi_in_JS(self, ddi_name):
        JS_patterns = r'(getCurrentValue|getRefreshValue|setValues)\([\'\"](*DDINAME*)[\'\"]'.replace('*DDINAME*', ddi_name)
        matches = re.findall(DDI_PATTERN, str(self.headers))
        if len(matches):
            referenced_ddis.extend(matches)

        return matches

    def replace_ddi(self, old_name, new_name):

        # URL
        self.request = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', self.request)
        self.element.set('REQUEST', self.request)

        # POST data
        for post_item in self.post_items:
            post_item['name'] = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', post_item['name'])
            post_item['value'] = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', post_item['value'])
            post_item['element'].set('NAME', post_item['name'])
            post_item['element'].set('VALUE', post_item['value'])

        # Validation
        if self.success != None:
            self.success = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', self.success)
            self.success_element.text = self.success

        # Headers
        for header in self.headers:
            header['name'] = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', header['name'])
            header['value'] = re.sub(r'\{\{'+old_name+r'\}\}', '{{'+new_name+'}}', header['value'])
            header['element'].set('NAME', header['name'])
            header['element'].text = header['value']

        self.referenced_ddis = self.find_ddi_references()


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
        for step in steps_element.findall(SCHEME_PREFIX+'STEP'):
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

    def pull_steps_by_ddi(self, ddi_name):
        result = []
        for step in self.steps:
            if ddi_name in step.referenced_ddis:
                result.append(step)
        return result

    def replace_ddi_references(self, old_name, new_name):
        steps_with_references = self.pull_steps_by_ddi(old_name)
        for step in steps_with_references:
            step.replace_ddi(old_name, new_name)




    def __repr__(self):
        return str(ET.tostring(self.root))



