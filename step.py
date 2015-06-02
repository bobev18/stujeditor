import re

DDI_PATTERN = r'\{\{(.+?)\}\}'
SCHEME_PREFIX = '{http://www.reflective.com}'

class UJLoadPostDataException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

class StepNameException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]


        # <STEP COUNTASTRANSACTION="false" EXECUTESEPARATELY="false"
        #     FIRSTCYCLEONLY="false" LASTCYCLEONLY="false"
        #     NAME="More Pages" NAMEUSERDEFINED="true" ORDER="33"
        #     PROCESSRESPONSE="false" TYPE="CONTROL">
        #     <REQUEST URL=" "/>
        #     <DESCRIPTION/>
        #     <SLEEPTIME>0</SLEEPTIME>
        #     <NVP NAME="logRequest" TYPE="java.lang.Boolean">false</NVP>
        #     <FLOWCONTROL TYPE="VARIABLELOOP">
        #         <NVP NAME="DESTINATIONSTEP" ORDER="0">10</NVP>
        #         <NVP NAME="MAXITERCOUNT" ORDER="0">10</NVP>
        #         <NVP NAME="MINITERCOUNT" ORDER="0">5</NVP>
        #         <NVP NAME="SLEEPTIME" ORDER="0">0.0</NVP>
        #     </FLOWCONTROL>
        # </STEP>

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
        self.name_user_defined = element.get('NAMEUSERDEFINED') == 'true'
        self.nameuserdefined = bool(element.get('NAMEUSERDEFINED'))
        # print('>>>>', element.tag, element.attrib)
        self.id = int(element.get('ORDER'))
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
            self.stepgroup_id = int(self.stepgroup_element.text)
        else:
            self.stepgroup_id = self.id

        self.post_element = element.find(SCHEME_PREFIX+'POST')
        self.post_items = []
        if self.post_element:
            if len(self.post_element.findall(SCHEME_PREFIX+'NVP')):
                for post_item in self.post_element.findall(SCHEME_PREFIX+'NVP'):
                    self.post_items.append({'element': post_item, 'name': post_item.get('NAME'), 'value': post_item.get('VALUE')})
            if len(self.post_element.findall(SCHEME_PREFIX+'TEXTDATA')):
                self.post_items.append({'element': self.post_element.find(SCHEME_PREFIX+'TEXTDATA'), 'name': '', 'value': self.post_element.find(SCHEME_PREFIX+'TEXTDATA').text})

            if len(self.post_items) == 0:
                raise UJLoadPostDataException('found POST Element, but no NVP or TEXTDATA subElements')

        self.items = []
        self.headers = []
        for nvp_item in element.findall(SCHEME_PREFIX+'NVP'):
            record = {'element': nvp_item, 'name': nvp_item.get('NAME'), 'type': nvp_item.get('TYPE'), 'value': booleanize(nvp_item)}
            if nvp_item.get('PLUGIN') == '1':
                self.headers.append(record)
            else:
                self.items.append(record)

        self.flow_control_element = element.find(SCHEME_PREFIX+'FLOWCONTROL')
        if self.flow_control_element:
            self.flow_type = self.flow_control_element.get('TYPE')
            # print('flow control found at ', self.id, 'with type', self.flow_type)
            self.flow_items = []
            for nvp_item in self.flow_control_element.findall(SCHEME_PREFIX+'NVP'):
                self.flow_items.append({'name': nvp_item.get('NAME'), 'order': nvp_item.get('ORDER'), 'value': nvp_item.text})

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
        matches = re.findall(DDI_PATTERN, str([ z['name']+str(z['value']) for z in self.headers ]))
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


    def rename(self, new_name):
        self.name = new_name
        self.name_user_defined = True
        self.element.set('NAME', new_name)
        self.element.set('NAMEUSERDEFINED', 'true')