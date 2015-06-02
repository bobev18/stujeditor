from userjourney import UserJourney


SCHEME_PREFIX = '{http://www.reflective.com}'

uj = UserJourney('Availability Manager.xml')

user_named_steps = uj.find_steps_by_attribute('name_user_defined', True)
for step in user_named_steps:
	print(step.name)