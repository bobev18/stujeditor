from userjourney import UserJourney

uj = UserJourney('Update Purchase Order User Journey.xml')

# print(uj.pull_ddi_by('name', 'Update Purchase Order ID 21').siphons)

id13 = uj.pull_ddi_by('name', 'Update Purchase Order ID 13')
print(id13.name, '\n', id13.siphons)

id13.rename('MXID Item')


# print('-'*20)
# for ddi in uj.dditems:
# 	for s in ddi.siphons:
# 		if s.type == 'R':
# 			# print(s.start)

# 			# print([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5'] ])
# 			if any([ s.start.count(z) for z in ['[^~]', '\\1', '\\2', '\\3', '\\4', '\\5', 'mx\\d'] ]):
# 				print('>>>',s.start)

steps_csrftoken = uj.pull_steps_by_ddi('csrftoken')
print(len(steps_csrftoken))
print(steps_csrftoken)
print(type(steps_csrftoken[0]))