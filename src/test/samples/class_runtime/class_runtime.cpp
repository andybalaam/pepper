#include <stdio.h>

struct MyClass
{
    int a;
    double b;
};

void MyClass_pep_c_pep___init__( MyClass& self, int a, double b );
int MyClass_pep_c_pep_meth( MyClass& self );

void MyClass_pep_c_pep___init__( MyClass& self, int a, double b )
{
    self.a = a;
    self.b = b;
}

int MyClass_pep_c_pep_meth( MyClass& self )
{
    return (self.a + 1);
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_pep_c_pep___init__( mc, argc, 1.5 );
    printf( "%d\n", mc.a );
    printf( "%f\n", mc.b );
    printf( "%d\n", MyClass_pep_c_pep_meth( mc ) );

    return 0;
}
