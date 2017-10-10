#!/usr/bin/python

"""
Provides a function that can execute a function or method every n seconds.
"""

# This code runs on 2.x and 3.x
# We really only need 2.x, but my tools are configured to use 3.x now.

from __future__ import print_function

import sys
import time


class EveryNSeconds(object):
    """Run a user-specified callback every n seconds, avoiding most drift."""

    # pylint: disable=too-many-instance-attributes,too-few-public-methods

    # This will still drift slightly - to really eliminate drift we probably
    # need a runno and to multiply that by "seconds".  But that will do
    # somewhat nonintuitive things if a laptop lid gets closed or there's
    # some form of network downtime.
    #
    # Neither is ideal for all situations.

    def __init__(self, seconds, resolution=0.1, max_reps=None,
                 retry_exceptions=(), retry_return_values=()):
        """Run callback every "seconds" seconds."""

        # pylint: disable=too-many-arguments
        # I'd like to use keyword only arguments here, but I can't since we're
        # targetting CPython 2.x.

        self.seconds = seconds
        self.resolution = resolution
        self.max_reps = max_reps
        self.retry_exceptions = retry_exceptions
        self.retry_return_values = retry_return_values

        self.current_rep = 0
        self.previous_time = time.time()

        self.first_iteration = True

    def is_done_running(self, callback):
        """Run callback subject to constraints specified in initializer."""

        while True:
            current_time = time.time()
            if \
                    self.previous_time + self.seconds <= current_time or \
                    self.first_iteration:
                self.first_iteration = False
                if self.max_reps is not None:
                    self.current_rep += 1
                    if self.current_rep > self.max_reps:
                        # We've run all we need; return indicating we're done.
                        return True
                try:
                    return_value = callback()
                except self.retry_exceptions as exc:
                    # We got an exception we should retry for.
                    # Sleep for "resolution" seconds and try again immediately.
                    # Do not update previous_time, which would change when we
                    # consider a success having been achieved.
                    exc_name = type(exc).__name__
                    string = '{}: Caught {} exception, retrying\n'
                    sys.stderr.write(string.format(sys.argv[0], exc_name))
                    self.current_rep -= 1
                    continue
                if return_value in self.retry_return_values:
                    string = '{}: Got {} return value, retrying\n'
                    formatted = string.format(sys.argv[0], str(return_value))
                    sys.stderr.write(formatted)
                    self.current_rep -= 1
                    continue
                self.previous_time = current_time
                # We did another callback run; return indicating that we're not
                # done.
                return False
            time.sleep(self.resolution)
