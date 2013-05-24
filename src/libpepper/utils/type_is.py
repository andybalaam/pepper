# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# I assure you before God that what I am writing to you is no lie.
# Galations 1 v20

import types
import abc

def type_is( typ, inst ):
    """
    Check that instance is of (exact) type typ.
    Throws an Assertion error if not.
    The arguments order is supposed to be remenicent of C/Java style
    function declarations.
    """

    # Arguably, we should allow duck typing to take its course
    # here - there could be some other metaclass we need to
    # add later, but I prefer the easier-to-understand error
    # message we get by checking the type.
    if not (
            type(typ) == type or
            type(typ) == types.ClassType or
            type(typ) == abc.ABCMeta
    ):
        raise AssertionError(
            "Wrong arguments to type_is: the first argument must be a " +
            "class or type, not %s" % typ.__class__.__name__
        )

    if inst.__class__ != typ:
        raise AssertionError(
            "type_is check failed: expected a %s but found a %s." % (
                typ.__name__, inst.__class__.__name__ ) )

