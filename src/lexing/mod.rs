pub mod char_iter;
pub mod filepos;
pub mod token;
mod lex_int;
mod lex_operator;
mod lex_symbol;
mod lex_whitespace;

use std::error::Error;
use self::token::Token;
use self::char_iter::CharsError;
use self::filepos::FilePos;


pub fn lex<I: Iterator<Item=Result<char, CharsError>>>(chars: I) -> Lexed<I> {
    Lexed::new(chars)
}

struct CharsWithPos<I: Iterator<Item=Result<char, CharsError>>> {
    chars: I,
    file_pos: FilePos,
}

impl <I: Iterator<Item=Result<char, CharsError>>> Iterator
        for CharsWithPos<I> {
    type Item = Result<char, CharsError>;
    fn next(&mut self) -> Option<Result<char, CharsError>> {
        match self.chars.next() {
            Some(Ok(c)) => {
                let ret = Some(Ok(c));
                if c == '\n' {
                    self.file_pos.line += 1;
                    self.file_pos.column = 1;
                } else {
                    self.file_pos.column += 1;
                }
                ret
            },
            Some(Err(e)) => Some(Err(e)),
            None => None,
        }
    }
}

pub struct Lexed<I: Iterator<Item=Result<char, CharsError>>> {
    chars: CharsWithPos<I>,
}


impl <I: Iterator<Item=Result<char, CharsError>>> Lexed<I> {
    fn new(chars: I) -> Lexed<I> {
        Lexed {
            chars: CharsWithPos {
                chars: chars,
                file_pos: FilePos {
                    filename: String::new(),
                    line: 1,
                    column: 1,
                },
            }
        }
    }

    fn next_token(&mut self) -> Option<Token> {
        let fp = self.chars.file_pos.clone();
        match self.chars.next() {
            Some(Ok(c)) => {
                self.next_token_starting_with(c, fp)
            },
            Some(Err(e)) => {
                Some(
                    Token::IoErrorTok(
                        e.description().to_string(),
                        fp,
                    )
                )
            },
            None => {
                None
            },
        }
    }

    /// Lex a token starting with `first`,
    /// pulling more tokens from `others` as needed.
    fn next_token_starting_with(
        &mut self,
        first: char,
        file_pos: FilePos,
    ) -> Option<Token> {
        if lex_whitespace::is_space(first) {
            self.next_token()
        }
        else
        {
            Some(
                if lex_int::first_char(first) {
                    lex_int::token(
                        first,
                        &mut self.chars,
                        file_pos,
                    )
                } else {
                    lex_operator::if_known(
                        lex_symbol::token(
                            first,
                            &mut self.chars,
                            file_pos,
                        )
                    )
                }
            )
        }
    }

}


impl <I: Iterator<Item=Result<char, CharsError>>> Iterator for Lexed<I> {
    type Item = Token;
    fn next(&mut self) -> Option<Token> {
        self.next_token()
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

    fn badintt(
        chars: &str,
        correct_chars: &str,
        line: usize,
        column: usize,
    ) -> Token {
        Token::BadIntLexErrorTok(
            String::from(chars),
            String::from(correct_chars),
            FilePos { filename: String::new(), line: line, column: column },
        )
    }

    #[test]
    fn single_character_int() {
        assert_lex("3", &[intt("3")]);
        assert_lex("9", &[intt("9")]);
    }

    #[test]
    fn int_starting_with_underscore_is_actually_a_symbol() {
        assert_lex("_3_4", &[symbolt("_3_4")]);
    }

    #[test]
    fn int_with_wrong_underscores_is_an_error() {
        assert_lex("3_1", &[badintt("3_1", "31", 1, 1)]);
        assert_lex("\n  123_1", &[badintt("123_1", "1_231", 2, 3)]);
        assert_lex("59_87123_1", &[badintt("59_87123_1", "59_871_231", 1, 1)]);
    }

    #[test]
    fn multiple_character_int() {
        assert_lex("31", &[intt("31")]);

        let long_int = "21_345_789_111_111_101_345_789_111_111_101_345_789";
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
    fn operator_plus() {
        assert_lex("1 + 2", &[intt("1"), operatort("+"), intt("2")]);
    }
}
