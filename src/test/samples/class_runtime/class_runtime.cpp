
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

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_eey_c_eey___init__( mc, argc, 1.5 );

    return 0;
}
