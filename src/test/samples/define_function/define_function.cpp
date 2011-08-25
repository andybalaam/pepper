#include <stdio.h>

void print_this( int num )
{
    printf( "%d\n", num );
}

int main( int argc, char* argv[] )
{
    printf( "%d\n", 5 );
    print_this( argc );

    return 0;
}
