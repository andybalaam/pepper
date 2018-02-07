use std::str::Chars;
use super::token::Token;


pub fn token(first_char: char, chars: &mut Chars) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(c) if within_int_char(c) => s.push(c),
            _ => return Token::IntTok(s)
        }
    }
}


pub fn first_char(c: char) -> bool {
    match c {
        '0' ... '9' => true,
        _           => false,
    }
}


fn within_int_char(c: char) -> bool {
    match c {
        '0' ... '9' => true,
        _           => false,
    }
}
