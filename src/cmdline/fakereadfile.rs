#[cfg(test)]
pub mod tests {
    use std::io;

    pub struct FakeReadFile {
        contents: Vec<u8>,
    }


    impl FakeReadFile {
        pub fn from(contents: &[u8]) -> FakeReadFile {
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
}
