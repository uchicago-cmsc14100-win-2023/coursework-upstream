"""
CMSC 14100
Winter 2023

Test helper functions
"""

import pytest


def check_result(actual, expected, recreate_msg):
    # check that the result is not None
    if actual is None:
        return gen_none_error(actual, recreate_msg)

    # check the type error
    if not isinstance(actual, type(expected)):
        return gen_type_error(actual, expected, None, recreate_msg)

    if actual != expected:
        return gen_equals_error(actual, expected, recreate_msg)

    return None


def gen_none_error(actual, recreate_msg=None):
    """
    Generate an error if the actual value is unexpectedly none.
    """

    msg = ("\n\nThe function returned None when a value "
           "other than None was expected.\n"
           "Common sources of this problem include:\n"
           "  - including a print statement rather than a return statement, and\n"
           "  - forgetting to include a return statement along some path in the compuation.\n")
    if recreate_msg is not None:
        msg = msg + recreate_msg
            
    return msg

def gen_type_error(actual, expected, expected_type_str=None, recreate_msg=None):
    """
    Generate an error if the actual value has the wrong type.
    """
    if expected_type_str is None:
        expected_type_str = type(expected).__name__

    msg = (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {expected_type_str}\n"
           f"  Actual return type: {type(actual).__name__}\n")

    if recreate_msg is not None:
        msg = msg + recreate_msg

    return msg


def gen_equals_error(actual, expected, recreate_msg=None):
    """
    Generate an error if the actual and expected values are not
    equal.
    """
    msg = ("\n\nThe actual and expected values do not match\n"
           f"  Expected: {expected}\n"
           f"  Actual: {actual}\n")

    if recreate_msg is not None:
        msg += recreate_msg

    return msg



    
