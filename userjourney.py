import functools

import xml.etree.cElementTree as ET
from step import Step
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
        steps = []
        orphans = []
        stepgroup_ids = []
        for step in steps_element.findall(SCHEME_PREFIX+'STEP'):
            current_step = Step(step)
            steps.append(current_step)
            current_step_stepgroup = current_step.stepgroup
            if current_step_stepgroup != None:
                if current_step_stepgroup not in stepgroup_ids:
                    stepgroup_ids.append(current_step_stepgroup)
            else:
                orphans.append(current_step.order)

        # stepgroup_ids = set(stepgroup_ids)

        stepgroups = []
        for stepgroup_id in stepgroup_ids:
            leading_step = [ z for z in steps if z.order == stepgroup_id ][0]
            subscribed_steps = [ z for z in steps if z.stepgroup == stepgroup_id ]
            stepgroups.append(StepGroup(leading_step, subscribed_steps))

        for step_id in orphans:
            orphan_step = [ z for z in steps if z.order == step_id ][0]
            stepgroups.append(StepGroup(orphan_step, [orphan_step]))

        return stepgroups

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
        return functools.reduce(lambda x,y: x+y, [z.list_step_names() for z in self. stepgroups])

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
            target_ddi = self.pull_ddi_by('name', old_name)
            # print(old_name, new_name, target_ddi)
            # target_ddi = target_ddi[0]
            target_ddi.rename(new_name)
            self.replace_ddi_references(old_name, new_name)
        else:
            raise DDINameException('new DDI name - ', new_name, ' already exists')

    def list_stepgroup_names(self):
        return [z.name for z in self.stepgroups]


    def __repr__(self):
        return str(ET.tostring(self.root))
