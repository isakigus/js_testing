#!/usr/bin/env python
import unittest
from testing_functions import Functions
from testing_data import get_tests_data

func = lambda x:  getattr(Functions, x)


class TestsContainer(unittest.TestCase):
    pass


def make_test_function(test_function, test_args=None):

    def test(self):

        if test_args:
            test_function(self, **test_args)
        else:
            test_function(self)

    return test


def generate_test_with_data(key):

    for rec in get_tests_data(key):

        test_function = func(rec.get('function'))
        test_name = rec.get('name')
        test_args = rec.get('test_args')

        test_dynamic_func = make_test_function(test_function, test_args)
        setattr(TestsContainer, 'test_{0}'.format(
            test_name), test_dynamic_func)


def main():

    try:
        import nocommit
    except ImportError:
        exit('\n  no data provided [spreadsheet key]\n')

    generate_test_with_data(nocommit.key)
    unittest.main()


if __name__ == '__main__':
    main()
