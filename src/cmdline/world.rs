use std::io;


pub struct World<'a> {
    pub stdin: &'a mut io::Read,
    pub stdout: &'a mut io::Write,
    pub stderr: &'a mut io::Write,
}
