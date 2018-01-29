mod token;
use self::token::Token;

fn lex(chars: &str) -> Token {
    Token::IntTok(String::from(chars))
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn single_character_int() {
        assert_eq!(lex("3"), Token::IntTok(String::from("3")));
    }
}
