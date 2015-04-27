import xml.etree.cElementTree as ET


class UserJourney():

	def __init__(self, filename):
		# self.filename = filename
		with open(filename, 'r') as f:
			self.raw = f.read()
		self.tree = ET.ElementTree(file=filename)
		self.root = self.tree.getroot()
		self.name = self.root.attrib['NAME']

	def load(self):
		pass



