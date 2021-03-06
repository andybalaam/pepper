# Copyright (C) 2010-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


ASCIIDOC = asciidoc
ASCIIDOC_CONF = xhtml11-modified.conf
ASCIIDOC_OPTS = \
	-a stylesdir=/etc/asciidoc/stylesheets \
	-a scriptsdir=/etc/asciidoc/javascripts \
	-a stylesheet=${PWD}/layout.css \
	-a max-width=50em \
	-a toc=true

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
	samples/interface_param/interface_param.asciidoc \
	samples/debuggable_version/debuggable_version.asciidoc \

REAL_SAMPLES = \
	real_samples/samples/hello/hello.asciidoc \
	real_samples/samples/for_in_range/for_in_range.asciidoc \
	real_samples/samples/addatcompiletime/addatcompiletime.asciidoc \
	real_samples/samples/overload_function/overload_function.asciidoc \
	real_samples/samples/overload_runtime/overload_runtime.asciidoc \
	real_samples/samples/calculated_type/calculated_type.asciidoc \
	real_samples/samples/quoting/quoting.asciidoc \
	real_samples/samples/interfaces/interfaces.asciidoc \


HTMLS = \
	html/index.html \
	html/explicitownership.html \
	html/examples.html \
	html/choosinglicense.html \


TEXTS=html/COPYING.txt

all: html txt

html: $(SAMPLES) $(REAL_SAMPLES) $(HTMLS)

txt: $(TEXTS)

# TODO: make this depend on all existing files in the list
#       .pepper .pepperlexed .cpp .pepperparsetree .output
$(SAMPLES): samples/%.asciidoc: $(SAMPLE2ASCIIDOC) samples/%.pepper
	$(SAMPLE2ASCIIDOC) $@

# TODO: make this depend on all existing files in the list
#       .pepper .pepperlexed .cpp .pepperparsetree .output
$(REAL_SAMPLES): real_samples/%.asciidoc: $(SAMPLE2ASCIIDOC) \
		../src/test/%.pepper
	$(SAMPLE2ASCIIDOC) $@

$(ASCIIDOC_CONF): xhtml11-modifications.patch
	patch -o $(ASCIIDOC_CONF) /etc/asciidoc/xhtml11.conf xhtml11-modifications.patch

html/%.html: asciidoc/%.asciidoc layout.css $(ASCIIDOC_CONF) $(SAMPLES)
	mkdir -p html
	$(ASCIIDOC) -f $(ASCIIDOC_CONF) $(ASCIIDOC_OPTS) --out-file $@ $<

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
