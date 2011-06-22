
GRAMMAR=parse/eeyore.g
GEN_LEX=parse/EeyoreLexer.py
GEN_PAR=parse/EeyoreParser.py
GEN_TRE=parse/EeyoreTreeWalker.py
GENS=$(GEN_LEX) $(GEN_PAR) $(GEN_TRE)

RUNANTLR=runantlr -o parse/ $(GRAMMAR) && touch $(GENS)

all: genparse

test: genparse
	nosetests

parsetests: genparse
	python scheme.py parse/test.eeyore

genparse: $(GENS)

%.py: $(GRAMMAR)
	$(RUNANTLR)

