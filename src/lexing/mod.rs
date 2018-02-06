mod token;

use std::str::Chars;

use self::token::Token;


#[derive(Debug)]
struct Lexed<'a> {
    chars: Chars<'a>,
}

impl<'a> Lexed<'a> {
    fn new(chars: Chars<'a>) -> Lexed {
        Lexed {
            chars: chars,
        }
    }
}

impl<'a> Iterator for Lexed<'a> {
    type Item = Token;

    fn next(&mut self) -> Option<Token> {
        match self.chars.next() {
            Some(c) => Some(next_int(c, &mut self.chars)),
            None    => None,
        }
    }
}


fn next_int(first_char: char, chars: &mut Chars) -> Token {
    let mut s = String::new();
    s.push(first_char);
    loop {
        match chars.next() {
            Some(c) if within_int_char(c)  => s.push(c),
            _ => return Token::IntTok(s)
        }
    }
}

fn within_int_char(c: char) -> bool {
    match c {
        '0' ... '9' => true,
        _           => false,
    }
}


fn lex(chars: Chars) -> Lexed {
    Lexed::new(chars)
}


#[cfg(test)]
mod tests {
    use super::*;

    fn assert_lex(input: &str, output: &[Token]) {
        let actual: Vec<Token> = lex(input.chars()).collect();
        let actual: &[Token] = actual.as_ref();
        assert_eq!(actual, output);
    }

    fn intt(chars: &str) -> Token {
        Token::IntTok(String::from(chars))
    }

    #[test]
    fn single_character_int() {
        assert_lex("3", &[intt("3")]);
        assert_lex("9", &[intt("9")]);
    }

    #[test]
    fn multiple_character_int() {
        assert_lex("31", &[intt("31")]);

        let long_int = "01234567891111111111012345678911111111110123456789";
        assert_lex(long_int, &[intt(long_int)]);
    }

    #[test]
    fn several_ints() {
        assert_lex("31 420", &[intt("31"), intt("420")]);
    }
}
