from tools_examples import *

@skip
@istest
def function_call():
    assert_example(
        "foo( 3 )",
        "symbol:foo ( int:3 )",
        "PepFunctionCall( PepSymbol('foo'), [PepInt('3')] )",
        "PepFunctionCall( PepSymbol('foo'), [PepInt('3')] )",
        "PepFunctionCall( PepSymbol('foo'), [PepInt('3')] )",
        None,
        None,
    )

@skip
@istest
def for_loop():
    assert_example(
        """
            for( range(3) )
            { |i|
                print( i )
            }
        """,
        """
            symbol:for
            (
                symbol:range ( int:3 )
            )
            {
                | symbol:i |
                symbol:print ( symbol:i )
            }
        """,
        """
            PepFunctionCall( PepSymbol('for'), [
                PepFunctionCall( PepSymbol('range'), [PepInt('3')] )
            ]
            PepCodeBlock(
                [PepSymbol('i')],
                [
                    PepFunctionCall( PepSymbol('print'), [PepSymbol('i')] )
                ]
            )
        """,
        """
            PepForBlock( PepRange(3) )
            PepCodeBlock(
                [PepSymbol('i')],
                [
                    PepPrint( [PepSymbol('i')] )
                ]
            )
        """,
        """
            PepFor(
                PepRange( 3 ),
                PepCode(
                    [PepSymbol('i')],
                    [
                        PepPrint( [PepSymbol('i')] )
                    ]
                )
            )
        """,
        """
            #include <cstdio>

            int main( int argv, char*[] argv )
            {
                for ( int i = 0; i < 3; ++i )
                {
                    printf( "%d\n", i );
                }
            }
        """,
        """
            0
            1
            2
        """,
    )


@skip
@istest
def if_elif_else():
    assert_example(
        """
            if( x == 3 )
            {
                print( 3 )
            }
            elif( x == 2 )
            {
                print( 2 )
            }
            else
            {
                print( 0 )
            }
        """,
        """
            symbol:if
            ( symbol:x == int:3 )
            { symbol:print ( int:3 ) }
            symbol:elif
            ( symbol:x == int:2 )
            { symbol:print ( int:2 ) }
            symbol:else
            { symbol:print ( int:2 ) }
        """,
        """
            PepFunctionCall(
                PepSymbol('if'),
                [ PepEquals( PepSymbol('x'), PepInt('3') ) ]
            )
            PepCodeBlock(
                [],
                [PepFunctionCall( PepSymbol('print'), [PepInt(3)]]
            )
            PepFunctionCall(
                PepSymbol('elif'),
                [ PepEquals( PepSymbol('x'), PepInt('2') ) ]
            )
            PepCodeBlock(
                [],
                [PepFunctionCall( PepSymbol('print'), [PepInt(2)]]
            )
            PepSymbol('else')
            PepCodeBlock(
                [],
                [PepFunctionCall( PepSymbol('print'), [PepInt(0)]]
            )
        """,
        """
            PepIfBlock( PepEquals( PepSymbol('x'), PepInt('3') ) )
            PepCodeBlock( [], [PepPrint(PepInt(3))] )
            PepElifBlock( PepEquals( PepSymbol('x'), PepInt('2') ) )
            PepCodeBlock( [], [PepPrint(PepInt(2))] )
            PepElseBlock()
            PepCodeBlock( [], [PepPrint(PepInt(0))] )
        """,
        """
            PepIf(
                [
                    PepEquals( PepSymbol('x'), PepInt('3') ),
                    PepCode( [], [PepPrint(PepInt(3))] ),
                ],
                [
                    PepEquals( PepSymbol('x'), PepInt('2') ),
                    PepCode( [], [PepPrint(PepInt(2))] ),
                ],
                PepCode( [], [PepPrint(PepInt(0))] )
            )
        """,
        None,
        None
    )

