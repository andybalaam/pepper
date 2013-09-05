#include <stdio.h>

void (*ret_it( int unused ))( double, double );
void fn1( double a, double b );

void (*ret_it( int unused ))( double, double )
{
    printf( "in ret_it\n" );
    return fn1;
}

void fn1( double a, double b )
{
    printf( "In fn1\n" );
}

int main( int argc, char* argv[] )
{
    ret_it( argc );

    return 0;
}
