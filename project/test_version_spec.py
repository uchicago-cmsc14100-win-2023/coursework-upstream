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

    msg = (f"\n\nTo recreate this test in ipython3, run:\n" + 
           version_import_str + 
           f"  import {MODULE}\n" + 
           f"  vs = {MODULE}.Version_Spec('{version_str}')\n")

    return msg


def check_construction(name, con_fn):
    try:
        v = con_fn()
    except Exception as e:
        msg = f"Unexpected exception caught when constructing {name}: {e}\n" + \
            f"\nException {traceback.format_exc()}"
        return None, msg

    return v, None


@pytest.mark.parametrize("vs_str",
                         ["^1.2.3",
                          "+1.2.3",
                          "~1.2.3",
                          "1.2.3"])
def test_version_spec_constructor(vs_str):
    recreate_msg = gen_recreate_header(vs_str)

    vs, error_msg = check_construction("vs",
                                       lambda : version_spec.VersionSpecification(vs_str))
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)


@pytest.mark.parametrize("vs_str",
                         ["^1.2.3",
                          "+1.2.3",
                          "~1.2.3",
                          "1.2.3"])
def test_version_spec_str_method(vs_str):
    recreate_msg = gen_recreate_header(vs_str) + \
        f"  str(vs)\n"

    # construct the necessary instance
    vs, error_msg = check_construction("vs",
                                       lambda : version_spec.VersionSpecification(vs_str))
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = str(vs)
    except Exception as e:
        error_msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        pytest.fail(error_msg)

    error_msg = helpers.check_result(actual, vs_str, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)
        


@pytest.mark.parametrize("vs_str, v_tuple, expected",
                         [("1.2.3", (1, 2, 3), True),
                          ("1.2.3", (1, 2, 4), False),
                          ("1.2.3", (1, 4, 3), False),
                          ("1.2.3", (4, 2, 3), False),
                          ("0.2.3", (0, 2, 3), True),

                          ("~10.20.30", (10, 20, 30), True),
                          ("~10.20.30", (10, 20, 31), True),
                          ("~10.20.30", (10, 20, 29), False),
                          ("~10.20.30", (10, 21, 30), False),
                          ("~10.20.30", (10, 21, 31), False),
                          ("~10.20.30", (11, 20, 30), False),

                          ("^100.200.300", (100, 200, 300), True),
                          ("^100.200.300", (100, 201, 300), True),
                          ("^100.200.300", (100, 201, 301), True),
                          ("^100.200.300", (100, 201, 299), True),                                                    
                          ("^100.200.300", (100, 200, 299), False),
                          ("^100.200.300", (100, 199, 300), False),
                          ("^100.200.300", (100, 199, 301), False),
                          ("^100.200.300", (100, 199, 299), False),
                          ("^100.200.300", (101, 200, 300), False),
                          ("^100.200.300", (99, 199, 299), False),
                          ("^100.200.300", (90, 200, 300), False),

                          ("+1000.2000.3000", (1000, 2000, 3000), True),
                          ("+1000.2000.3000", (1000, 2001, 3000), True),
                          ("+1000.2000.3000", (1000, 2001, 3010), True),
                          ("+1000.2000.3000", (1000, 2001, 2990), True),                                                    

                          ("+1000.2000.3000", (1001, 2000, 3000), True),
                          ("+1000.2000.3000", (1001, 2001, 3000), True),
                          ("+1000.2000.3000", (1001, 2001, 2990), True),
                          ("+1000.2000.3000", (1001, 2001, 3010), True),
                          ("+1000.2000.3000", (1001, 1999, 3000), True),                                                    

                          ("+1000.2000.3000", (1000, 2000, 2990), False),
                          ("+1000.2000.3000", (1000, 1990, 3000), False),
                          ("+1000.2000.3000", (1000, 1990, 3010), False),
                          ("+1000.2000.3000", (1000, 1990, 2990), False),
                          ("+1000.2000.3000", (990, 1990, 2990), False),
                          ("+1000.2000.3000", (900, 2000, 3000), False),
                          ])
def test_satisfies_specification(vs_str, v_tuple, expected):
    major, minor, patch = v_tuple
    recreate_msg = gen_recreate_header(vs_str) + \
        f"  v = version.Version({major}, {minor}, {patch})\n" + \
        f"  vs.satisfies_specification(v)\n"

    # construct the necessary VersionSpecification instance
    vs, error_msg = check_construction("vs",
                                       lambda : version_spec.VersionSpecification(vs_str))
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    # construct the necessary Version instance
    v, error_msg = check_construction("v",
                                       lambda : version.Version(*v_tuple))
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = vs.satisfies_specification(v)
    except Exception as e:
        error_msg = f"Unexpected exception caught: {e}\n" + \
            f"\nException {traceback.format_exc()}" + \
            recreate_msg
        print(error_msg)
        pytest.fail(error_msg)

    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)

        
