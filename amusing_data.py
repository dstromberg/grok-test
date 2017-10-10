#!/usr/bin/python

"""Generate some amusing data."""

# It is your choice for the type of data you would like to send. It could
# be bitcoin prices at a given time, it could be the CPU utilization on the
# server at a given time, it could be temperature in your city at a given
# time. Keep in mind that this data will need to keep running for a few
# days. It is up to you where you want to get this data, whether you read
# from a csv, whether you make requests to another service to get this
# data. It doesn't matter to us, but we will judge your creativity in this
# process.

# This code runs on 2.x and 3.x
# We really only need 2.x, but my tools are configured to use 3.x now.

from __future__ import print_function

import os
import time
import pprint
import itertools

import port


# It might be nice to do Redhat stock price data.  However, I haven't yet
# had much luck finding a module or REST interface that still works as
# described.  This might be a reasonable approximation, though it seems to
# update only seldom, if at all:
#
# $ curl 'http://download.finance.yahoo.com/d/quotes.csv?s=rht&f=price'
# below cmd output started 2017 Sat Oct 07 08:22:50 AM PDT
# 115.52,70.05,N/A,"+1.54 - +1.33%",1.67
# above cmd output done    2017 Sat Oct 07 08:22:50 AM PDT


def timestamps_forever():
    """Generate timestamps forever."""
    while True:
        current_time = int(time.time())
        yield current_time


def perfect_squares_forever():
    """
    Generate perfect squares forever.
    We take advantage of the fact that perfect squares increase by an odd
    integer each time to avoid multiplying large numbers.
    """
    square = 1
    adjustment = 3
    while True:
        yield square
        square += adjustment
        adjustment += 2


def lcg_random_numbers_forever(seed=None):
    """
    Generate random numbers forever, using the constants from glibc.
    The algorithm used is Linear Congruential.
    """
    modulus = pow(2, 31) - 1
    multiplier = 1103515245
    increment = 12345

    if seed is None:
        # This is not a strong seed, but it's good enough for our purposes
        seed = int(time.time() * os.getpid()) % modulus

    while True:
        seed = (multiplier * seed + increment) % modulus
        yield seed


def amusing_data():
    """
    Generate amusing data (strings) forever.

    The amusing data is comprised of:
    1) A datum number.
    2) A timestamp: seconds since the epoch And a human-readable time.
    3) Perfect squares that grow forever.
    4) Random numbers that go on forever with a decent-but-not-awesome period.
    """
    for tuple_ in port.ZIPPER(
            itertools.count(1),
            timestamps_forever(),
            perfect_squares_forever(),
            lcg_random_numbers_forever(),
    ):
        result_dict = {}
        (
            result_dict['datumno'],
            result_dict['timestamp'],
            result_dict['perfect-square'],
            result_dict['random-number'],
        ) = tuple_
        yield result_dict


def main():
    """Main function."""
    # top = 1000000
    top = 10
    # Print the first "top" values from amusing_data
    for row in port.ZIPPER(range(top), amusing_data()):
        pprint.pprint((top - row[0], row[1]))

if __name__ == '__main__':
    main()
