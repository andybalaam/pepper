#include <stdio.h>

int reduce( int end );

int reduce( int end )
{
    int acc = 1;
    for( int v = 1; v < end; ++v )
    {
        acc *= v;
    }
    return acc;
}

int main( int argc, char* argv[] )
{
    printf( "%d\n", 12 );
    printf( "%d\n", reduce( argc + 1 ) );

    return 0;
}
