import xml.etree.cElementTree as ET
# import re
from step import Step
from dynamic_data import DynamicDataItem
from stepgroup import StepGroup

SCHEME_PREFIX = '{http://www.reflective.com}'

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
        self.steps = []
        orphans = []
        order_ids_used_for_stepgroup = []
        for step in steps_element.findall(SCHEME_PREFIX+'STEP'):
            self.steps.append(Step(step))
            if self.steps[-1].stepgroup != None:
                order_ids_used_for_stepgroup.append(self.steps[-1].stepgroup)
            else:
                orphans.append(self.steps[-1].order)

        order_ids_used_for_stepgroup = set(order_ids_used_for_stepgroup)
        stepgroups = []
        for stepgroup_id in order_ids_used_for_stepgroup:
            # print([(z.name, z.order, z.stepgroup) for z in self.steps])
            # leading_step = [ z for z in self.steps if z.order == stepgroup_id ]
            # print(stepgroup_id, leading_step)
            # if len(leading_step):
            leading_step = [ z for z in self.steps if z.order == stepgroup_id ][0]
            subscribed_steps = [ z for z in self.steps if z.stepgroup == stepgroup_id ]
            stepgroups.append(StepGroup(leading_step, subscribed_steps))

        for step_id in orphans:
            orphan_step = [ z for z in self.steps if z.order == step_id ][0]
            stepgroups.append(StepGroup(orphan_step, orphan_step))

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

    def rename_ddi(self, old_name, new_name):
        target_ddi = self.pull_ddi_by('name', old_name)
        target_ddi.rename(new_name)
        self.replace_ddi_references(old_name, new_name)

    def list_stepgroup_names(self):
        return [z.name for z in self.stepgroups]


    def __repr__(self):
        return str(ET.tostring(self.root))
