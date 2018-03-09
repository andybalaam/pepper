#[derive(Clone)]
#[derive(Debug)]
#[derive(PartialEq)]
pub struct FilePos {
    pub filename: String,
    pub line: usize,
    pub column: usize,
}
