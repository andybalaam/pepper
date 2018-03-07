use std::error::Error;
use std::iter::FromIterator;

use super::token::Token;
use super::char_iter::CharsError;


pub fn token<I: Iterator<Item=Result<char, CharsError>>>(
    first_char: char, chars: &mut I
) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(Ok(c)) if within_int_char(c) => {
                s.push(c);
            },
            Some(Err(e)) => {
                return Token::IoErrorTok(e.description().to_string())
            },
            _ => {
                return int_tok_if_underscores_valid(s)
            },
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
        '_'         => true,
        _           => false,
    }
}


fn int_tok_if_underscores_valid(s: String) -> Token {
    match validate_underscores(&s) {
        Ok(_) => Token::IntTok(s),
        Err(correct) => Token::BadIntLexErrorTok(s, correct),
    }
}


fn validate_underscores(s: &String) -> Result<usize, String> {
    let mut n = 0;
    for ch in s.chars().rev() {
        n += 1;
        if n % 4 == 0 {
            if is_digit(ch) {
                return Err(fix_underscores(&s))
            }
        } else {
            if !is_digit(ch) {
                return Err(fix_underscores(&s))
            }
        }
    }
    Ok(0)
}

fn fix_underscores(s: &String) -> String {
    let mut ret = String::with_capacity(s.len());
    let mut n: usize = 0;
    for ch in s.chars().rev() {
        match ch {
            '0' ... '9' => {
                n += 1;
                if n % 4 == 0 {
                    ret.push('_');
                    n += 1;
                }
                ret.push(ch);
            },
            _ => {},
        }
    }
    String::from_iter(ret.chars().rev())
}

fn is_digit(ch: char) -> bool {
    match ch {
        '0' ... '9' => true,
        _ => false,
    }
}
