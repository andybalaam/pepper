use std::error::Error;
use super::char_iter::CharsError;
use super::filepos::FilePos;
use super::token::Token;


pub fn token<I: Iterator<Item=Result<char, CharsError>>>(
    first_char: char,
    chars: &mut I,
    file_pos: FilePos,
) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(Ok(c)) if within_symbol_char(c) => {
                s.push(c);
            },
            Some(Err(e)) => {
                return Token::IoErrorTok(
                    e.description().to_string(),
                    file_pos,
                )
            },
            _ => {
                return Token::SymbolTok(s)
            },
        }
    }
}


fn within_symbol_char(c: char) -> bool {
    match c {
        'a' ... 'z' => true,
        'A' ... 'Z' => true,
        '0' ... '9' => true,
        '_' => true,
        _ => false,
    }
}
