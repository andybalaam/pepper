# Copyright (C) 2011-2013 Andy Balaam and The MetaPepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

GRAMMAR=metapepper.g
GENS=gen/MetaPepperLexer.py gen/MetaPepperParser.py

RUNANTLR=runantlr -o gen/ $(1) && touch $(2)

export PATH := ${PWD}:${PATH}

all: genparse runparse

genparse: $(GENS)

runparse: $(GENS)
	python run.py test.metapepper
	

gen/MetaPepper%.py: $(GRAMMAR)
	$(call RUNANTLR,$(GRAMMAR),$(GENS))

clean:
	rm $(GENS)
	find ./ -name "*.pyc" -delete

