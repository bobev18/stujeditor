import functools
import itertools

from xml.dom import minidom

import xml.etree.cElementTree as ET
from step import Step, StepNameException
# from dynamic_data import DynamicDataItem
from dynamic_data import ConstantDDI, DateDDI, DelimitedFileDDI, ListDDI, VariableDDI, RelatedDDI, ResponseDDI, AutoCorrelatedDDI, AutoIncrementDDI
from stepgroup import StepGroup

SCHEME_PREFIX = '{http://www.reflective.com}'
TYPE_TO_CLASS_MAP = {'AUTOCORR': AutoCorrelatedDDI, 'AUTOINCR': AutoIncrementDDI, 'CONSTANT': ConstantDDI, 'DATE    ': DateDDI, 'FLATFILE': DelimitedFileDDI,
                     'LIST    ': ListDDI, 'RESPONSE': ResponseDDI, 'SAMEAS  ': RelatedDDI, 'VARIABLE': VariableDDI,}

class DDINameException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

StepIDException = DDINameException
StepGroupIDException = DDINameException

class UserJourney():

    def __init__(self, uj_name, app_name='', version ='7.7'):
        self.name = uj_name
        self.app_name = app_name
        self.version = version

    def import_uj(self, filename):
        # self.filename = filename
        with open(filename, 'r') as f:
            raw = f.readlines()

        self.first_import_line = raw[0]

        ET.register_namespace('', SCHEME_PREFIX[1:-1])
        tree = ET.parse(filename)
        root = tree.getroot()
        self.name = root.attrib['NAME']
        self.app_name = root.attrib['APPNAME']
        self.version = root.attrib['VERSION']

        created = root.find(SCHEME_PREFIX+'CREATED')
        self.created = created.text

        self.uj_global_settings = []
        for nvp in root.findall(SCHEME_PREFIX+'NVP'):
            self.uj_global_settings.append({'NAME': nvp.attrib['NAME'], 'PLUGIN': nvp.attrib['PLUGIN'], 'TYPE': nvp.attrib['TYPE'], 'text': nvp.text})



        #### Dynamic Data Items ###
        dditems_element = root.find(SCHEME_PREFIX+'DYNAMICDATA')
        self.dditems = []

        for ddi in dditems_element.findall(SCHEME_PREFIX+'DDITEM'):
            ddi_type = ddi.find(SCHEME_PREFIX+'SOURCE').attrib['TYPE']
            self.dditems.append(TYPE_TO_CLASS_MAP[ddi_type](ddi))

        #### Steps & Step-Groups ####
        # stepgroups are not defined in the XML, so to construct a stepgroup, we need list of all the steps
        steps_element = root.find(SCHEME_PREFIX+'STEPS')
        stepgroups = []
        stepgroup_steps = []
        lead_step = None
        last_step_stepgroup_id = -1
        for step in steps_element.findall(SCHEME_PREFIX+'STEP'):
            current_step = Step(step)

            if last_step_stepgroup_id == -1: # adjust for starting element
                lead_step = current_step
                last_step_stepgroup_id = current_step.stepgroup_id

            if current_step.stepgroup_id != last_step_stepgroup_id:
                stepgroups.append(StepGroup(lead_step, stepgroup_steps))
                lead_step = current_step
                stepgroup_steps = [current_step]
                last_step_stepgroup_id = current_step.id
            else:
                stepgroup_steps.append(current_step)

        # finalize after last step
        stepgroups.append(StepGroup(lead_step, stepgroup_steps))
        # lead_step = current_step
        # stepgroup_steps = [current_step]
        # last_step_stepgroup_id = current_step.id

        self.stepgroups = stepgroups

    def list_ddi_names(self):
        return [z.name for z in self.dditems]

    def find_ddi_by_name(self, name):
        for ddi in self.dditems:
            if ddi.name == name:
                return ddi
        return None

    def find_ddis_by_attribute(self, attrib, value):
        result = []
        for ddi in self.dditems:
            if getattr(ddi, attrib) == value:
                result.append(ddi)
        return result

    def list_step_names(self):
        return functools.reduce(lambda x,y: x+y, [z.list_step_names() for z in self. stepgroups])

    def find_step_by_name(self, name):
        for stepgroup in self.stepgroups:
            match = stepgroup.find_steps_by_attribute('name', name)
            if len(match):
                return match[0]

        return None

    def find_step_by_id(self, id_):
        for stepgroup in self.stepgroups:
            match = stepgroup.find_steps_by_attribute('id', id_)
            if len(match):
                return match[0]

        return None

    def find_steps_by_attribute(self, attrib, value):
        result = []
        for stepgroup in self.stepgroups:
            result.extend(stepgroup.find_steps_by_attribute(attrib, value))
        return result

    def find_steps_by_ddi_reference(self, ddi_name):
        result = []
        for stepgroup in self.stepgroups:
            result.extend(stepgroup.find_steps_by_ddi_reference(ddi_name))
        return result

    def replace_ddi_references(self, old_name, new_name):
        steps_with_references = self.find_steps_by_ddi_reference(old_name)
        for step in steps_with_references:
            step.replace_ddi(old_name, new_name)

    def rename_ddi(self, old_name, new_name):
        if new_name not in self.list_ddi_names():
            target_ddi = self.find_ddi_by_name(old_name)
            target_ddi.rename(new_name)
            self.replace_ddi_references(old_name, new_name)
        else:
            raise DDINameException('new DDI name - ', new_name, ' already exists')

    def rename_step(self, old_name, new_name):
        if new_name not in self.list_step_names():
            target_step = self.find_step_by_name(old_name)
            target_step.rename(new_name)
        else:
            raise StepNameException('new step name - ', new_name, ' already exists')

    def list_stepgroup_names(self):
        return [z.name for z in self.stepgroups]

    # def __repr__(self):
        # return str(ET.tostring(self.root))

    def tree_output(self):
        result = ''
        for stepgroup in self.stepgroups:
            result += stepgroup.tree_output()
            if stepgroup.lead_step.flow_control_element:
                result = result[:-1]
                destination_names = []
                for destination in [ z for z in stepgroup.lead_step.flow_items if z['name'] == 'DESTINATIONSTEP' ]:
                    try:
                        name = self.find_step_by_id(int(destination['value'])).name
                    except (ValueError, AttributeError):
                        name = destination['value']
                    destination_names.append(name)
                result += ' -->> ' + '|'.join(destination_names) +'\n'

        return result

    def find_stepgroup_by_id(self, id_):
        groups_wiht_id = [ z for z in self.stepgroups if z.id == id_ ]
        if len(groups_wiht_id) != 1:
            return None
            # message = str(len(groups_wiht_id)) + ' stepgroups found for id ' + str(id_)
            # raise StepGroupIDException(message)

        return groups_wiht_id[0]

    def find_stepgroup_by_step_id(self, id_):
        target_step = self.find_step_by_id(id_)
        if target_step == None:
            return None
        return self.find_stepgroup_by_id(target_step.stepgroup_id), target_step

    def promote_step_to_lead(self, id_):
        # lead_to_be = self.find_step_by_id(id_)
        target_stepgroup, lead_to_be = self.find_stepgroup_by_step_id(id_)
        target_stepgroup.promote(lead_to_be)

    def change_uj_name(self, new_name):
        self.name = new_name
        # self.root.set('NAME', new_name)

    def xml(self):
        ET.register_namespace('', SCHEME_PREFIX[1:-1])
        root = ET.Element("USERJOURNEY", {'APPNAME': self.app_name, 'NAME': self.name, 'VALID': 'true', 'VERSION': self.version})
        root.set('xmlns', "http://www.reflective.com")
        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        root.set('xsi:schemaLocation', "http://www.reflective.com stschema.xsd")
        # root.set('APPNAME', self.app_name)
        # root.set('NAME', self.name)
        # root.set('VALID', 'true')
        # root.set('VERSION', self.version)

        description = ET.SubElement(root, 'DESCRIPTION')
        plugin = ET.SubElement(root, 'PLUGIN', {'ID': '1'})
        responseprocessor = ET.SubElement(root, 'RESPONSEPROCESSOR')
        created = ET.SubElement(root, 'CREATED')
        created.text = self.created

        for nvp in self.uj_global_settings:
            text = nvp['text']
            attributes = {key: value for key, value in nvp.items() if key is not 'text'}
            new_nvp = ET.SubElement(root, 'NVP', attributes)
            new_nvp.text = text

        dynamic_data_element = ET.SubElement(root, 'DYNAMICDATA')
        for ddi in self.dditems:
            dynamic_data_element.append(ddi.xml())

        steps_element = ET.SubElement(root, 'STEPS')
        for step in [step for sg in self.stepgroups for step in sg.steps]:
            st = step.xml()
            steps_element.append(step.xml())


        # tree = ET.ElementTree(root)
        # tree.write("page.xhtml")

        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent='\t').replace('<?xml version="1.0" ?>\n', self.first_import_line)

    def export_uj(self, filename):
        with open(filename, 'w') as xml_file:
            xml_file.write(self.xml())


    def push_stepgroup_changes_to_XML(self):
        new_step_list = list(itertools.chain(*[z.steps for z in self.stepgroups]))
        new_step_list = [z.element for z in new_step_list]
        steps_element = self.root.find(SCHEME_PREFIX+'STEPS')
        container = self.root.find(SCHEME_PREFIX+'STEPS')
        if len(new_step_list):
            container[:] = new_step_list
        else:
            if container != None:
                self.root.remove(steps_element)

    def write_to_file(self, file_name):
        self.push_stepgroup_changes_to_XML()

        if not len(self.dditems):
            self.root.remove(self.dditems_element)

        with open(file_name, 'w') as xml_file:
            xml_file.write(self.raw.split('\n')[0] + '\n' + ET.tostring(self.root).decode("utf-8"))

    def delete_step_by_id(self, id_):
        # target_step = self.find_step_by_id(id_)
        target_stepgroup, target_step = self.find_stepgroup_by_step_id(id_)
        # print('group len', len(target_stepgroup.steps))
        if len(target_stepgroup.steps) == 1:
            self.stepgroups.remove(target_stepgroup)
        else:
            target_stepgroup.delete_step(target_step)

    def delete_ddi(self, ddi_name):
        target_ddi = self.find_ddi_by_name(ddi_name)
        # self.dditems_element.remove(target_ddi.element)
        self.dditems.remove(target_ddi)



