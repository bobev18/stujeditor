import functools

import xml.etree.cElementTree as ET
from step import Step, StepNameException
from dynamic_data import DynamicDataItem
from stepgroup import StepGroup

SCHEME_PREFIX = '{http://www.reflective.com}'

class DDINameException(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]

StepIDException = DDINameException

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

        self.parent_map = {child:parent for parent in self.tree.iter() for child in parent}

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

    def promote_step_to_lead(self, id_):
        # find target step
        # find the stepgroup of the target step i.e target stepgroup
        # find the stepgroup lead
        # swap the target step and the lead step in the steps list of the stepgroup object
        # swap the target step and the lead step in the XML
        # exchange the id of the target step to the id of the lead step in objects
        # exchange the id of the target step to the id of the lead step in the XML
        # exchange the names:
        #  - name of the target step is the name that was on the lead step
        #  - name the ex-lead step based of the request url ((ensure it's unique))
        # reflect name changes in the XML
        # reflect the new lead step in the stepgroup object
        #


        # find target step
        lead_to_be = self.find_step_by_id(id_)

        # find the stepgroup of the target step i.e target stepgroup
        eligible_stepgroups = [ z for z in self.stepgroups if z.id == lead_to_be.stepgroup_id]
        if len(eligible_stepgroups) == 0:
            message = 'no eligible stepgroups found for step with id ' + str(id_)
            raise StepIDException(message)
        elif len(eligible_stepgroups) == 1:
            target_stepgroup = eligible_stepgroups[0]
        else:
            raise StepIDException('UJ error - there are two or more stepgroups with duplicate ids')

        # find the stepgroup lead
        ex_lead = target_stepgroup.lead_step

        # swap the target step and the lead step in the steps list of the stepgroup object
        lead_position = 0 # target_stepgroup.steps.index(ex_lead)
        target_step_position = target_stepgroup.steps.index(lead_to_be)
        new_step_order = target_stepgroup.steps.copy()
        new_step_order[lead_position] = lead_to_be
        new_step_order[target_step_position] = ex_lead
        target_stepgroup.steps = new_step_order

        # swap the target step and the lead step in the XML
        # print('~'*100)
        # print(self.parent_map)
        # print(ex_lead)
        # print(self.parent_map[ex_lead])
        self.parent_map[ex_lead.element].remove(lead_to_be.element)
        self.parent_map[ex_lead.element].insert(0, lead_to_be.element)


        # exchange the id of the target step to the id of the lead step in objects
        ex_lead.id = lead_to_be.id
        lead_to_be.id = target_stepgroup.id
        # exchange the id of the target step to the id of the lead step in the XML
        ex_lead.element.set('ORDER', lead_to_be.id)
        lead_to_be.element.set('ORDER', target_stepgroup.id)
        # exchange the names:
        #  - name the ex-lead step based of the request url ((ensure it's unique))
        new_name = ex_lead.request.rsplit('/', 1)[1]
        if self.find_step_by_name(new_name) != None:
            counter = 1
            while self.find_step_by_name(new_name + ' (' + str(counter) + ')') != None:
                counter += 1

            new_name = new_name + ' (' + str(counter) + ')'

        ex_lead.name = new_name
        ex_lead.element.set('NAME', new_name)

        #  - name of the target step is the name that was on the lead step
        lead_to_be.name = target_stepgroup.name
        lead_to_be.element.set('NAME', target_stepgroup.name)

        # reflect the new lead step in the stepgroup object
        target_stepgroup.lead_step = lead_to_be
