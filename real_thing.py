#!/usr/bin/python3

"""Upload data to Grok indefinitely."""

# This code runs on 2.x and 3.x
# We really only need 2.x, but my tools are configured to use 3.x now.

from __future__ import print_function

import os
import sys
import json
import time
import functools

import requests
# import requests.auth import HTTPBasicAuth
# requests.auth.HTTPBasicAuth

import port
import amusing_data
import every_n_seconds


def usage(retval):
    """Output a usage message."""

    if retval:
        write = sys.stderr.write
    else:
        write = sys.stdout.write

    write('Usage: {}\n'.format(sys.argv[0]))
    write('    --max-iterations 10\n')
    write('    --tenacious\n')
    write('    --source-name source_name\n')
    write('    --interval 300\n')

    sys.exit(retval)


class Options(object):
    # pylint: disable=too-few-public-methods
    """Deal with command line options."""

    def __init__(self):
        self.max_iterations = -1
        self.source_name = None
        self.base_url = None
        self.tenacious = False
        self.interval = None

        # We do this by hand so pylint can do its job more effectively.
        # It's a little more typing, but in a large project it becomes
        # worth it.
        while sys.argv[1:]:
            if sys.argv[1] == '--max-iterations':
                self.max_iterations = int(sys.argv[2])
                del sys.argv[1]
            elif sys.argv[1] == '--source-name':
                self.source_name = sys.argv[2]
                del sys.argv[1]
            elif sys.argv[1] == '--base-url':
                self.base_url = sys.argv[2]
                del sys.argv[1]
            elif sys.argv[1] == '--tenacious':
                self.tenacious = True
            elif sys.argv[1] == '--interval':
                self.interval = int(sys.argv[2])
                del sys.argv[1]
            elif sys.argv[1] in ('-h', '--help'):
                usage(0)
            else:
                string = '{}: Unrecognized option: {}\n'
                tuple_ = (sys.argv[0], sys.argv[1])
                sys.stderr.write(string.format(*tuple_))
                usage(1)
            del sys.argv[1]

    def check(self):
        """Check options for validity."""

        if self.source_name is None:
            string = '{}: --source-name is a required option\n'
            sys.stderr.write(string.format(sys.argv[0]))
            usage(1)

        if self.base_url is None:
            string = '{}: --base-url is a required option\n'
            sys.stderr.write(string.format(sys.argv[0]))
            usage(1)

        if self.interval is None:
            string = '{}: --interval is a required option\n'
            sys.stderr.write(string.format(sys.argv[0]))
            usage(1)


class UploadError(Exception):
    """An exception to raise on upload error - temporary or permanent."""


def get_auth_data():
    """Obtain authentication credentials from ~/.grok-auth-data ."""

    with open(os.path.expanduser('~/.grok-auth-data'), 'r') as file_:
        auth_data_line = file_.readline()

    fields = auth_data_line.split(':')

    if len(fields) != 2:
        string = '{}: Error: Bad number of fields in ~/.grok-auth-data\n'
        sys.stderr.write(string.format(sys.argv[0]))
        sys.exit(1)

    return fields


def post(url, data):
    """Post data to url."""

    current_time = int(time.time())
    print('posting at {} {}'.format(current_time, time.ctime(current_time)))
    username, password = get_auth_data()

    # Turning off SSL verification like this is ugly, but:
    # 1) Linux Mint 18.2's CPython 2.x build doesn't do it correctly.
    # 2) It's not worth the time to get a proper SSL certificate for this test.
    #
    # In production, we'd want to get a cert, and possibly build a
    # a better version of CPython 2 and/or the SSL library.
    result = requests.post(
        url,
        data=data,
        verify=False,
        auth=requests.auth.HTTPBasicAuth(username, password),
    )

    return result


def send_data_to_grok(base_url, source_name, timestamp, value, tenacious):
    """Send data (value) to grok custom metric named by "source_name"."""

    # This ssl_verify thing is an icky hack. For production code, it would be
    # better to fix the underlying problem by:
    # 1) moving to Python 3
    # Or:
    # 2) Rebuilding Python 2 and/or the SSL library.

    url = port.urljoin(base_url, '_metrics/custom/{}'.format(source_name))

    dict_ = {'timestamp': timestamp, 'value': value}
    data = json.dumps(dict_)

    if tenacious:
        # If we're "tenacious", we map all exceptions to UploadError for
        # every_n_seconds to deal with.
        try:
            result = post(url, data=data)
        except Exception as exc:
            exc_name = type(exc).__name__
            string = 'Got exception {} from requests.post'
            raise UploadError(string.format(exc_name))
    else:
        # If we're not tenacious, we just let the exception bubble up - for
        # ease of debugging
        result = post(url, data=data)

    if result.status_code != 200:
        raise UploadError('Got HTTP status_code {}'.format(result.status_code))

    return result


def main():
    """Main function."""
    options = Options()
    options.check()

    if options.max_iterations < 0:
        iterator = port.my_range(None)
    else:
        iterator = port.my_range(options.max_iterations)

    runner = every_n_seconds.EveryNSeconds(
        seconds=options.interval,
        resolution=0.001,
        retry_exceptions=(UploadError, ),
        )

    for tuple_ in port.ZIPPER(
            (x + 1 for x in iterator),
            amusing_data.timestamps_forever(),
            amusing_data.perfect_squares_forever(),
    ):
        datumno, timestamp, perfect_square = tuple_
        _unused = datumno
        # print(datumno, *tuple_)
        callback = functools.partial(
            send_data_to_grok,
            base_url=options.base_url,
            source_name=options.source_name,
            timestamp=timestamp,
            value=perfect_square,
            tenacious=options.tenacious,
            )
        if runner.is_done_running(callback=callback):
            break

main()
