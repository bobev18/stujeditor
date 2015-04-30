MAX_STEP_NAME_LENGTH = 32

class StepGroup():

    def __init__(self, lead_step, steps):
        self.lead_step = lead_step
        self.id = lead_step.id
        self.name = lead_step.name
        self.steps = steps

    def find_steps_by_attribute(self, attribute, value):
        result = []
        for step in self.steps:
            if getattr(step, attribute) == value:
                result.append(step)

        return result

    def find_steps_by_ddi_reference(self, ddi_name):
        result = []
        for step in self.steps:
            if ddi_name in step.referenced_ddis:
                result.append(step)
        return result

    def list_step_names(self):
        return [z.name for z in self.steps]

    def tree_output(self):
        # result = '[ '+str(self.order).center(5) + ' ] ' + self.name + '\n'
        result = str(self.id).center(5) + self.name.ljust(MAX_STEP_NAME_LENGTH)
        if not self.lead_step.flow_control_element:
            for step in self.steps:
                # result += ' '*10 + '[ ' + str(step.order).center(5) + ' ] NAME: ' + step.name.ljust(32) + '\t URL: ' + step.request + '\n'
                result += '\n' + ' '*10 + str(step.id).center(5) + ' NAME: ' + step.name.ljust(32) + '\t URL: ' + step.request + '\n'
                # for post in step.post_items:
                #     result += '\t\t' + post['name'] + ': ' + post['value']

        return result
