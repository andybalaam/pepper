#include <stdio.h>

int main( int argc, char* argv[] )
{
    for( int n = 0; n < 10; ++n )
    {
        printf( "%d\n", n );
    }
    for( int n = 50; n < 60; n += 2 )
    {
        printf( "%d\n", n );
    }

    return 0;
}
