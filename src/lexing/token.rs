use super::filepos::FilePos;


#[derive(Debug)]
#[derive(PartialEq)]
pub enum Token {
    IntTok(String),
    SymbolTok(String),
    OperatorTok(String),
    IoErrorTok(String, FilePos),
    BadIntLexErrorTok(String, String, FilePos),
}
