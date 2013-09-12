#include <stdio.h>

void do_something( int a, double b );
void (*get_fn( int unused ))( int, double );

void do_something( int a, double b )
{
    printf( "in do_something\n" );
}

void (*get_fn( int unused ))( int, double )
{
    printf( "in get_fn\n" );
    return do_something;
}

int main( int argc, char* argv[] )
{
    void (*got_fn)( int, double ) = get_fn( argc );
    got_fn( argc, 2.0 );

    return 0;
}
