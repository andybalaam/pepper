pub mod char_iter;
pub mod token;
mod lex_int;
mod lex_operator;
mod lex_symbol;
mod lex_whitespace;

use std::error::Error;
use self::token::Token;
use self::char_iter::CharsError;


pub fn lex<I: Iterator<Item=Result<char, CharsError>>>(chars: I) -> Lexed<I> {
    Lexed::new(chars)
}


pub struct Lexed<I: Iterator<Item=Result<char, CharsError>>> {
    chars: I
}


impl <I: Iterator<Item=Result<char, CharsError>>> Lexed<I> {
    fn new(chars: I) -> Lexed<I> {
        Lexed {
            chars: chars,
        }
    }
}


impl <I: Iterator<Item=Result<char, CharsError>>> Iterator for Lexed<I> {
    type Item = Token;
    fn next(&mut self) -> Option<Token> {
        next_token(&mut self.chars)
    }
}

fn next_token<I: Iterator<Item=Result<char, CharsError>>>(
    chars: &mut I
) -> Option<Token> {
    match chars.next() {
        Some(Ok(c)) => {
            next_token_starting_with(c, chars)
        },
        Some(Err(e)) => {
            Some(Token::IoErrorTok(e.description().to_string()))
        },
        None => {
            None
        },
    }
}

/// Lex a token starting with `first`,
/// pulling more tokens from `others` as needed.
fn next_token_starting_with<I: Iterator<Item=Result<char, CharsError>>>(
        first: char,
        others: &mut I,
) -> Option<Token> {
    if lex_whitespace::is_space(first) {
        next_token(others)
    }
    else
    {
        Some(
            if lex_int::first_char(first) {
                lex_int::token(first, others)
            } else {
                lex_operator::if_known(lex_symbol::token(first, others))
            }
        )
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use std::str::Chars;

    struct IoLikeChars<'a> {
        wrapped: Chars<'a>,
    }

    impl <'a> Iterator for IoLikeChars<'a> {
        type Item = Result<char, CharsError>;

        fn next(&mut self) -> Option<Result<char, CharsError>> {
            match self.wrapped.next() {
                Some(c) => Some(Ok(c)),
                None => None,
            }
        }
    }

    fn assert_lex(input: &str, output: &[Token]) {
        let instr = String::from(input);
        let ioch = IoLikeChars { wrapped: instr.chars() };
        let actual: Vec<Token> = lex(ioch).collect();
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
    fn symbols_separated_by_newline() {
        assert_lex("foo\nbar", &[symbolt("foo"), symbolt("bar")]);
    }

    #[test]
    fn newlines_before_symbol() {
        assert_lex("\n\n\nfoo", &[symbolt("foo")]);
    }

    #[test]
    fn operator() {
        assert_lex("1 + 2", &[intt("1"), operatort("+"), intt("2")]);
    }
}
