# Examples

## The pepper parser in Pepper

```pepper2
import(
    lexing.
        [ anyCharExcept
        , char
        , digitfixed_num
        , Lexer
        , or
        , sequence
        , Token
        , zeroOrMore
        ]
);

// Defined in prologue:
Type Char = Utf8Char;

// Defined in lexing:
Type LexerReturn = either(iter(Token), LexingFailed);
Type Lexer = fn(LexerReturn, iter(Char));
Lexer or =
    {:(Lexer... lexers)
        // This is wrong - should return a Lexer, not something lexed
        auto impl = {:(Lexer... lexers, LexingFailed lastFailure)
            case(head(lexers))
            (
                {:(Nothing _) lastFailure},
                {:(Just(iter(Token)) tokens) tokens},
                {:(Just(LexingFailed) failure) or(tail(lexers))}
            )
        };
        impl(lexers, emptyOr)
    }

Type natural = type_where({:(int i) i >= 1});

Lexer fixed_num =
    {:(natural how_many, Lexer item)
        int next = how_many - 1;
        case(next)
        ( {:(natural n) sequence(item, n)}
        , {:(int i)     item}
        )
    }

// Here

Lexer escapedUnicode = sequence(char('\\'), char('u'), fixed_num(4, digit));
Lexer escapedQuote = sequence(char('\\'), char('"'));

Lexer inString =
    or(
        escapedUnicode,
        escapedQuote,
        anyCharExcept('"\\')
    );

Lexer string = sequence(
    StringToken, char('"'), zeroOrMore(inString), char('"'));


// Tests

auto _unpack =
    {:(either(iter(Token), LexingFailed) tokens)
        case(tokens)
        ( {:(iter(Token) it) array(tokens)}
        , {:(any failure) failure}
        )
    }

test(
    "Empty string lexes",
    {
        assert({{{ _unpack(string('""')) == [StringToken("")] }}})
    }
);
```

