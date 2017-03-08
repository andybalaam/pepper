all: test

pep8:
	python3 -m pep8 .

test: pep8
	python3 -m unittest discover --quiet --failfast tests
	python3 -m doctest `find ./ -name '*.py'`

setup:
	sudo apt install python3 python3-pep8
