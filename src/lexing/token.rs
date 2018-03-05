#[derive(Debug)]
#[derive(PartialEq)]
pub enum Token {
    IntTok(String),
    SymbolTok(String),
    OperatorTok(String),
    IoErrorTok(String),
}
