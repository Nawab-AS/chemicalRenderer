import chemical_renderer

while True:
	name = input('\nenter a organic chemical name or type exit: ')
	if name == "exit":
		break
	try:
		chemical = chemical_renderer.Molecule(name)
		print(chemical.description())
		chemical.render(f'{name}.svg')
		print(f'SVG file saved as {name}.svg')
	except chemical_renderer.ParseError as err:
		print("\033[1m\033[33m", err, "\033[0m")
		print(name, 'is an invalid chemical name')
