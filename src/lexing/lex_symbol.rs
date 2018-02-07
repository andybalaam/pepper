use std::str::Chars;
use super::token::Token;


pub fn first_char(first_char: char) -> bool {
    true
}


pub fn token(first_char: char, chars: &mut Chars) -> Token {
    let mut s = String::new();
    s.push(first_char);
    Token::SymbolTok(s)
}
