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
                result += '\n' + ' '*10 + str(step.id).center(5) + ' NAME: ' + step.name.ljust(32) + '\t URL: ' + step.request# + '\n'
                # for post in step.post_items:
                #     result += '\t\t' + post['name'] + ': ' + post['value']

        return result + '\n'

    def promote(self, lead_to_be):
        # find the stepgroup lead
        ex_lead = self.lead_step

        # swap the target step and the lead step in the steps list of the stepgroup object
        lead_position = self.steps.index(ex_lead)
        target_step_position = self.steps.index(lead_to_be)
        new_step_order = self.steps.copy()
        new_step_order[lead_position] = lead_to_be
        new_step_order[target_step_position] = ex_lead
        self.steps = new_step_order

        # exchange the id of the target step to the id of the lead step in objects & in XML
        ex_lead.id = lead_to_be.id
        ex_lead.element.set('ORDER', str(lead_to_be.id))
        lead_to_be.element.set('ORDER', str(self.id))
        lead_to_be.id = self.id

        # exchange the names:
        ### name of the ex-lead step based of the request url ((ensure it's unique))
        new_name = ex_lead.request.rsplit('/', 1)[1]
        if self.find_steps_by_attribute('name', new_name) != []:
            counter = 1
            while self.find_steps_by_attribute('name', new_name + ' (' + str(counter) + ')') != []:
                counter += 1
            new_name = new_name + ' (' + str(counter) + ')'

        ex_lead.name = new_name
        ex_lead.element.set('NAME', new_name)

        ### name of the target step is the name that was on the lead step
        lead_to_be.name = self.name
        lead_to_be.element.set('NAME', self.name)

        # reflect the new lead step in the stepgroup object
        self.lead_step = lead_to_be

    def delete_step(self, target_step):
        if target_step.id == self.id:
            new_lead = self.steps[1]
            # id_to_delete = new_lead.id
            self.promote(new_lead)
            del self.steps[1]
        else:
            self.steps.remove(target_step)


