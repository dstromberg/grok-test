# This is grok-test

This is code I wrote as part of an interview process with Grokstream.

The code just uploads perfect squares from 1, 4, 9, 16, ...infinity, one perfect square every five minutes.  See the
Makefile for invocation examples; some of the rules include:

<table width="100%" border="1">
    <tr>
        <td><br>Rule name</td>
        <td><br>Sample invocation</td>
        <td><br>What it is</td>
        <td><br>What it does</td>
    </tr>
    <tr>
        <td>add-dependencies</td>
        <td>make add-dependencies</td>
        <td>Dependency installation</td>
        <td>Install required rpm's and pypi packages</td>
    </tr>
    <tr>
        <td>run-curl-test</td>
        <td>make run-curl-test</td>
        <td>A rudimentary test script in bash+curl.  I used this to explore the API a little before starting
            the python coding.</td>
        <td>A bash syntax check and ./curl-test invocation</td>
    </tr>
    <tr>
        <td>run-test-every-n-seconds</td>
        <td>make run-test-every-n-seconds</td>
        <td>Automated tests for every_n_seconds.py</td>
        <td>Scrutinize every_n_seconds.py using pylint (2.x and 3.x), run pep8, and test on CPython 2.x and CPython 3.x</td>
    </tr>
    <tr>
        <td>run-real-thing</td>
        <td>make run-real-thing</td>
        <td>Automated tests for real_thing.py. <b>This is main entry point for the assignment</b></td>
        <td>Scrutinize all relevant .py's using pylint (2.x and 3.x), run pep8, and run forever on CPython 2.x.
            Works on 3.x too, but that is not enabled right now!</td>
    </tr>
</table>

BTW, the "make" rules want /usr/bin/python3, pylint for 2.x and 3.x, and pep8 for either - which you can get, on CentOS
7, by running "make add-dependencies".  _The code runs on either CPython 2.x or CPython 3.x, at your option!_

