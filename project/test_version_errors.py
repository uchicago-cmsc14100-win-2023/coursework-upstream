"""
CMSC 14100
Winter 2023

Test code for Project #2 Version Class
Testing Error Checking
"""
import os
import sys
import traceback

import pytest
import test_helpers as helpers


# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position
import version

MODULE = "version"

def gen_recreate_header(versions):
    msg = (f"\n\nTo recreate this test in ipython3, run:\n"
           f"  import {MODULE}\n")

    for i, version_info in enumerate(versions):
        if isinstance(version_info, tuple):
            (major, minor, patch) = [str(x) if isinstance(x, int) else f"'{x}'" for x in version_info]
            msg += f"  v{i} = {MODULE}.Version({major}, {minor}, {patch})\n"
        elif isinstance(version_info, str):
            msg += f"  v{i} = '{version_info}'\n"            
        else:
            msg += f"  v{i} = {version_info}\n"

    return msg


def check_version_construction(name, major, minor, patch, exception_expected=False):
    try:
        v = version.Version(major, minor, patch)
    except version.VersionException as e:
        if exception_expected:
            return None, None
        else:
            msg = (f"Unexpected VersionException raised.  This test was\n"
                   f"not expected to raise an exception: {e}")
            return None, msg
    except Exception as e:
        if exception_expected:
            msg = (f"This test was expected to raise a VersionException,\n"
                   f"but a different exception was raised instead: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg
        else:
            msg = (f"Unexpected exception caught: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg

    if exception_expected:
        msg = ("This test was expected to raise a VersionException,\n"
               "but no exception was raised.")
        return None, msg
    return v, None

@pytest.mark.parametrize("major, minor, patch",
                         [("3", 2, 1),
                          (3, "2", 1),
                          ("3", "2", "1"),
                          (3, 2, "1"),
                          (-1, 1, 1),
                          (1, -1, 1),
                          (1, 1, -1),
                          (-1, -1, -1)])
def test_exceptions_for_constructor(major, minor, patch):
    recreate_msg = gen_recreate_header([(major, minor, patch)])

    v0, error_msg = check_version_construction("v0", major, minor, patch, True)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)


COMES_BEFORE = -1
EQUALS = 0
COMES_AFTER = 1
FAILURE = 2

relop_tests = [
    ((3, 2, 1), None),
    ((3, 2, 1), 5),
    ((3, 2, 1), "cs141"),

]

def relop_helper(v0_parts, v1, op_fn, recreate_msg, exception_expected):
    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", *v0_parts)
    if error_msg is not None:
        return "\n" + error_msg + recreate_msg
    
    # expect v1 to be bad, so don't both to try to construct it.

    try:
        actual = op_fn(v0, v1)
    except version.VersionException as e:
        if exception_expected:
            return None
        else:
            # should never get here, since we always expected
            # a VersionException in this test code. 
            msg = (f"Unexpected VersionException raised.  This test was\n"
                   f"not expected to raise an exception: {e}")
            return msg + recreate_msg
    except Exception as e:
        msg = (f"This test was expected to raise a VersionException,\n"
               f" but a different exception was raised instead: {e}\n"
               f"\nException {traceback.format_exc()}")
        return msg + recreate_msg

    if exception_expected:
        msg = ("This test was expected to raise a VersionException,\n"
               " but no exception was raised.")
        return msg + recreate_msg

    return None

@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_eq(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 == v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 == v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)
        

@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_ne(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 != v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 != v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_gt(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 > v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 > v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_ge(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 >= v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 >= v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)
        

@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_lt(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 < v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 < v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1", relop_tests)
def test_exception_le(v0_parts, v1):
    recreate_msg = gen_recreate_header([v0_parts, v1]) + \
        f"  v0 <= v1\n"

    error_msg = relop_helper(v0_parts, v1,
                             lambda v0, v1: v0 <= v1, recreate_msg, True)
    if error_msg is not None:
        pytest.fail(error_msg)

        
