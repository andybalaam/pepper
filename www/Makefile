
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
	samples/inline_cpp/inline_cpp.asciidoc \
	samples/quote_and_replace/quote_and_replace.asciidoc \
	samples/foreign_function/foreign_function.asciidoc \
	samples/web/web.asciidoc \
	samples/type_switch/type_switch.asciidoc \
	samples/reduce/reduce.asciidoc \

REAL_SAMPLES = \
	real_samples/samples/hello/hello.asciidoc \
	real_samples/samples/for_in_range/for_in_range.asciidoc \
	real_samples/samples/addatcompiletime/addatcompiletime.asciidoc \
	real_samples/samples/overload_function/overload_function.asciidoc \
	real_samples/samples/overload_runtime/overload_runtime.asciidoc \
	real_samples/samples/calculated_type/calculated_type.asciidoc \
	real_samples/samples/quoting/quoting.asciidoc \


HTMLS=html/index.html html/explicitownership.html html/examples.html

TEXTS=html/COPYING.txt

all: html txt

html: $(SAMPLES) $(REAL_SAMPLES) $(HTMLS)

txt: $(TEXTS)

# TODO: make this depend on all existing files in the list
#       .eeyore .eeyorelexed .cpp .eeyoreparsetree .output
$(SAMPLES): samples/%.asciidoc: $(SAMPLE2ASCIIDOC) samples/%.eeyore
	$(SAMPLE2ASCIIDOC) $@

# TODO: make this depend on all existing files in the list
#       .eeyore .eeyorelexed .cpp .eeyoreparsetree .output
$(REAL_SAMPLES): real_samples/%.asciidoc: $(SAMPLE2ASCIIDOC) \
		../src/test/%.eeyore
	$(SAMPLE2ASCIIDOC) $@


html/%.html: asciidoc/%.asciidoc layout.conf layout.css $(SAMPLES)
	mkdir -p html
	$(ASCIIDOC) $(ASCIIDOC_OPTS) --out-file $@ $<

html/%.txt: %.txt
	mkdir -p html
	cp $< $@

clean:
	rm -f $(HTMLS) $(TEXTS) $(SAMPLES) $(REAL_SAMPLES)

upload: all
	rsync -azii --delete html/ artificialworlds.net:www/pepper/

report: clean
	make | egrep "^fact|fiction"

view: html
	firefox $(PWD)/html/index.html
