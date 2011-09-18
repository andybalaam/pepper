#include <stdio.h>

void print_this( int num )
{
    int x = num;
    printf( "%d\n", x );
}

int main( int argc, char* argv[] )
{
    printf( "%d\n", 5 );
    print_this( argc );

    return 0;
}
