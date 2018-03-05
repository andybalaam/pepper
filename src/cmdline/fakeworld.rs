#[cfg(test)]
pub mod tests {
    use super::super::fakereadfile::tests::FakeReadFile;
    use super::super::world::World;


    pub struct FakeWorld {
        pub args: Vec<String>,
        pub stdin: FakeReadFile,
        pub stdout: Vec<u8>,
        pub stderr: Vec<u8>,
    }


    impl FakeWorld {

        pub fn new(inp: &[u8], args: &[&str]) -> FakeWorld {
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

        pub fn world(&mut self) -> World {
            World {
                args: self.args.clone(),
                stdin: &mut self.stdin,
                stdout: &mut self.stdout,
                stderr: &mut self.stderr,
            }
        }

    }
}
