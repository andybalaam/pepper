import sys

from pepper2like.ast.plaststring import plAstString
from pepper2like.log import Log
from pepper2like.parser.pl_parse import pl_parse
from pepper2like.test import pl_test, pl_assert_equals
from pepper2like.type_check import type_check


log = Log(sys.stdout)


def String_expr_parses_to_AST():
    ast = pl_parse('"s"')
    type_check(plAstString, ast)
pl_test(log, "String expression parses to AST", String_expr_parses_to_AST)


def String_expr_parse_holds_value():
    ast = pl_parse('"s"')
    pl_assert_equals(ast.value, "s")
pl_test(log, "String expr parse holds value", String_expr_parse_holds_value)
