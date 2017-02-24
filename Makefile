all: test

pep8:
	# TODO python3 -m pep8 .

test: pep8
	python3 -m unittest discover tests

setup:
	sudo apt install python3 python3-pep8
