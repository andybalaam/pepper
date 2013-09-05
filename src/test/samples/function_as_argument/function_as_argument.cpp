#include <stdio.h>

void fn1( double a, double b );
void run_it( int unused, void (*tocall)( double, double ) );

void fn1( double a, double b )
{
    printf( "In fn1\n" );
}

void run_it( int unused, void (*tocall)( double, double ) )
{
    printf( "in run_it\n" );
}

int main( int argc, char* argv[] )
{
    run_it( argc, fn1 );

    return 0;
}
