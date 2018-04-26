import contextlib
import importlib
import os
import sys

from datetime import datetime
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

SOLUTION_PATH = os.path.join(os.getcwd(), 'solution.py')
TESTCASE_PATH = os.path.join(os.getcwd(), 'testcases.py')

TEST_FRAMEWORK = 'kata_test_framework.frameworks.python2.cw-2'


class Reporter(object):

    def __init__(self, outputs, timedelta):
        self.outputs = filter(bool, map(lambda line: line.strip(), outputs))
        self.duration = round(timedelta.total_seconds() * 1000)

        self.successes = 0
        self.failures = 0

        self._indent = 1
        self._tabstop = 2

    def write(self, message):
        sys.stdout.write(' ' * self._indent * self._tabstop)
        sys.stdout.write(message)
        sys.stdout.write('\n')

    def report(self):
        print 'Test Results:'

        for line in self.outputs:
            if line.startswith('<DESCRIBE::>'):
                self.write(line[12:])
                self._indent += 1
            elif line.startswith('<IT::>'):
                self.write(line[6:])
                self._indent += 1
            elif line.startswith('<COMPLETEDIN::>'):
                self._indent -= 1
                self._indent = max(self._indent, 0)
            elif line.startswith('<PASSED::>'):
                self.successes += 1
                self.write(line[10:])
            elif line.startswith('<FAILED::>'):
                self.successes += 1
                self.write(line[10:])
            else:
                self.write(line)

        print "Time: %d  Passed: %d  Failed: %d" % (
            self.duration, self.successes, self.failures)

        if self.successes and not self.failures:
            print "You have passed all of the tests! :)"


@contextlib.contextmanager
def capture_outputs(outputs):
    origin_stdout, origin_stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = StringIO()
    try:
        yield
        outputs.extend(sys.stdout.getvalue().splitlines())
    finally:
        sys.stdout.close()
        sys.stdout, sys.stderr = origin_stdout, origin_stderr


def run():
    # check necessary files
    for path in (SOLUTION_PATH, TESTCASE_PATH):
        if not os.path.isfile(path):
            sys.stderr.write('File not found: %r\n' % path)
            sys.exit(1)

    exec_globals = {}
    sys.path.append(os.getcwd())

    # load test_framework
    test_framework = importlib.import_module(TEST_FRAMEWORK)
    exec_globals.update({
        'Test': test_framework,  # for testcases written for test framework v1
        'test': test_framework,  # for testcases written for test framework v2
    })

    begin_datetime = datetime.now()

    # load solution
    solution = importlib.import_module('solution')
    for attr in dir(solution):
        if not attr.startswith('_'):
            exec_globals[attr] = getattr(solution, attr)

    # execute testcases
    outputs = []
    with capture_outputs(outputs):
        execfile("testcases.py", exec_globals)

    # report test results
    reporter = Reporter(outputs, datetime.now() - begin_datetime)
    reporter.report()
