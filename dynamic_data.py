from siphon import Siphon

SCHEME_PREFIX = '{http://www.reflective.com}'

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
