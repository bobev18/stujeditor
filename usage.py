from userjourney import UserJourney


SCHEME_PREFIX = '{http://www.reflective.com}'

uj = UserJourney('Update Purchase Order User Journey.xml')

# print(uj.pull_ddi_by('name', 'Update Purchase Order ID 21').siphons)

# id13 = uj.find_ddi_by_name('Update Purchase Order ID 13')
# print(id13.name, '\n', id13.siphons)

# id13.rename('MXID Item')

# print()
# item_desc_step = uj.find_step_by_name('Item Description')
# print('step:', item_desc_step, ';; validation:', item_desc_step.success)


# print()
# print('-'*20)

# uj = UserJourney('Update Work Order User Journey.xml')
# for ddi in uj.dditems:
# 	for s in ddi.siphons:
# 		if s.type == 'R':
# 			# print(s.start)

# 			# print([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5'] ])
# 			if any([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5', 'mx\\d'] ]):
# 				print('>>>',s.start)

# steps_csrftoken = uj.find_steps_by_ddi_reference('csrftoken')
# print(len(steps_csrftoken))
# print(steps_csrftoken)
# print(type(steps_csrftoken[0]))
# print(str([ z['name']+z['value'] for z in steps_csrftoken[0].post_items ]))
# print(str([ z['name']+z['value'] for z in steps_csrftoken[0].headers ]))

# print()
# print('-'*20)
# print()



# print(uj.find_stepgroup_by_id(2).name)


# while uj.stepgroups != []:
# 	sg = uj.stepgroups[0]
# 	print('working sg ', sg.name)
# 	# while sg.steps
# 	for s in reversed(sg.steps):
# 		print('sg', sg, 's', s, 'id', s.id, s.request)
# 		uj.delete_step_by_id(s.id)

# 	print(uj.tree_output())
# 	# print('---', sg.tree_output())
# 	print([z.name for z in uj.stepgroups])
# 	# print('\t'*5, uj.find_stepgroup_by_id(14).steps)

uj.stepgroups = []

uj.push_stepgroup_changes_to_XML()

print('-'*20)
print(uj.tree_output())
print('-'*20)
print(uj)

uj.change_uj_name('delme')
# steps_element = uj.root.find(SCHEME_PREFIX+'STEPS')
# uj.root.remove(steps_element)
uj.write_to_file('delme UJ.xml')
