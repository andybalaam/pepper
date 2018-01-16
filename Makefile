
all: build test

setup:
	sudo apt install python3
	echo "Now install rust as described at rust-lang.org"

build:
	cargo build

test:
	./tests/test-doc/test-doc
