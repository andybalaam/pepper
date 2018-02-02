# Pepper3

Pepper3 is a ficticious programming language designed for general programming.
Its main features are:

- Simple, Python-like code, but with strong, expressive typing.
- Compilation and packaging for native and other platforms.
- Metaprogramming and dependent types inspired by Lisp.

I describe it as "ficticious" because at the moment it is a collection of
ideas, with some implementations, but is nowhere near a working language.

## Goals and ideas

Some ideas:

- Strong typing and type inference
- Late-binding interfaces - strongly-typed highly generic code
- Python-like string handling
- Compilation to native and also platforms like the JVM and JavaScript
- Full build, link and OS packaging as part of the language
- Code in other languages can be included inline
- Your code can run at compile time - metaprogramming is just programming
- Functional purity when you want it
- Memory management through object ownership, not garbage collection
- Types like "int" and "string" can be swapped at compile time

## What to read next

- [command_line](doc/command_line.md) - how to run the pepper3 program
- [todo](doc/todo.md) - current plans
- [lexing](doc/lexing.md) - internals of how the lexer works
