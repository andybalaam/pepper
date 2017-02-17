all: test

test: format
	./buildtools/test

format:
	@echo "TODO: pep8 check and formatting"

setup:
	sudo apt-get install python3
