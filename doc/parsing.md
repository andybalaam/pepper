# Parsing in Pepper3

This page documents the way the parser in Pepper3 works.  This information
will not be needed to use Pepper3 when it exists - it's part of the internals
of the language, building tokens that come from the [lexer](lexing.md) into
tree structures representing statements and expressions.

To see how the parser treats some code, you can invoke it like this:

```bash
#(Not implemented) $ echo "int x = 1; x + 2;" | pepper3 parse -
trees = import(language.parsing.trees);
[
    trees.assign("x", trees.int("1")),
    trees.function_call("+", [trees.symbol("x"), trees.int("2"),]),
];
```

Notice that the code above is actually Pepper3 code, so you can read in these
trees again by evaluating the output with `pepper3 run`.  Also, if you want
to make parse trees yourself in your own code, the above is a good starting
point for figuring out how to do it.

## Values

## Function calls

## Operator calls are function calls

## Function definitions
