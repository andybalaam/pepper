use std::str::Chars;
use super::token::Token;


pub fn token(first_char: char, chars: &mut Chars) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(c) if within_symbol_char(c) => s.push(c),
            _ => return Token::SymbolTok(s)
        }
    }
}


fn within_symbol_char(c: char) -> bool {
    c != ' '
}
