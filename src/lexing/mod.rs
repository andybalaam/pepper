mod lex_int;
mod lex_operator;
mod lex_symbol;
mod token;

use std::str::Chars;
use self::token::Token;


/// Lex the supplied characters, providing the
/// results as an Iterator of Tokens.
pub fn lex(chars: Chars) -> Lexed {
    Lexed::new(chars)
}


#[derive(Debug)]
pub struct Lexed<'a> {
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
            Some(c) => Some(lex_token(c, &mut self.chars)),
            None    => None,
        }
    }
}


/// Lex a token starting with `first`,
/// pulling more tokens from `others` as needed.
fn lex_token(first: char, others: &mut Chars) -> Token {
    if lex_int::first_char(first) {
        lex_int::token(first, others)
    } else {
        lex_operator::if_known(lex_symbol::token(first, others))
    }
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

    fn operatort(chars: &str) -> Token {
        Token::OperatorTok(String::from(chars))
    }

    fn symbolt(chars: &str) -> Token {
        Token::SymbolTok(String::from(chars))
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

    #[test]
    fn single_character_symbol() {
        assert_lex("x", &[symbolt("x")]);
        assert_lex("y", &[symbolt("y")]);
    }

    #[test]
    fn multiple_character_symbol() {
        assert_lex("foo", &[symbolt("foo")]);
        assert_lex("bar", &[symbolt("bar")]);
    }

    #[test]
    fn several_symbols() {
        assert_lex("foo bar", &[symbolt("foo"), symbolt("bar")]);
    }

    #[test]
    fn operator() {
        assert_lex("1 + 2", &[intt("1"), operatort("+"), intt("2")]);
    }
}
