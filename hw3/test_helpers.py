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
           "  - forgetting to replace the None placeholder in return statements,\n"
           "  - including a print statement rather than a return statement, and\n"
           "  - forgetting to include a return statement.\n")
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

def check_type(actual, expected, recreate_msg=None):
    """
    Generate an error if the actual value has the wrong type.
    """
    actual_type = type(actual)
    expected_type = type(expected)

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {expected_type.__name__}\n"
           f"  Actual return type: {actual_type.__name__}\n")
    if recreate_msg is not None:
        msg += recreate_msg

    assert isinstance(actual, expected_type), msg


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
    msg = ("\n\nActual and expected values do not match\n"
           f"  Actual: {actual}\n"
           f"  Expected: {expected}\n")
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
