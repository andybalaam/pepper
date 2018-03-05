use std::error::Error;
use super::token::Token;
use super::char_iter::CharsError;


pub fn token<I: Iterator<Item=Result<char, CharsError>>>(
    first_char: char, chars: &mut I
) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(Ok(c)) if within_symbol_char(c) => {
                s.push(c);
            },
            Some(Err(e)) => {
                return Token::IoErrorTok(e.description().to_string())
            },
            _ => {
                return Token::SymbolTok(s)
            },
        }
    }
}


fn within_symbol_char(c: char) -> bool {
    c != ' '
}
