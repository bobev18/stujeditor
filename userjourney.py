import functools

import xml.etree.cElementTree as ET
from step import Step, StepNameException
from dynamic_data import DynamicDataItem
from stepgroup import StepGroup

SCHEME_PREFIX = '{http://www.reflective.com}'

class DDINameException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

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

        self.stepgroups = self.capture_stepgroups()

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
                destination_names = []
                for destination in [ z for z in stepgroup.lead_step.flow_items if z['name'] == 'DESTINATIONSTEP' ]:
                    try:
                        name = self.find_step_by_id(int(destination['value'])).name
                    except ValueError:
                        name = destination['value']
                    destination_names.append(name)
                result += ' -->> ' + '|'.join(destination_names) +'\n'

        return result
