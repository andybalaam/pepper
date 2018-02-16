pub mod world;
mod command;

use self::command::Command;
use self::world::World;

use std::io;


pub fn run(world: World) -> i32 {
    let (cmd, args) = command::identify(&world.args);
    match cmd {
        Command::Shell => shell(world, args),
        Command::Echo => echo(world, args),
        _ => cat(world, args),
    }
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


    struct FakeReadFile {
        contents: Vec<u8>,
    }


    impl FakeReadFile {
        fn from(contents: &[u8]) -> FakeReadFile {
            let mut c = Vec::from(contents);
            c.reverse();
            FakeReadFile {
                contents: c,
            }
        }
    }


    impl io::Read for FakeReadFile {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            if buf.len() == 0 {
                Ok(0)
            } else {
                match self.contents.pop() {
                    Some(b) => {
                        buf[0] = b;
                        Ok(1)
                    }
                    None => Ok(0)
                }
            }
        }
    }


    struct FakeWorld {
        args: Vec<String>,
        stdin: FakeReadFile,
        stdout: Vec<u8>,
        stderr: Vec<u8>,
    }


    impl FakeWorld {

        fn new(inp: &[u8], args: &[&str]) -> FakeWorld {
            let mut a: Vec<String> = Vec::new();
            a.push(String::from("exename"));
            for s in args {
                a.push(String::from(*s));
            }
            FakeWorld {
                args: a,
                stdin: FakeReadFile::from(inp),
                stdout: Vec::new(),
                stderr: Vec::new(),
            }
        }

        fn world(&mut self) -> World {
            World {
                args: self.args.clone(),
                stdin: &mut self.stdin,
                stdout: &mut self.stdout,
                stderr: &mut self.stderr,
            }
        }

    }


    /// The following test the fake behaviour I have made
    /// so far.  They will be deleted.
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
