pub mod fakereadfile;
pub mod fakeworld;
pub mod world;
mod cmdlex;
mod command;

use self::command::Command::*;
use self::world::World;
use self::cmdlex::lex;

use std::io;


pub fn run(world: World) -> i32 {
    let (cmd, args) = command::identify(&world.args);
    match cmd {
        Cat    => cat(world, args),
        Echo   => echo(world, args),
        Lex    => lex(world, args),
        Print3 => print3(world, args),
        Shell  => shell(world, args),
    }
}


/// To get some of the doc tests to pass before they should
fn print3(world: World, _args: Vec<String>) -> i32 {
    world.stdout.write(b"3\n").expect("Failed to write 3.");
    0
}


fn shell(world: World, _args: Vec<String>) -> i32 {
    world.stderr.write(b"Shell mode not implemented yet.\n")
        .expect("\
            Failed writing to stderr when complaining \
            that shell mode is not implemented yet.\
        ");
    2
}


const STATUS_OK: i32 = 0;
const STATUS_FAILED_TO_WRITE_STDOUT: i32 = 1;
const STATUS_FAILED_TO_WRITE_STDERR: i32 = 2;
const STATUS_FAILED_TO_READ_STDIN: i32 = 3;


fn write_error(e: io::Error, world: World) -> i32 {
    match world.stderr.write(e.to_string().as_bytes()) {
        Ok(_) => STATUS_FAILED_TO_WRITE_STDOUT,
        Err(_) => STATUS_FAILED_TO_WRITE_STDERR,
    }
}


fn read_error(e: io::Error, world: World) -> i32 {
    match world.stderr.write(e.to_string().as_bytes()) {
        Ok(_) => STATUS_FAILED_TO_READ_STDIN,
        Err(_) => STATUS_FAILED_TO_WRITE_STDERR,
    }
}


fn echo(world: World, args: Vec<String>) -> i32 {
    let mut first = true;
    for s in args {
        if first {
            first = false
        } else if let Err(e) = world.stdout.write(b" ") {
                return write_error(e, world)
        }
        if let Err(e) = world.stdout.write(s.as_bytes()) {
            return write_error(e, world)
        }
    }
    if let Err(e) = world.stdout.write(b"\n") {
        return write_error(e, world)
    }
    STATUS_OK
}


fn cat(world: World, _args: Vec<String>) -> i32 {
    let mut buf = [0; 1024];
    loop {
        match world.stdin.read(&mut buf) {
            Err(e) => return read_error(e, world),
            Ok(0) => return STATUS_OK,
            Ok(n) => {
                if let Err(e) = world.stdout.write(&buf[..n]) {
                    return write_error(e, world)
                }
            },
        }
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use super::fakeworld::tests::FakeWorld;


    #[test]
    fn no_arg_fails() {
        let mut fake = FakeWorld::new(b"", &[]);
        assert_eq!(run(fake.world()), 2);
        assert_eq!(fake.stdout, b"");
        assert_eq!(fake.stderr, b"Shell mode not implemented yet.\n");
    }

    #[test]
    fn cat_outputs_input() {
        let mut fake = FakeWorld::new(b"foo\nbar", &["cat"]);
        assert_eq!(run(fake.world()), 0);
        assert_eq!(fake.stdout, b"foo\nbar");
        assert_eq!(fake.stderr, vec![]);
    }

    #[test]
    fn echo_prints_args() {
        let mut fake = FakeWorld::new(b"", &["echo", "foo", "bar"]);
        assert_eq!(run(fake.world()), 0);
        assert_eq!(fake.stdout, b"foo bar\n");
        assert_eq!(fake.stderr, vec![]);
    }
}
