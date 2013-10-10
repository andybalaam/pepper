#include <cstdio>

struct make_plusn_pep_f_toreturn
{
private:
    int n;
public:
    make_plusn_pep_f_toreturn( int n )
    : n( n )
    {
    }

    int operator()( int i )
    {
        return n + i;
    }
};

make_plusn_pep_f_toreturn make_plusn( int n )
{
    return make_plusn_pep_f_toreturn( n );
}

int main( int argc, char* argv[] )
{
    make_plusn_pep_f_toreturn plus6 = make_plusn( 6 );
    printf( "%d\n", plus6( 5 ) );

    return 0;
}

