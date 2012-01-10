
EGRAMMAR=parse/eeyore.g
EGENS=parse/EeyoreLexer.py parse/EeyoreParser.py parse/EeyoreTreeWalker.py

LGRAMMAR=parse/lexed.g
LGENS=parse/LexedLexer.py parse/LexedParser.py

RUNANTLR=runantlr -o parse/ $(1) && touch $(2)

export PATH := ${PWD}:${PATH}

all: genparse

test: genparse
	python test/eeyorenosetests.py --with-eeyoresamplenoseplugin

quick-test:
	nosetests

parsetests: genparse
	python scheme.py parse/test.eeyore

genparse: $(EGENS) $(LGENS)

parse/Eeyore%.py: $(EGRAMMAR)
	$(call RUNANTLR,$(EGRAMMAR),$(EGENS))

parse/Lexed%.py: $(LGRAMMAR)
	$(call RUNANTLR,$(LGRAMMAR),$(LGENS))

clean:
	rm $(EGENS)
