# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


EGRAMMAR=parse/pepper.g
EGENS=parse/PepperLexer.py parse/PepperParser.py parse/PepperTreeWalker.py

LGRAMMAR=parse/lexed.g
LGENS=parse/LexedLexer.py parse/LexedParser.py

RUNANTLR=runantlr -o parse/ $(1) && touch $(2)

export PATH := ${PWD}:${PATH}

all: genparse

test: genparse
	python test/peppernosetests.py --with-peppersamplenoseplugin

quick-test: genparse
	nosetests

parsetests: genparse
	python scheme.py parse/test.pepper

genparse: $(EGENS) $(LGENS)

parse/Pepper%.py: $(EGRAMMAR)
	$(call RUNANTLR,$(EGRAMMAR),$(EGENS))

parse/Lexed%.py: $(LGRAMMAR)
	$(call RUNANTLR,$(LGRAMMAR),$(LGENS))

clean:
	rm $(EGENS)
	find ./ -name "*.pyc" -delete

