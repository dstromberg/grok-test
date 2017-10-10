#!/usr/bin/python3

"""Some portability code."""

# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=wrong-import-order

# This code runs on 2.x and 3.x. In fact, that's its reason for existence.
# We really only need 2.x, but my tools are configured to use 3.x now.

import sys
import itertools

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# actually, pypi module "six" is a good way of doing things like this.


if hasattr(itertools, 'izip'):
    ZIPPER = getattr(itertools, 'izip')
else:
    ZIPPER = zip


def my_range(number):
    """
    Kinda like range/xrange with consistent semantics.
    But number is None means "iterate forever".
    """

    result = 0
    while True:
        yield result
        result += 1
        if number is not None and result >= number:
            break
