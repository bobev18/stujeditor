from userjourney import UserJourney

uj = UserJourney('Update Purchase Order User Journey.xml')

# print(uj.pull_ddi_by('name', 'Update Purchase Order ID 21').siphons)

id13 = uj.find_ddi_by_name('Update Purchase Order ID 13')
print(id13.name, '\n', id13.siphons)

id13.rename('MXID Item')

print()
item_desc_step = uj.find_step_by_name('Item Description')
print('step:', item_desc_step, ';; validation:', item_desc_step.success)


print()
print('-'*20)

uj = UserJourney('Update Work Order User Journey.xml')
for ddi in uj.dditems:
	for s in ddi.siphons:
		if s.type == 'R':
			# print(s.start)

			# print([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5'] ])
			if any([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5', 'mx\\d'] ]):
				print('>>>',s.start)

steps_csrftoken = uj.find_steps_by_ddi_reference('csrftoken')
print(len(steps_csrftoken))
print(steps_csrftoken)
print(type(steps_csrftoken[0]))
print(str([ z['name']+z['value'] for z in steps_csrftoken[0].post_items ]))
print(str([ z['name']+z['value'] for z in steps_csrftoken[0].headers ]))

print()
print('-'*20)
print()

for ddi in uj.dditems
	.elem

print(uj.tree_output())

