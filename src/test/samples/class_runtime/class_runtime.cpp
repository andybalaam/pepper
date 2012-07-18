#include <stdio.h>

struct MyClass
{
    int a;
    double b;
};

void MyClass_eey_c_eey___init__( MyClass& self, int a, double b )
{
    self.a = a;
    self.b = b;
}

int MyClass_eey_c_eey_meth( MyClass& self )
{
    return (self.a + 1);
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_eey_c_eey___init__( mc, argc, 1.5 );
    printf( "%d\n", mc.a );
    printf( "%f\n", mc.b );
    printf( "%d\n", MyClass_eey_c_eey_meth( mc ) );

    return 0;
}
