# Dialects of Pepper2

To bootstrap Pepper2, we have multiple dialects of it.

## AST manually defined in Python

We can write Pepper2 in Python by manually constructing the AST objects that
are usually created by the parser.

This allows us to write Pepper2 code without having a lexer or parser yet.

For example, this Pepper snippet:

```pepper2
String x = "Hello";
```

would be written like this in astPepper2:

```python3
from astPepper2 import *
astDefinition(astSymbol("String"), astSymbol("x"), astString("Hello"))
```

## Pepper2Like Python

We keep this to a minimum, but when we must write actual Python code, we
write it in a dialect called Pepper2Like, which is a set of Python libraries
designed to allow you to make your Python code look and work as much like
Pepper2 as possible.

For example to define a function:

```python3
def double(x):
    return x * 2
double = pl_def(double, float, float)  # adds type checking
```

The Pepper2 equivalent would be:

```pepper2
fn(float) double = {:(float x) x*2}
```

or to write a test:

```python3
def check_maths_works:
    pl_assert_equals(2 + 2, 4)
pl_test("Check maths works", check_maths_works)
```

The Pepper2 equivalent would be:

```pepper2
test(
    "Check maths works",
    {
        assert({{{2 + 2 == 4}}})
    }
);
```
