
all: test

setup:
	sudo apt install python3
	echo "Now install rust as described at rust-lang.org"

build:
	cargo build

test: build
	cargo test
	./tests/test-doc/test-doc
