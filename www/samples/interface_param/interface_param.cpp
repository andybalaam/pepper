#include <stdio.h>

void print_all( vector<int>* lst )
{
    for( size_t i = 0; i < lst->size(); ++i )
    {
        printf( "%d\n", (*lst)[i] );
    }
}

int main( int argc, char* argv[] )
{
    vector<int> mylst;
    mylst.push_back( 3 );
    mylst.push_back( 1 );
    mylst.push_back( 4 );
    mylst.push_back( 5 );
    mylst.push_back( 9 );

    print_all( my_lst );

    return 0;
}

