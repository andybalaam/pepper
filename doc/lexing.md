# Lexing in Pepper3

This page documents the way the lexer in Pepper3 works.  This information
will not be needed to use Pepper3 when it exists - it's part of the internals
of the language, breaking text input into chunks that make sense to the
compiler.

To see how the lexer treats some code, you can invoke it like this:

```bash
$ echo "1 + 2" | pepper3 lex -
tokens = import(language.lexing.tokens);
[
    tokens.int("1"),
    tokens.operator("+"),
    tokens.int("2"),
];
```

Notice that the code above is actually Pepper3 code, so you can read in these
tokens again by evaluating the output with `pepper3 run`.  Also, if you want
to make lexing tokens yourself in your own code, the above is a good starting
point for figuring out how to do it.

## Numbers

Pepper3's lexer recognises two types of numeric literal: integers and
floating-point numbers.  While the code is running, these could be put into
variables of various types (e.g. a 32-bit IEEE floating point, or an
arbitrary-precision integer class) but the lexer only looks for literals - we
will find out later in the compilation (or running) process whether they are
suitable to put into the type of variable being used.

### Integers

Integers start with a digit (0-9) and contain only digits and underscores.

Underscores must be used as thousand separators in integers.

```bash
$ echo "10_000" | pepper3 lex -
tokens = import(language.lexing.tokens);
[
    tokens.int("10_000"),
];
```

```bash
$ echo "a 1000_0" | pepper3 lex -
tokens = import(language.lexing.tokens);
[
    tokens.symbol("a"),
-:1:3 Lexing error: the number "1000_0" has underscores in the wrong place: it should be written "10_000".
[exited with status code 2]
```

## Symbols

Symbols are words and operators that are used as names for things like
variables and functions.  They start with a character that is not special
in any other way, i.e. anything except a quote, bracket or digit.

```bash
$ echo "foo bar" | pepper3 lex -
tokens = import(language.lexing.tokens);
[
    tokens.symbol("foo"),
    tokens.symbol("bar"),
];
```

### Operators

Operators are symbols that have been added to a special list meaning they
are used as "infix" operators - i.e. they are functions taking two arguments,
and those arguments are written before and after the symbol, instead of
using the normal function call syntax.

For example, "+" is an operator:

```bash
$ echo "3 + 5" | pepper3 lex -
tokens = import(language.lexing.tokens);
[
    tokens.int("3"),
    tokens.operator("+"),
    tokens.int("5"),
];
```

Some programming languages restrict infix operators to a specific list of
known symbols, and some require special syntax to use a normal symbol as an
infix operator (e.g. Haskell's back-tick syntax).  Pepper3 allows any symbol
to be an operator, and it handles this by recognising them during the lexing
phase.

To treat an operator as a word, enclose it in brackets like this:

```pepper3shell
# (Not implemented) >>> (+)(3, 5)
8
```

## Custom lexing

(Future, not done yet) Any program can customise how Pepper3 lexes its code.
To do this you need to write code modifying the lexing setup, then call the
special `lang.reparse` function to tell Pepper3 to use what you have changed.
For example:

```pepper3
import(lang)
import(lang.lexer)

lang.lexer.operators += ":-)"  # Add a new operator

lang.reparse()  # Tell Pepper3 to evaluate the following code
                # after applying the change above

:-) = {:(int a, int b)  # Define a function called ":-)"
    a*2 + b
}

x = 3 :-) 4   # Now we can use it!
```

If you import a file that customises lexing, you must call `lang.reparse`
before you use it:

```pepper3
import(lang)
import_inline(mylexing)
lang.reparse()  # You must include this, or the next line is an error
x = 3 :-) 4
```

In the above example, mylexing.pepper3 could look like this:

```pepper3
import(lang)
import(lang.lexer)
lang.lexer.operators += ":-)"
lang.reparse()
:-) = {:(int a, int b)  # Define a function called ":-)"
    a*2 + b
}
```

Note that it is not enough for mylexing.pepper3 to include a call to
`lang.reparse` - the file that includes it must do so too.

`lang.reparse` is a special function that tells the lexer and parser to stop
working on this file, and continue after the previous code has been run.
Because of this special behaviour, it can't be called from within some other
function - it must be written at the top level of the file's code as shown
in these examples.

If you are customising Pepper3's lexing process with your own code, you can
test it like this:

```bash
$ echo "1 :-) 2" | pepper3 run mylexing.pepper3 -- lex -
3
```
