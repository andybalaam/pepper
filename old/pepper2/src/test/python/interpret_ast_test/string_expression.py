import sys

from pepper2like.ast.plast import plAst
from pepper2like.ast.plaststring import plAstString
from pepper2like.log import Log
from pepper2like.test import pl_test, pl_assert_equals
from pepper2like.type_check import type_check


log = Log(sys.stdout)


def Can_make_ast_node_for_string():
    ast = plAstString("s")
    type_check(plAst, ast)
    type_check(plAstString, ast)
    pl_assert_equals(ast.value, "s")
pl_test(log, "Can make AST node for string", Can_make_ast_node_for_string)
