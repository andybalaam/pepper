# Imports in Pepper3

Pepper3 code is organised into separate files.  To use the code from one file
inside another, you can import it.

The simplest way to import code is to use the `import` function:

```pepper3
math = import(math)
math.sqrt(64)
===>
8
```

Once you have `import`ed the `math` file, you can use the names defined
inside it as shown, by typing `math.` followed by the name, for example
`math.sqrt`.

Sometimes you want the names defined in a file to be visible as if they were
defined inside this file.  To achieve that, use `import_inline`:

```pepper3
import_inline(math)
sqrt(16)
===>
4
```

Note: you should be careful with this: it can make it hard to read your code
and see where names come from.

If you only want some of the names from a file, provide the names you want
to `import`:

```pepper3
math = import(math, [sqrt])
math.sqrt(4)
===>
2
```

Or similarly for `import_inline`:

```pepper3
import_inline(math, [sqrt])
sqrt(9)
===>
3
```

If you want to use a different name to refer to a file, simply call it something different:

```pepper3
m = import(math)
m.sqrt(25)
===>
5
```
