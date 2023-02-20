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
import version_spec

MODULE = "version_spec"

def gen_recreate_header(version_str, include_version=False):
    if include_version:
        version_import_str = f"  import version\n"
    else:
        version_import_str = ""

    if isinstance(version_str, str):
        arg_str = f"'{version_str}'"
    else:
        arg_str = f"{version_str}"

    msg = (f"\n\nTo recreate this test in ipython3, run:\n" + 
           version_import_str + 
           f"  import {MODULE}\n" + 
           f"  vs = {MODULE}.VersionSpecification({arg_str})\n")

    return msg


def check_construction(name, con_fn, exception_expected):
    try:
        v = con_fn()
    except version_spec.VersionSpecException as e:
        if exception_expected:
            return None, None
        else:
            msg = (f"Unexpected VersionSpecException raised. This test was\n"
                   f"not expected to raise an exception:\n  {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg
    except Exception as e:
        if exception_expected:
            msg = (f"This test was expected to raise a VersionSpecException,\n"
                   f"but a different exception was raised instead:\n"
                   f"  {e.__class__.__name__}: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg
        else:
            msg = (f"Unexpected exception caught:\n"
                   f"  {e.__class__.__name__}: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg

    if exception_expected:
        msg = ("This test was expected to raise a VersionSpecException,\n"
               " but no exception was raised.")
        return None, msg
    
    return v, None


@pytest.mark.parametrize("vs_str",
                         [5,
                          "^1.2",
                          "+1.2.-3",
                          "~1.2.",
                          "#1.2.3",
                          "1",
                          "1.",
                          "",
                          5,
                          None])
def test_exceptions_VS_constructor(vs_str):
    recreate_msg = gen_recreate_header(vs_str)

    vs, error_msg = check_construction("vs",
                                       lambda : version_spec.VersionSpecification(vs_str),
                                       True)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)


@pytest.mark.parametrize("ver",
                         ["1.2.3",
                          5,
                          None,
                          (1, 2, 3),
                          ])
def test_exception_satisfies_specification(ver):
    vs_str = "1.2.3"
    ver_str = f"'{ver}'" if isinstance(ver, str) else str(ver)

    recreate_msg = gen_recreate_header(vs_str) + \
        f"  v = {ver_str}       # Not an instance of Version\n" + \
        f"  vs.satisfies_specification(v)\n"

    # construct the necessary VersionSpecification instance
    vs, error_msg = check_construction("vs",
                                       lambda : version_spec.VersionSpecification(vs_str),
                                       False)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    # v is expected to be bad, don't both to construct it.

    try:
        actual = vs.satisfies_specification(ver)
    except version_spec.VersionSpecException as e:
        # this is the expected behaviour for these tests
        return
    except Exception as e:
        msg = (f"This test was expected to raise a VersionSpecException,\n"
               f"but a different exception was raised instead:\n"
               f"  {e.__class__.__name__}: {e}\n"
               f"\nException {traceback.format_exc()}")
        pytest.fail(msg + recreate_msg + "\n")

    msg = ("\nThis test was expected to raise a VersionSpecException,\n"
           "but no exception was raised.")
    pytest.fail(msg + recreate_msg + "\n")
    
        
