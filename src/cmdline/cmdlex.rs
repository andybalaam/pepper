use std::error::Error;
use std::io;
use lexing;
use lexing::token::Token;
use super::world::World;


pub fn lex(world: World, _args: Vec<String>) -> i32 {
    let tokens = lexing::lex(lexing::char_iter::chars(world.stdin));
    match write_lexed(world.stdout, world.stderr, tokens) {
        Ok(_) => 0,
        Err(e) => {
            world.stderr.write(e.description().as_bytes())
                .expect("Failed to write an error to error stream.");
            2
        }
    }
}


fn write_lexed<I: Iterator<Item=Token>>(
    stdout: &mut io::Write, stderr: &mut io::Write, tokens: I
) -> io::Result<usize> {
    stdout.write(b"tokens = import(language.lexing.tokens);\n[\n")?;
    for t in tokens {
        match t {
            Token::IntTok(i) => {
                stdout.write(b"    tokens.int(\"")?;
                stdout.write(i.as_bytes())?;
                stdout.write(b"\"),\n")?;
            },
            Token::SymbolTok(s) => {
                stdout.write(b"    tokens.symbol(\"")?;
                stdout.write(s.as_bytes())?;
                stdout.write(b"\"),\n")?;
            },
            Token::OperatorTok(o) => {
                stdout.write(b"    tokens.operator(\"")?;
                stdout.write(o.as_bytes())?;
                stdout.write(b"\"),\n")?;
            },
            Token::IoErrorTok(e) => {
                return Err(
                    io::Error::new(
                        io::ErrorKind::Other,
                        format!(
                            "{file}:{line}:{column} IO error: {err}\n",
                            file="-",
                            line=1,
                            column=1,
                            err=e,
                        )
                    )
                )
            },
            Token::BadIntLexErrorTok(actual, correct) => {
                return Err(
                    io::Error::new(
                        io::ErrorKind::Other,
                        format!(
                            "{file}:{line}:{column} Lexing error: \
                            the number \"{actual}\" has underscores in the \
                            wrong place: it should be written \"{correct}\".\n",
                            file="-",
                            line=1,
                            column=1,
                            actual=actual,
                            correct=correct,
                        )
                    )
                )
            },
        }
    }
    stdout.write(b"];\n")?;
    Ok(0)
}


#[cfg(test)]
mod tests {
    use std::convert::From;
    use super::*;
    use super::super::fakeworld::tests::FakeWorld;


    fn assert_vec_eq(left: &Vec<u8>, right: &[u8]) {

        let sleft = String::from_utf8(left.clone());
        let sright = String::from_utf8(Vec::from(&right[..]));

        match (sleft, sright) {
            (Ok(le), Ok(ri)) => assert_eq!(le, ri),
            (Ok(_), Err(e)) => panic!(e),
            (Err(e), _) => panic!(e),
        }
    }


    #[test]
    fn simple_expression_printed_as_code() {
        let mut fake = FakeWorld::new(b"1 + 2\n", &["lex", "-"]);
        let args = vec!(String::from("-"));
        let status = lex(fake.world(), args);
        assert_eq!(status, 0);
        assert_vec_eq(&fake.stderr, b"");
        assert_vec_eq(&fake.stdout, b"\
            tokens = import(language.lexing.tokens);\n\
            [\n    \
                tokens.int(\"1\"),\n    \
                tokens.operator(\"+\"),\n    \
                tokens.int(\"2\"),\n\
            ];\n\
            "
        );
    }
}
