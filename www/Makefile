
ASCIIDOC = asciidoc
ASCIIDOC_OPTS = -f layout.conf
#-a toc
SAMPLE2ASCIIDOC = sample2asciidoc/sample2asciidoc

SAMPLES = \
	samples/poohsticks/poohsticks.asciidoc \
	samples/classes/classes.asciidoc \
	samples/if_expression/if_expression.asciidoc \
	samples/closure/closure.asciidoc \
	samples/compile_time_fibonacci/compile_time_fibonacci.asciidoc \
	samples/compile_time_for/compile_time_for.asciidoc \
	samples/deffn/deffn.asciidoc \
	samples/fn_as_value/fn_as_value.asciidoc \
	samples/meta_fn/meta_fn.asciidoc \
	samples/pure_fn/pure_fn.asciidoc \
	samples/template_nontypes/template_nontypes.asciidoc \
	samples/templates/templates.asciidoc \
	samples/implicit_templates/implicit_templates.asciidoc \
	samples/token_pasting/token_pasting.asciidoc \

REAL_SAMPLES = \
	real_samples/samples/hello/hello.asciidoc \
	real_samples/samples/addatcompiletime/addatcompiletime.asciidoc \


HTMLS=html/index.html html/explicitownership.html html/examples.html

all: html

html: $(SAMPLES) $(REAL_SAMPLES) $(HTMLS)

samples/%.asciidoc: \
        $(wildcard $*.eeyore) \
        $(wildcard $*.eeyorelexed) \
        $(wildcard $*.cpp) \
        $(wildcard $*.eeyoreparsetree) \
        $(wildcard $*.output) \
        $(SAMPLE2ASCIIDOC)
	$(SAMPLE2ASCIIDOC) $@

real_samples/%.asciidoc: \
        $(wildcard ../src/test/$*.eeyore) \
        $(wildcard ../src/test/$*.eeyorelexed) \
        $(wildcard ../src/test/$*.cpp) \
        $(wildcard ../src/test/$*.eeyoreparsetree) \
        $(wildcard ../src/test/$*.output) \
        $(SAMPLE2ASCIIDOC)
	$(SAMPLE2ASCIIDOC) $@

html/%.html: asciidoc/%.asciidoc layout.conf layout.css $(SAMPLES)
	mkdir -p html
	$(ASCIIDOC) $(ASCIIDOC_OPTS) --out-file $@ $<

clean:
	rm -f $(HTMLS) $(SAMPLES)

upload: all
	rsync -azii --delete html/ artificialworlds.net:www/eeyore/

report: clean
	make | egrep "^fact|fiction"
