import sys

from pepper2like.log import Log
from pepper2like.test import pl_test, pl_assert_equals

log = Log(sys.stdout)

def check_maths_works():
    pl_assert_equals(2 + 2, 4)
pl_test(log, "Check maths works", check_maths_works)

