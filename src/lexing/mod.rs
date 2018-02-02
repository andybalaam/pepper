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
            Some(c) => {
                let mut s = String::new();
                s.push(c);
                Some(Token::IntTok(s))
            },
            None => None,
        }
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
}
