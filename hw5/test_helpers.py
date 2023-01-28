"""
CMSC 14100
Autumn 2022

Test helper functions
"""

import pytest

def gen_recreate_msg(module, function, *params):
    """
    Generate a message to explain how to recreate a test in ipython.
    """
    params = [str(p) if not isinstance(p, str) else f"'{p}'" for p in params]
    params_str = ", ".join(params)

    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {module}\n"
                    f"  {module}.{function}({params_str})\n\n")

    return recreate_msg


def check_not_none(actual, recreate_msg=None):
    """
    Generate an error if the actual value is unexpectedly none.
    """

    msg = ("\n\nThe function returned None when a value "
           "other than None was expected.\n"
           "Common sources of this problem include:\n"
           "  - including a print statement rather than a return statement, and\n"
           "  - forgetting to include a return statement along some path in the compuation.\n")
    if recreate_msg is not None:
        msg += recreate_msg

    assert actual is not None, msg


def check_expected_none(actual, recreate_msg=None):
    """
    Generate an error if the actual value is not none
    """

    msg = "The function returned a value other than the expected value: None."
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is None, msg

def check_type(actual, expected, recreate_msg=None, expected_type_str=None):
    """
    Generate an error if the actual value has the wrong type.
    """
    if expected_type_str is None:
        expected_type_str = type(expected).__name__

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {expected_type_str}\n"
           f"  Actual return type: {type(actual).__name__}\n")
    if recreate_msg is not None:
        msg += recreate_msg

    assert isinstance(actual, type(expected)), msg


def check_number(actual, recreate_msg=None):
    """
    Generate an error if the actual value is not an int or a float
    """
    actual_type = type(actual)

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: an integer or a float.\n"
           f"  Actual return type: {actual_type.__name__}.\n")
    if recreate_msg is not None:
        msg += recreate_msg

    assert isinstance(actual, (int, float)), msg


def check_equals(actual, expected, recreate_msg=None):
    """
    Generate an error if the actual and expected values are not
    equal.
    """
    msg = ("\n\nThe actual and expected values do not match\n"
           f"  Expected: {expected}\n"
           f"  Actual: {actual}\n")

    if recreate_msg is not None:
        msg += recreate_msg

    assert actual == expected, msg


def check_float_equals(actual, expected, recreate_msg=None):
    """
    Generate an error if the actual and expected values do not
    fall within epsilon of each other.
    """
    msg = (f"\n\nActual ({actual}) and expected ({expected}) "
           f"values do not match.\n")
    if recreate_msg is not None:
        msg += recreate_msg

    assert pytest.approx(expected) == actual, msg


def check_result(actual, expected, recreate_msg):
    """
    Do the work of checking the result when the correctness test is
    equality.
    """
    if expected is None:
        check_expected_none(actual, recreate_msg)
        return

    # We expect a result is not None
    check_not_none(actual, recreate_msg)

        # We expect a result of the right type
    check_type(actual, expected, recreate_msg)

    if isinstance(expected, float):
        # The expected result is a float. Check that the actual
        # value is close enought to the expected value
        check_float_equals(actual, expected, recreate_msg)
    else:
        # We expect a result that is the same as expected
        check_equals(actual, expected, recreate_msg)


def check_1D_list(actual, expected, expected_type_str, recreate_msg):
    """
    Verify that two lists are the same.
    """

    if recreate_msg is None:
        recreate_msg = ""

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {expected_type_str}\n")
    actual_type = type(actual)
    msg2 = f"  Actual return type: {actual_type.__name__}\n"

    assert isinstance(actual, list), msg + msg2 + recreate_msg

    if actual == expected:
        return

    msg = (f"\nThe actual length ({len(actual)}) of the result does not match the expected length ({len(expected)}) of the result")
    actual_len = len(actual)
    expected_len = len(expected)
    assert actual_len == expected_len, msg + recreate_msg

    msg3 = ("The type of the actual value is incorrect.\n"
            "  The actual value at index {} has type {}.\n"
            "  The expected type is {}.\n")

    msg4 = ("\n  The values do not match at list index {}:\n"
            "      The actual value is {}\n"
            "      The expected value is {}\n")

    for i, (actual_val, expected_val) in enumerate(zip(actual, expected)):
        actual_val_type = type(actual_val)
        expected_val_type = type(expected_val)
        assert isinstance(actual_val, expected_val_type), \
            msg3.format(i, actual_val_type.__name__, expected_val_type.__name__) \
               + recreate_msg

        actual_val_str = str(actual_val) if not isinstance(actual_val, str) else '"' + actual_val + '"'
        expected_val_str = str(expected_val) if not isinstance(expected_val, str) else '"' + expected_val + '"'
        assert actual_val == expected_val, \
            msg4.format(i, actual_val_str, expected_val_str) + recreate_msg
        
    
    
def check_list_unmodified(param_name, before, after, recreate_msg=None):
    """
    Generate an error if a list was modified when modifications
    are disallowed.
    """

    msg = "You modified the contents of the parameter {} (which is not allowed).\n"
    msg = msg.format(param_name)
    msg += "  Value before your code: {}\n".format(before)
    msg += "  Value after your code:  {}".format(after)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert before == after, msg


def check_2D_list_unmodified(param_name, before, after, recreate_msg=None):
    """
    Generate an error if a list was modified when modifications
    are disallowed.
    """

    msg = "You modified the contents of the parameter {} (which is not allowed).\n"
    msg = msg.format(param_name)
    msg += "  Value before your code: {}\n".format(before)
    msg += "  Value after your code:  {}".format(after)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert before == after, msg
    for b_val, a_val in zip(before, after):
        assert b_val == a_val, msg
        

def check_length(actual, expected, recreate_msg, desc=""):
    """
    Generate an error if the length is not correct.
    """

    if desc:
        msg = (f"\n\nThe actual length ({len(actual)}) of the list of {desc} does not "
               f"match the expected length ({len(expected)}) of the list of {desc}")
    else:
        msg = f"\n\nThe actual length ({len(actual)}) of the result does not match the expected length ({len(expected)}) of the result.\n"

    actual_len = len(actual)
    expected_len = len(expected)

    assert actual_len == expected_len, msg + recreate_msg


def check_tuple(actual, expected, expect_type_str, recreate_msg=""):
    """
    Verify that two tuples are the same.
    """
    if actual == expected:
        return

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {type(expected).__name__}\n"
           f"  Actual return type: {type(actual).__name__}\n")

    assert isinstance(actual, tuple), msg + recreate_msg

    msg = (f"\nThe actual length ({len(actual)}) does not match the expected length ({len(expected)})")
    assert len(actual) == len(expected), msg + recreate_msg

    if len(expected) < 5:
        msg = ("\n  The actual and expected values do not match:\n"
               f"     Expected: {expected}\n"
               f"     Actual: {actual}\n")

        assert actual == expected, msg + recreate_msg
    else:
        msg3 = ("The type of the actual value is incorrect.\n"
                "  The actual value at index {} has type {}.\n"
                "  The expected type is {}.\n")

        msg4 = ("\n  The values do not match at list index {}:\n"
                "      The actual value is {}\n"
                "      The expected value is {}\n")

        for i, (actual_val, expected_val) in enumerate(zip(actual, expected)):
            assert isinstance(actual_val, type(expected_val)), \
                msg3.format(i,
                            type(actual_val).__name__,
                            type(expected_val).__name__) \
                + recreate_msg

            actual_val_str = str(actual_val) if not isinstance(actual_val, str) else '"' + actual_val + '"'
            expected_val_str = str(expected_val) if not isinstance(expected_val, str) else '"' + expected_val + '"'
            assert actual_val == expected_val, \
                msg4.format(i, actual_val_str, expected_val_str) + recreate_msg
    

def check_2D_type(check_element_type_fn, actual, error_msg=None):
    """
    Generate an error if actual is not a list of lists.  Or if an
    element has the wrong type.
    """
    assert isinstance(actual, list), error_msg
    for row in actual:
        assert isinstance(row, list), error_msg
        for val in row:
            assert check_element_type_fn(val), error_msg


def check_2D_shape(actual, expected, recreate_msg):
    """
    Check that a list of lists has the right shape
    """

    msg = "The actual shape of the result does not match the expected shape\n"
    msg += "  Expected: {} x {}\n"
    msg += "  Actual: {} x {}\n"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    expected_n = len(expected)
    expected_m = len(expected[0])

    actual_n = len(actual)
    actual_m = len(actual[0])

    assert actual_n == expected_n and actual_m == expected_m, \
        msg.format(expected_n, expected_m, actual_n, actual_m)

    msg = "The rows in the actual result should all be of length {}"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    for row in actual:
        assert len(row) == actual_m, msg.format(expected_m)


def check_2D(check_val_fn, actual, expected, recreate_msg=None):
    """
    Generate an error if at least one entry in actual does not match expected.
    """
    check_2D_shape(actual, expected, recreate_msg)

    msg = "Actual and expected values do not match at location ({}, {}).\n"
    msg += "   Expected value: {}\n"
    msg += "   Actual value: {}"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    for i, row in enumerate(expected):
        for j, val in enumerate(row):
            if not check_val_fn(val, actual[i][j]):
                assert False, msg.format(i, j, val, actual[i][j])
        
