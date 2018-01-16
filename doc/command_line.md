# Running Pepper3

Everything you do with Pepper3 is done by using the `pepper3` executable.

## Running a program

To run a program type `pepper3 run`:

```bash
$ #(Not implemented) pepper3 run myprogram.pepper3
# Hello from my program!
```

Or, because `run` is the default, you can miss it out:

```bash
$ #(Not implemented) pepper3 myprogram.pepper3
# Hello from my program!
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
