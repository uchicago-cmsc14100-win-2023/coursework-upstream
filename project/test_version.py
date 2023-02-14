"""
CMSC 14100
Winter 2023

Test code for Project #1 Version Class
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
            (major, minor, patch) = version_info
            msg += f"  v{i} = {MODULE}.Version({major}, {minor}, {patch})\n"
        else:
            msg += f"  v{i} = {version_info}\n"

    return msg


def check_version_construction(name, major, minor, patch):
    try:
        v = version.Version(major, minor, patch)
    except Exception as e:
        msg = f"Unexpected exception caught when constructing {name}: {e}\n" + \
            f"\nException {traceback.format_exc()}"
        return None, msg

    return v, None

@pytest.mark.parametrize("major, minor, patch",
                         [(1, 2, 3),
                          (0, 1, 2),
                          (0, 2, 1),
                          (3, 2, 4)])
def test_version_constructor(major, minor, patch):
    recreate_msg = gen_recreate_header([(major, minor, patch)])

    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)


@pytest.mark.parametrize("major, minor, patch",
                         [(1, 2, 3),
                          (0, 1, 2),
                          (10, 20, 5),
                          (3, 2, 4)])
def test_get_major(major, minor, patch):
    recreate_msg = gen_recreate_header([(major, minor, patch)]) + \
        f"  v0.get_major()\n"

    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = v0.get_major()
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(msg)

    error_msg = helpers.check_result(actual, major, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("major, minor, patch",
                         [(1, 2, 3),
                          (0, 1, 2),
                          (10, 20, 5),
                          (3, 2, 4)])
def test_get_minor(major, minor, patch):
    recreate_msg = gen_recreate_header([(major, minor, patch)]) + \
        f"  v0.get_minor()\n"

    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = v0.get_minor()
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(msg)

    error_msg = helpers.check_result(actual, minor, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("major, minor, patch",
                         [(1, 2, 3),
                          (0, 1, 2),
                          (10, 20, 5),
                          (3, 2, 4)])
def test_get_patch(major, minor, patch):
    recreate_msg = gen_recreate_header([(major, minor, patch)]) + \
        f"  v0.get_patch()\n"

    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = v0.get_patch()
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(msg)

    error_msg = helpers.check_result(actual, patch, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)
        

@pytest.mark.parametrize("major, minor, patch, expected",
                         [(1, 2, 3, True),
                          (0, 1, 2, False),
                          (0, 0, 2, False),
                          (0, 2, 0, False),
                          (10, 0, 5, True),
                          (3, 2, 0, True)])
def test_is_stable(major, minor, patch, expected):
    recreate_msg = gen_recreate_header([(major, minor, patch)]) + \
        f"  v0.is_stable()\n"

    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = v0.is_stable()
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(msg)
        
    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)



@pytest.mark.parametrize("major, minor, patch, expected",
                         [(1, 2, 3, "1.2.3"),
                          (0, 1, 2, "0.1.2"),
                          (10, 20, 5, "10.20.5"),
                          (3, 2, 4, "3.2.4")])
def test_version_str_method(major, minor, patch, expected):
    recreate_msg = gen_recreate_header([(major, minor, patch)]) + \
        f"  str(v0)\n"

    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", major, minor, patch)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = str(v0)
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(msg)
        
    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


COMES_BEFORE = -1
EQUALS = 0
COMES_AFTER = 1
FAILURE = 2

relop_tests = [
    ((0, 0, 0), (0, 0, 0), EQUALS),

    ((0, 0, 0), (0, 0, 1), COMES_BEFORE),
    ((0, 0, 1), (0, 0, 0), COMES_AFTER),

    ((0, 0, 0), (0, 1, 0), COMES_BEFORE),
    ((0, 1, 0), (0, 0, 0), COMES_AFTER),

    ((0, 0, 0), (1, 0, 0), COMES_BEFORE),
    ((1, 0, 0), (0, 0, 0), COMES_AFTER),

    ((3, 2, 1), (3, 2, 1), EQUALS),

    ((3, 2, 0), (3, 2, 1), COMES_BEFORE),
    ((3, 2, 1), (3, 2, 0), COMES_AFTER),

    ((3, 1, 1), (3, 2, 1), COMES_BEFORE),
    ((3, 2, 1), (3, 1, 1), COMES_AFTER),

    ((2, 2, 1), (3, 2, 1), COMES_BEFORE),
    ((3, 2, 1), (2, 2, 1), COMES_AFTER),
    
    ((3, 1, 10), (3, 2, 1), COMES_BEFORE),
    ((3, 2, 1), (3, 1, 10), COMES_AFTER),

    ((3, 3, 2), (4, 3, 2), COMES_BEFORE),
    ((4, 3, 2), (3, 3, 2), COMES_AFTER),
    ]


def relop_helper(v0_parts, v1_parts, expected, op_fn, recreate_msg):
    # construct the necessary instance
    v0, error_msg = check_version_construction("v0", *v0_parts)
    if error_msg is not None:
        return "\n" + error_msg + recreate_msg
    
    # construct the necessary instance
    v1, error_msg = check_version_construction("v1", *v1_parts)
    if error_msg is not None:
        return "\n" + error_msg + recreate_msg

    try:
        actual = op_fn(v0, v1)
    except Exception as e:
        msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        return msg

    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg is not None:
        return error_msg
    
    return None


@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_eq(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 == v1\n"

    expected = (relationship == EQUALS)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 == v1, recreate_msg)
    print("em:", error_msg)
    if error_msg is not None:
        pytest.fail(error_msg)
        

@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_ne(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 != v1\n"

    expected = (relationship != EQUALS)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 != v1, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_gt(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 > v1\n"

    expected = (relationship == COMES_AFTER)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 > v1, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_ge_method(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 >= v1\n"

    expected = (relationship == COMES_AFTER) or (relationship == EQUALS)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 >= v1, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)
        

@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_lt(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 < v1\n"

    expected = (relationship == COMES_BEFORE)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 < v1, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


@pytest.mark.parametrize("v0_parts, v1_parts, relationship",
                         relop_tests)
def test_le(v0_parts, v1_parts, relationship):
    recreate_msg = gen_recreate_header([v0_parts, v1_parts]) + \
        f"  v0 <= v1\n"

    expected = (relationship == COMES_BEFORE) or (relationship == EQUALS)
    error_msg = relop_helper(v0_parts, v1_parts, expected,
                             lambda v0, v1: v0 <= v1, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)

        
