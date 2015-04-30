import xml.etree.cElementTree as ET
# import re
from step import Step
from dynamic_data import DynamicDataItem

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

        steps_element = self.root.find(SCHEME_PREFIX+'STEPS')
        self.steps = []
        for step in steps_element.findall(SCHEME_PREFIX+'STEP'):
            self.steps.append(Step(step))

        # self.stepgroups = self.


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
