#include <stdio.h>

void do_it( bool x )
{
    printf( "bool: %s\n", (x ? "true" : "false") );
}

void do_it_eey_1( int x )
{
    printf( "int: %d\n", x );
}

int main( int argc, char* argv[] )
{
    do_it( (argc > 2) );
    do_it_eey_1( argc );
    do_it_eey_1( argc );
    do_it( (argc > 3) );

    return 0;
}
