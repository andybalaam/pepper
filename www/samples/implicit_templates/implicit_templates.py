# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import random
import sys

def lst_swap( lst, i1, i2 ):
    lst[i1], lst[i2] = lst[i2], lst[i1]

def partition( lst, start, end, pi ):
    # Swap the pivot to the end for now
    last = end - 1
    lst_swap( lst, pi, last )
    pivot_item = lst[last]

    # Compare each value to the pivot and if smaller, put it at the beginning
    counter = start
    for idx, item in enumerate( lst[start:last], start ):
        if item < pivot_item:
            lst_swap( lst, idx, counter )
            counter += 1

    # Put the pivot back in the middle
    lst_swap( lst, last, counter )

    # Return where the pivot ended up
    return counter



def choose_pivot_index( start, end ):
    return random.randrange( start, end )


def quick_sort( lst, start, end ):
    if end - start <= 1:
        return
    pi = choose_pivot_index( start, end )
    new_pi = partition( lst, start, end, pi )
    quick_sort( lst, start, new_pi )
    quick_sort( lst, new_pi + 1, end )


def sort( lst ):
    quick_sort( lst, 0, len( lst ) )

nums = [ (int)( arg ) for arg in sys.argv[1:] ]

# This line causes an "array(int,3)" version of sort to be created
sort( nums )

print( nums )

