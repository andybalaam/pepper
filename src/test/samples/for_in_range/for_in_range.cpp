#include <stdio.h>

int main( int argc, char* argv[] )
{
    for( int n = 0; n < argc; ++n )
    {
        printf( "%d\n", n );
    }
    for( int n = 3; n < argc; n += 2 )
    {
        printf( "%d\n", n );
    }

    return 0;
}
