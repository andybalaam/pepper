# Lexing in Pepper3

This page documents the way the lexer in Pepper3 works.  This information
will not be needed to use Pepper3 when it exists - it's part of the internals
of the language, breaking text input into chunks that make sense to the
compiler.

To see how the lexer treats some code, you can invoke it like this:

```bash
# (Not implemented) $ echo "1 + 2" | pepper3 lex -
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

(Future, not done yet)  If you are customising Pepper3's lexing process with
your own code, you can test it like this:

```bash
$ echo "1 :-) 2" | pepper3 run mylexing.pepper3 -- lex -
3
```
