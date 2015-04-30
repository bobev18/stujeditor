class StepGroup():

	def __init__(self, lead_step, steps):
		self.lead_step = lead_step
		self.order = lead_step.order
		self.name = lead_step.name
		self.steps = steps

