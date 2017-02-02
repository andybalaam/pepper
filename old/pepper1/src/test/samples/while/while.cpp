#include <stdio.h>

int main( int argc, char* argv[] )
{
    while( false )
    {
        printf( "Don't print this.\n" );
    }
    int x = 10;
    while( x > 5 )
    {
        printf( "x=%d\n", x );
        x -= 1;
    }
    printf( "End\n" );

    return 0;
}
