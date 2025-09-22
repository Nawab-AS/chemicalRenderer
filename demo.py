import chemical_renderer

while True:
	name = input('enter a organic chemical name or type exit: ')
	if name == "exit":
		break
	try:
		chemical = chemical_renderer.Molecule(name)
		print(chemical.description())
		chemical.render('test2.svg')
	except chemical_renderer.ParseError as err:
		print("\033[1m\033[33m", err, "\033[0m")
		print(name, 'is an invalid chemical name')
