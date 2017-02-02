#include <stdio.h>

struct A
{
};

void do_foo( int a, A& f );
void A_pep_c_pep_foo( A& self, int a );
void A_pep_c_pep___init__( A& self, int a );

void do_foo( int a, A& f )
{
    printf( "do_foo\n" );
    A_pep_c_pep_foo( f, a );
}

void A_pep_c_pep_foo( A& self, int a )
{
    printf( "A.foo\n" );
}

void A_pep_c_pep___init__( A& self, int a )
{
}

int main( int argc, char* argv[] )
{
    A ainst; A_pep_c_pep___init__( ainst, argc );
    do_foo( argc, ainst );

    return 0;
}
