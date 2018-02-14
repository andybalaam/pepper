pub mod world;

use self::world::World;

use std::io;


pub fn run(world: World) -> i32 {
    //let mut inp = Vec::new();
    //world.stdin.read_to_end(&mut inp);
    //let stderr = world.stderr;
    //stderr.write(&inp);
    let res = world.stdout.write(b"3\n");
    match res {
        Ok(_) => 0,
        Err(_) => 1,
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
        stdin: FakeReadFile,
        stdout: Vec<u8>,
        stderr: Vec<u8>,
    }


    impl FakeWorld {

        fn new(inp: &[u8]) -> FakeWorld {
            FakeWorld {
                stdin: FakeReadFile::from(inp),
                stdout: Vec::new(),
                stderr: Vec::new(),
            }
        }

        fn world(&mut self) -> World {
            World {
                stdin: &mut self.stdin,
                stdout: &mut self.stdout,
                stderr: &mut self.stderr,
            }
        }

    }


    /// This tests the fake behaviour I have made
    /// so far.  It will be deleted.
    #[test]
    fn running_prints_3_with_no_error() {
        let mut fake = FakeWorld::new(b"");
        assert_eq!(run(fake.world()), 0);
        assert_eq!(fake.stdout, b"3\n");
        assert_eq!(fake.stderr, vec![]);
    }
}
