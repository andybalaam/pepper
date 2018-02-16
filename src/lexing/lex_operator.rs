use super::token::Token;


/// If the supplied symbol is a known operator,
/// return an operator token.  Otherwise, return
/// the supplied token.
pub fn if_known(symbol: Token) -> Token {
    if let Token::SymbolTok(ref name) = symbol {
        if known_name(&name) {
            return Token::OperatorTok(name.clone())
        }
    }
    symbol
}


fn known_name(name: &String) -> bool {
    name == "+"
}
