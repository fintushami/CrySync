def setup():
    print("basic setup into module")


def teardown():
    print("basic teardown into module")


def setup_module(module):
    print("module setup")


def teardown_module(module):
    print("module teardown")


def setup_function(function):
    print("function setup")


def teardown_function(function):
    print("function teardown")


def test_imports():
    print("test import")
    import os
    import sys
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
    from gostcrypt import MsgEncryptor
    from gostcrypt import cbcEncryptor
    from protocol.Datatypes import Response
    from protocol.Datatypes import Request
    from protocol.Transport import Serialize


class TestUM:
    def setup(self):
        print("basic setup into class")

    def teardown(self):
        print("basic teardown into class")

    def setup_class(cls):
        print("class setup")

    def teardown_class(cls):
        print("class teardown")

    def setup_method(self, method):
        print("method setup")

    def teardown_method(self, method):
        print("method teardown")
    #
    # def test_numbers_5_6(self):
    #     print("test 5*6")
    #     assert 5 * 6 == 30
