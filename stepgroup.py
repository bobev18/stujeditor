class StepGroup():

    def __init__(self, lead_step, steps):
        self.lead_step = lead_step
        self.order = lead_step.order
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
