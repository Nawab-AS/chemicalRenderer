import substance

while True:
	name = input('enter a organic chemical name or type exit: ')
	if name == "exit":
		break
	try:
		methane = substance.Substance(name)
	except ValueError:
		print(name, 'is an invalid chemical name')

