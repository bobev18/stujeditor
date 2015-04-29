import xml.etree.cElementTree as ET

# tree = ET.ElementTree(file='no_scheme_Update Purchase Order User Journey.xml')
# root = tree.getroot()
# print(root.attrib['NAME'])

# for child_of_root in root:
# 	print (child_of_root.tag, child_of_root.attrib)

# for elem in tree.iter(tag='DDITEM'):
# 	print('DDI',elem.tag, elem.attrib)


SCHEME_PREFIX = '{http://www.reflective.com}'

tree = ET.ElementTree(file='Update Purchase Order User Journey.xml')
root = tree.getroot()
print(root.attrib['NAME'])

for child_of_root in root:
	print (child_of_root.tag, child_of_root.attrib)

print('='*10)
ddis = root.find(SCHEME_PREFIX + 'DYNAMICDATA')
for child_of_root in ddis:
	print (child_of_root.tag, child_of_root.attrib)

for ddi in ddis.findall(SCHEME_PREFIX + 'DDITEM'):
	print (ddi.tag, '|||', ddi.attrib)
	# ET.dump(ddi)

first_ddi = ddis.findall(SCHEME_PREFIX + 'DDITEM')[0]
print('>> DDI element [0] attrib EXISTING = ', first_ddi.attrib['EXISTING'])
for child in first_ddi.getchildren():
	print (child.tag, '|||', child.attrib)

sixst_ddi = ddis.findall(SCHEME_PREFIX + 'DDITEM')[6]
print('>> DDI element [0] SOURCE TYPE = ', first_ddi.find(SCHEME_PREFIX+'SOURCE').attrib['TYPE'])
print('>> DDI element [0] DESCRIPTION = ', first_ddi.find(SCHEME_PREFIX+'DESCRIPTION').text)
print('>> DDI element [6] DESCRIPTION = ', sixst_ddi.find(SCHEME_PREFIX+'DESCRIPTION').text)

sixst_items = {}
for item in sixst_ddi.findall(SCHEME_PREFIX+'ITEM'):
	sixst_items[item.get('CODE')] = item.text

print('>> DDI element [6] ITEMS:')
for key, val in sixst_items.items():
	print(key,':',val)

print('~'*20)
print
ddi_mxid21 = [ z for z in ddis.findall(SCHEME_PREFIX+'DDITEM') if z.attrib['NAME'] == "Update Purchase Order ID 21" ][0]

siphons = ddi_mxid21.find(SCHEME_PREFIX+'SIPHONS')
# print(siphons)
mxid21_siphons = {}
for sip in siphons.findall(SCHEME_PREFIX+'SIPHON'):
	print (sip.tag, '|||', sip.attrib)
	sip_items = {}
	for item in sip.getchildren():
		sip_items[item.tag.replace(SCHEME_PREFIX,'')] = item.text

	print([sip.get('SEQUENCE'), sip.get('TYPE')])
	mxid21_siphons[ sip.get('SEQUENCE')+sip.get('TYPE') ] = sip_items

print()
print('>> DDI element ', ddi_mxid21.get('NAME'), ' ITEMS:')
for key, val in mxid21_siphons.items():
	print(key,':',val)

ddi_mxid21.set('NAME', 'MXID WO Task')
print('>> DDI element 21 is renamed to "', ddi_mxid21.get('NAME'),'"')

# ET.dump(tree)
# print(type(ET.tostring(root)))
# print(str(ET.tostring(root)))

# ===================================================================================
# ===================================================================================



print('='*20)
steps = root.find(SCHEME_PREFIX + 'STEPS')
# for child in steps:
# 	print (child.tag, child.attrib)

for step in steps.findall(SCHEME_PREFIX + 'STEP'):
	print (step.tag, '|||', step.attrib)
	# ET.dump(ddi)

print('-'*10)

import re

with open('Update Purchase Order User Journey.xml', 'r') as f:
	raw = f.read()

# matches = re.findall(r'<step [^~]+?name="(?P<name>.+?)".+?order="(?P<order>\d+?)"[^~]+?<stepgroup>(?P<group>\d+?)</stepgroup>', raw, re.I)
# print(matches)
matches = re.finditer(r'<step [^~]+?name="(?P<name>.+?)".+?order="(?P<order>\d+?)"[^~]+?<stepgroup>(?P<group>\d+?)</stepgroup>', raw, re.I)
# print([z.groupdict() for z in matches])
mlist = [z.groupdict() for z in matches]
st_gr_list = [ z['group'] for z in mlist ]
for st_id in st_gr_list:
	print([ z['name'] for z in mlist if z['order']==st_id  ])