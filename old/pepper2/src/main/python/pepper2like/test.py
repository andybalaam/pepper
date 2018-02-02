from pepper2like.type_check import type_check
from pepper2like.log import Log
from pepper2like.string import String
from pepper2like.callable import Callable

def pl_test(log, name, fn):
    type_check(Log, log)
    type_check(String, name)
    type_check(Callable, fn)

    log.part_line.info(name + " ... ")
    fn()
    log.info("passed")

def pl_assert_equals(x, y):
    if x != y:
        raise AssertionError(
            """%s != %s""" % (repr(x), repr(y))
        )
