import functools
import itertools

import xml.etree.cElementTree as ET
from step import Step, StepNameException
from dynamic_data import DynamicDataItem
from stepgroup import StepGroup

SCHEME_PREFIX = '{http://www.reflective.com}'

class DDINameException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

StepIDException = DDINameException
StepGroupIDException = DDINameException

class UserJourney():

    def __init__(self, filename):
        # self.filename = filename
        with open(filename, 'r') as f:
            self.raw = f.read()

        ET.register_namespace('', 'http://www.reflective.com')
        self.tree = ET.parse(filename)
        # self.tree = ET.ElementTree(file=filename)
        self.root = self.tree.getroot()
        self.name = self.root.attrib['NAME']


        dditems_element = self.root.find(SCHEME_PREFIX+'DYNAMICDATA')
        self.dditems = []
        for ddi in dditems_element.findall(SCHEME_PREFIX+'DDITEM'):
            self.dditems.append(DynamicDataItem(ddi))

        self.stepgroups = self.capture_stepgroups()

        # self.parent_map = {child:parent for parent in self.tree.iter() for child in parent}

    def capture_stepgroups(self):
        # stepgroups are not defined in the XML, so to construct a stepgroup, we need list of all the steps
        steps_element = self.root.find(SCHEME_PREFIX+'STEPS')
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
        lead_step = current_step
        stepgroup_steps = [current_step]
        last_step_stepgroup_id = current_step.id

        return stepgroups

    def list_ddi_names(self):
        return [z.name for z in self.dditems]

    def find_ddi_by_name(self, name):
        for ddi in self.dditems:
            if ddi.name == name:
                return ddi
        return None

    # def find_ddis_by_attribute(self, attrib, value):
    #     result = []
    #     for ddi in self.dditems:
    #         if getattr(ddi, attrib) == value:
    #             result.append(ddi)
    #     return result

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

    def __repr__(self):
        return str(ET.tostring(self.root))

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
        self.root.set('NAME', new_name)

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




