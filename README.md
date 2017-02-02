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
int main(System sys)
{
    print(sys.stdout, "Hello, world!");
}
```

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
See the file COPYING.txt for details.

