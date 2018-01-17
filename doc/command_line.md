# Running Pepper3

Everything you do with Pepper3 is done by using the `pepper3` executable.

The most important subcommands you can type are:

```
pepper3 run FILENAME
pepper3 compile FILENAME
pepper3 eval EXPRESSION
```

These are explained in the following sections.

If you want to start an interactive session, simply type:

```
pepper3
```

## Running a program

To run a program type `pepper3 run`:

```bash
#(Not implemented) $ pepper3 run myprogram.pepper3
Hello from my program!
```

Or, because `run` is the default, you can miss it out:

```bash
#(Not implemented) $ pepper3 myprogram.pepper3
Hello from my program!
```

## Evaluating programs on the command line

You can evaluate a snippet of code using `pepper3 eval`:

```bash
$ pepper3 eval "x = 3; x"
3
```

To provide a program to run on stdin, give "-" as the file name.

```bash
$ echo "1 + 2" | pepper3 run -
3
```

## Compiling a program

```bash
#(Not implemented) $ pepper3 compile myprogram.pepper && ./myprogram
Hello from my program!
```

## Running multiple commands

You can run multiple Pepper3 subcommands in the same environment by joining
them together with `--`.  For example, to evaluate a command in the context
of come code in a file, you can `run` the file, then `eval` the command:

```bash
$ cat snippets/set_x_to_4.pepper3
x = 4
```

```bash
$ pepper3 run snippets/set_x_to_4.pepper3 -- eval "x - 1"
3
```
