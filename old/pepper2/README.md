# The Pepper Programming Language

Pepper is a ficticious multi-paradigm programming language. Some features:

- Made up and doesn't really exist
- Strong typing and type inference
- Late-binding interfaces - strongly-typed highly generic code
- Python-like string handling
- Compilation to native and also platforms like the JVM and JavaScript
- Your code can run at compile time - metaprogramming is just programming
- Functional purity when you want it
- Memory management through object ownership, not garbage collection
- Full build, link and OS packaging as part of the language
- Code in other languages can be included inline
- Types like "int" and "string" can be swapped at compile time

If you like, think of it as a strongly-typed Lisp with syntax like Java, that
feels like Python and compiles to modern C++.  Written in Haskell.  Inspired by
Ruby.  With some ideas that are a bit like Rust and Node.

## Examples

```pepper2
fn(int, [System]) main =
{:(System sys)
    print(sys.stdout, "Hello, world!");
    return 0;
}
``

`main` is a function returning `int` that takes an argument of type `System`.
Pepper tries to encourage you to use a "parameterise from above" style so
instead of providing a `print` function that prints to a globally-available
standard output, we must pass it `stdout` which is part of the `System`
object.

The integer value returned from `main` will be the status code of the generated
executable, and is mandatory.

Blocks of code and function bodies are the same thing and are built with the
literal syntax shown, starting with a `{` and optional `:(ARGS)`, and ending
with `}`.  This can be used to make named functions like `main` above as well
as anonymous (lambda) functions, and also the bodies of compound statement
blocks like `if` and `for`:

```pepper2
if (x == 2)
{
    for (range(3))
    {:(int i)
        x += i;
    }
}
```

The bodies of the `if` and `for` blocks above are actually anonymous functions
- the `for` block takes and argument which is the loop variable.

## Build

Install all prerequisites (on Debian/Ubuntu):

```bash
make setup
```
Build and run tests:

```bash
make
```

## More info

Web site: http://www.artificialworlds.net/pepper

## Copying

Pepper and all its associated documentation are released under the MIT License.
See the file [COPYING.txt](COPYING.txt) for details.

