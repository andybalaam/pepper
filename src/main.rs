mod cmdline;
mod lexing;  // Needed to ensure tests run

use cmdline::world::World;

//use std::env;
use std::io;
use std::process;


fn main() {
    let world = World {
        //args: env::args(),
        stdin:  &mut io::stdin(),
        stdout: &mut io::stdout(),
        stderr: &mut io::stderr(),
    };

    process::exit(cmdline::run(world));
}
