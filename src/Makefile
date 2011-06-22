
all: test

test: nosetests parsetests

nosetests:
	nosetests

parsetests: genparse
	python scheme.py parse/test.eeyore

genparse: parse/EeyoreLexer.py parse/EeyoreParser.py

parse/EeyoreLexer.py: parse/eeyore.g
	runantlr -o parse parse/eeyore.g

parse/EeyoreParser.py: parse/eeyore.g
	runantlr -o parse parse/eeyore.g

