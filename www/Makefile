
ASCIIDOC = asciidoc
ASCIIDOC_OPTS = -f layout.conf
#-a toc
SAMPLE2ASCIIDOC = sample2asciidoc/sample2asciidoc

SAMPLES = samples/hello/hello.asciidoc samples/poohsticks/poohsticks.asciidoc  samples/addatcompiletime/addatcompiletime.asciidoc

HTMLS=html/index.html html/explicitownership.html html/examples.html

all: html

html: $(SAMPLES) $(HTMLS)

samples/%.asciidoc: \
        $(wildcard $*.eeyore) \
        $(wildcard $*.cpp) \
        $(wildcard $*.parsetree) \
        $(wildcard $*.output) \
        $(SAMPLE2ASCIIDOC)
	$(SAMPLE2ASCIIDOC) $@

html/%.html: asciidoc/%.asciidoc layout.conf layout.css $(SAMPLES)
	$(ASCIIDOC) $(ASCIIDOC_OPTS) --out-file $@ $<

clean:
	rm -f $(HTMLS) $(SAMPLES)

upload: all
	rsync -azii --delete html/ artificialworlds.net:www/eeyore/

