"""
CMSC 14100
Winter 2023

Test code for Project #3
"""

import csv
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
import library
import version_spec
import hub

MODULE = "hub"



def gen_recreate_header():
    msg = (f"\n\nTo recreate this test in ipython3, run:\n"
           f"  import {MODULE}\n"
           f"  lib_hub = hub.LibraryHub()\n")
    return msg

def mk_str_parameter(x):
    return str(x) if not isinstance(x, str) else f"'{x}'"

def gen_reg_lib(hub_name, lib_var, lib_name, lib_ver, reg_by, exception_expected):
    lib_name = mk_str_parameter(lib_name)
    lib_ver = mk_str_parameter(lib_ver)
    reg_by = mk_str_parameter(reg_by)
    if exception_expected:
        comment = "\n  # LibraryHubException expected from the next call\n"
    else:
        comment = "\n  # no LibraryHubException expected from the next call\n"
    return (comment +
            f"  {lib_var} = {hub_name}.register_library({lib_name}, {lib_ver}, {reg_by})\n")


def add_libraries_to_hub(libs):
    parts = {}
    recreate_msg = gen_recreate_header()

    # building the hub should not fail
    lib_hub, error_msg = check_fn(lambda : hub.LibraryHub(), hub.LibraryHubException, False)
    if error_msg:
        parts["recreate_msg"] = recreate_msg
        parts["error_msg"] = error_msg
        return parts


    # construct the libraries
    libraries = []
    for i, (lib_name, lib_ver, reg_by, exception_expected) in enumerate(libs):
        recreate_msg += gen_reg_lib("lib_hub", f"lib{i}", lib_name, lib_ver, reg_by, exception_expected)
        lib, error_msg = check_fn(lambda : lib_hub.register_library(lib_name, lib_ver, reg_by),
                                  hub.LibraryHubException,
                                  exception_expected)
        if error_msg:
            parts["recreate_msg"] = recreate_msg
            parts["error_msg"] = error_msg
            return parts

        if not exception_expected:
            if lib is None:
                error_msg = (f"The register_library method returned None, when\n"
                             f"an instance of the Library class was expected.")
                parts["recreate_msg"] = recreate_msg
                parts["error_msg"] = error_msg
                return parts


            if not isinstance(lib, library.Library):
                error_msg = (f"The register_library method returned a value of type {type(lib)}, when\n"
                             f"an instance of the Library class was expected.")
                parts["recreate_msg"] = recreate_msg
                parts["error_msg"] = error_msg
                return parts

        libraries.append(lib)

    # set up the return value
    parts["hub"] = lib_hub
    parts["libraries"] = libraries
    parts["recreate_msg"] = recreate_msg
    parts["error_msg"] = None
    return parts


def check_fn(fn, exception_type, exception_expected=False):
    """
    Run a function and catch any exceptions that occur.
    If an exception is expected, check against the expected exception type.

    Return a pair:
       the value if the function succeeded or None, otherwise
       an error message, if appropriate, None otherwise.
    """

    exception_type_name = exception_type.__name__

    try:
        val = fn()
    except exception_type as e:
        if exception_expected:
            return None, None
        else:
            msg = (f"Unexpected {exception_type_name} raised. This test was\n"
                   f" not expected to raise an exception:\n"
                   f"   {e.__class__.__name__}: {e}\n\n"
                   f"{traceback.format_exc()}")
            return None, msg
    except Exception as e:
        if exception_expected:
            msg = (f"This test was expected to raise a {exception_type_name},\n"
                   f" but a different exception was raised instead:\n"
                   f"   {e.__class__.__name__}: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg
        else:
            msg = (f"Unexpected exception caught\n"
                   f"   {e.__class__.__name__}: {e}\n"
                   f"\nException {traceback.format_exc()}")
            return None, msg

    if exception_expected:
        msg = (f"This test was expected to raise a {exception_type_name},\n"
               "but no exception was raised.")
        return None, msg

    return val, None


# bad library parameters
# add add library with a name for the first time
# add add library with a name for the second time
# add a dup

@pytest.mark.parametrize("libs",
                         [[("libA", "1.2.3", "Armand Gamache", False)],
                          [("libA", "1.2.3", "Armand Gamache", False),
                           ("libA", "2.0.0", "Jean Guy Beauvoir", False)],
                          [("libA", "1.2.3", "Armand Gamache", False),
                           ("libB", "2.0.0", "George Dupin", False)],
                          [("libA", "1.2.3", "Armand Gamache", False),
                           ("libA", "1.2.3", "Jean Guy Beauvoir", True)],
                          [(5, "1.1.1", "x", True)],
                          [("sam", None, "x", True)],
                          [("sam", "1.1.1", False, True)],
                          [("sam", "1.1", "x", True)],
                          [("sam", "1.", "x", True)],
                          [("sam", "1.1.-1", "x", True)],
                          ])
def test_register_library(libs):
    parts = add_libraries_to_hub(libs)
    recreate_msg = parts["recreate_msg"]
    if not parts["error_msg"] is None:
        pytest.fail("\n" + parts["error_msg"] + recreate_msg)

    lib_hub = parts["hub"]
    # check that the libraries were added
    for i, (lib_name, lib_ver, reg_by, exception_expected) in enumerate(libs):
        if not exception_expected:
            # should fail, if the add succeeded.
            recreate_msg += gen_reg_lib("lib_hub", f"lib{i}", lib_name, lib_ver, reg_by, True)
            lib, error_msg = check_fn(lambda : lib_hub.register_library(lib_name, lib_ver, reg_by),
                                      hub.LibraryHubException,
                                      True)
            if error_msg:
                pytest.fail("\n" + error_msg + recreate_msg)


def get_lib_id(lib):
    try:
        lib_name = lib.get_name()
    except Exception:
        lib_name = "UNKNOWN"

    try:
        lib_version = lib.get_version()
    except Exception:
        lib_version = "UNKNOWN"

    return lib_name, lib_version




@pytest.mark.parametrize("libs, gets",
                         [([("libA", "1.2.3", "Armand Gamache", False)],
                           [("libA", "1.2.3", False, 0)]),    # find one

                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False)],
                           [("libA", "1.2.3", False, 0),
                            ("libA", "1.2.4", False, 1)]),     # Check exact matches multiple versioon of A

                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False),
                            ("libA", "2.1.5", "Armand Gamache", False),
                            ("libA", "2.1.9", "Armand Gamache", False),
                            ("libA", "2.1.0", "Armand Gamache", False),
                            ("libA", "2.2.4", "Armand Gamache", False),
                            ("libA", "2.4.2", "Armand Gamache", False),
                            ("libA", "3.1.5", "Armand Gamache", False)],

                           [("libA", "~2.1.5", False, 3)]),   # Check ~

                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False),
                            ("libA", "2.1.5", "Armand Gamache", False),
                            ("libA", "2.1.9", "Armand Gamache", False),
                            ("libA", "2.1.0", "Armand Gamache", False),
                            ("libA", "2.2.4", "Armand Gamache", False),
                            ("libA", "2.4.2", "Armand Gamache", False),
                            ("libA", "3.1.5", "Armand Gamache", False)],

                           [("libA", "^2.1.0", False, 6)]),   # check ^


                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False),
                            ("libA", "2.1.5", "Armand Gamache", False),
                            ("libA", "2.1.9", "Armand Gamache", False),
                            ("libA", "2.1.0", "Armand Gamache", False),
                            ("libA", "2.2.4", "Armand Gamache", False),
                            ("libA", "2.4.2", "Armand Gamache", False),
                            ("libA", "3.1.5", "Armand Gamache", False)],

                           [("libA", "+2.1.0", False, 7)]),     # check +

                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False),
                            ("libA", "2.1.5", "Armand Gamache", False),
                            ("libA", "2.1.9", "Armand Gamache", False),
                            ("libA", "2.1.0", "Armand Gamache", False),
                            ("libA", "2.2.4", "Armand Gamache", False),
                            ("libA", "2.4.2", "Armand Gamache", False),
                            ("libA", "3.1.5", "Armand Gamache", False)],

                           [("libA", "4.0.0", False, None)]),   # No libraries exist with the exact verion

                          ([("libA", "1.2.3", "Armand Gamache", False),
                            ("libA", "1.2.4", "Armand Gamache", False),
                            ("libA", "2.1.5", "Armand Gamache", False),
                            ("libA", "2.1.9", "Armand Gamache", False),
                            ("libA", "2.1.0", "Armand Gamache", False),
                            ("libA", "2.2.4", "Armand Gamache", False),
                            ("libA", "2.4.2", "Armand Gamache", False),
                            ("libA", "3.1.5", "Armand Gamache", False)],

                           [("libB", "1.0.0", False, None)]),   # No libB libraries exist

                          ([], [(5, "1.1.1", True, None)]),   # check bad name

                          ([], [("libA", "1.1", True, None)])  # check bad version spec.
                          ])
def test_get_library(libs, gets):
    parts = add_libraries_to_hub(libs)
    recreate_msg = parts["recreate_msg"]
    if not parts["error_msg"] is None:
        pytest.fail("\n" + parts["error_msg"] + recreate_msg)

    lib_hub = parts["hub"]
    for i, (lib_name, ver_spec_str, exception_expected, expected_idx) in enumerate(gets):
        recreate_msg += \
            f"\n  found_lib{i} = lib.hub.get_library({mk_str_parameter(lib_name)}, {mk_str_parameter(ver_spec_str)})\n"
        lib, error_msg = check_fn(lambda : lib_hub.get_library(lib_name, ver_spec_str),
                                  hub.LibraryHubException,
                                  exception_expected)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)

        if expected_idx is None:
            if lib is None:
                # done with this part of the test.
                continue
            else:
                msg = ("The get_library method returned a value other than None,\n"
                       "when None was the expected value.\n")
                pytest.fail("\n" + msg + recreate_msg)

        # if we get here, expected_idx is not None
        if lib is None:
            msg = ("The get_library method returned None,\n"
                   "when a value other than None was expected.\n")
            pytest.fail(msg + recreate_msg)


        if not isinstance(lib, library.Library):
            msg = (f"The get_library method returned a value of type {type(lib)},\n"
                   "when instance of the Library class was expected\n")
            pytest.fail("\n" + msg + recreate_msg)


        expected_lib = parts["libraries"][expected_idx]
        if not lib is expected_lib:
            actual_name, actual_version = get_lib_id(lib)

            expected_name, expected_version, _, _ = libs[expected_idx]
            msg = ("The library returned from get did not match the expected library.\n"
                   f"  Expected: {expected_name} {expected_version} (lib{expected_idx}) (repr: {repr(expected_lib)})\n"
                   f"  Actual: {actual_name} {actual_version}  (found_lib{i})  (repr: {repr(lib)})\n")
            pytest.fail("\n" + msg + recreate_msg)


@pytest.mark.parametrize("hub_filename, deps",
                         [("tests/test0.txt",
                           [(0, "libB", "1.0.0", False)]),  # Good

                          ("tests/test0.txt",
                           [(0, "libB", "1.0.0", False),
                            (0, "libX", "1.1.1", True)   # None existant dep
                            ]),

                          ("tests/test0.txt",
                           [(8, "libC", "^0.0.0", False),   # Non-stable lib can depend on non-stable dep
                            (8, "libA", "1.2.3", False),    # Non-stable lib can depend on stable dep
                            ]),

                          ("tests/test0.txt",
                           [(0, "libB", "0.0.0", True)   # stable lib, Non-stable dep
                            ]),

                          ("tests/test0.txt",
                           [(0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),
                            (0, "libE", "3.3.3", False),
                            (0, "libB", "1.0.1", True)]), # duplicate library name

                          ("tests/test0.txt",
                           [(16, "libA", "1.2.3", False),
                            (13, "libE", "~3.3.0", False),
                            (12, "libD", "2.4.3", False),
                            (9, "libF", "3.3.2", False),
                            (0, "libC", "^3.0.0", False),
                            (0, "libB", "1.0.0", True),  # Would cause a cycle
                            ]
                           )
                          ])
def test_hub_add_dependencies(hub_filename, deps):
    libs = []
    try:
        with open(hub_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                row = [r.strip() for r in row] + [False]
                libs.append(tuple(row))
    except Exception:
        pytest.fail("Attempt to read the library information from {hub_filename} failed.")

    parts = add_libraries_to_hub(libs)
    recreate_msg = parts["recreate_msg"]

    if not parts["error_msg"] is None:
        pytest.fail("\n" + parts["error_msg"] + recreate_msg)

    # if we get to here, we can swap out the
    # recreate message
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n"
                    f"  lib_hub = hub.create_hub_from_file('{hub_filename}')\n")

    lib_hub = parts["hub"]
    for lib_idx, dep_name, dep_ver_spec, exception_expected in deps:
        lib_name, lib_ver, _, _ = libs[lib_idx]

        if exception_expected:
            comment = "\n  # Exception expected from the next call to add_dependency\n"
        else:
            comment = "\n  # No exception expected from the next call to add_dependency\n"

        recreate_msg += \
            comment + \
            f"  lib_hub.add_dependency({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_ver)}, {mk_str_parameter(dep_name)}, {mk_str_parameter(dep_ver_spec)})\n"
        lib, error_msg = check_fn(lambda : lib_hub.add_dependency(lib_name, lib_ver, dep_name, dep_ver_spec),
                                  hub.LibraryHubException,
                                  exception_expected)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)


@pytest.mark.parametrize("hub_filename, deps, removes",
                         [("tests/test0.txt",
                           [(0, "libB", "1.0.1", False)],
                           [(0, "libB", "1.0.1", False)]),

                          ("tests/test0.txt",
                           [(0, "libB", "1.0.1", False)],
                           [(0, "libB", "1.0.0", True)]),  # different version of libB

                          ("tests/test0.txt",
                           [(15, "libA", "1.2.3", False),
                            (15, "libF", "~3.3.0", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libC", "^3.0.0", False),
                            ],
                           [(15, "libA", "1.2.3", False)]  # remove when there are multiple dependencies
                           ),

                          ("tests/test0.txt",
                           [(15, "libA", "1.2.3", False),
                            (15, "libF", "~3.3.0", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libC", "^3.0.0", False),
                            ],
                           [(15, "libC", "3.2.0", False)]  # remove when there are multiple dependencies
                           ),

                          ("tests/test0.txt",
                           [(15, "libA", "1.2.3", False),
                            (15, "libF", "~3.3.0", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libC", "^3.0.0", False),
                            ],
                           [(15, "libC", "3.2.0", False),  
                            (15, "libA", "1.2.3", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libF", "3.3.2", False), # remove all dependencies
                            ]
                           ),

                          ("tests/test0.txt",
                           [(15, "libA", "1.2.3", False),
                            (15, "libF", "~3.3.0", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libC", "^3.0.0", False),   # remove them all
                            ],

                           [(15, "libC", "3.2.0", False),
                            (15, "libA", "1.2.3", False),
                            (15, "libD", "2.4.3", False),
                            (15, "libF", "3.3.2", False),
                            (15, "libA", "1.2.3", True),   # already removed
                            ]
                           ),

                          ("tests/test0.txt",
                           [],  # no deps
                           [(0, "libZ", "1.0.0", True)]),  # dep does not exist
                          
                          ("tests/test0.txt",
                           [],  # no deps
                           [(0, 5, "1.0.0", True)]),  # bad dep name

                          ("tests/test0.txt",
                           [],  # no deps
                           [(0, "libZ", "1.0", True)]),  # bad dep version

                          ("tests/test0.txt",
                           [],  # no deps
                           [(-1,)]),  # lib does not exist

                          ("tests/test0.txt",
                           [],  # no deps
                           [(-2,)]),  # bad lib name

                          ("tests/test0.txt",
                           [],  # no deps
                           [(-3,)]),  # bad lib version

                          ])
def test_hub_remove_dependencies(hub_filename, deps, removes):
    libs = []
    try:
        with open(hub_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                row = [r.strip() for r in row] + [False]
                libs.append(tuple(row))
    except Exception:
        pytest.fail("Attempt to read the library information from {hub_filename} failed.")

    parts = add_libraries_to_hub(libs)
    recreate_msg = parts["recreate_msg"]
    if not parts["error_msg"] is None:
        pytest.fail("\n" + parts["error_msg"] + recreate_msg)

    # if we get to here, we can swap out the
    # recreate message
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n"
                    f"  lib_hub = hub.create_hub_from_file('{hub_filename}')\n")

    lib_hub = parts["hub"]
    
    if len(removes) == 1 and removes[0][0] < 0:
        # do bad parameter tests
        tag = removes[0][0]
        if tag == -1:
            # lib does not exist
            lib_name = "libZ"
            lib_ver = "1.1.1"
            dep_name = "libA"
            dep_ver = "1.2.3"
        elif tag == -2:
            lib_name = 5
            lib_ver = "1.1.1"
            dep_name = "libA"
            dep_ver = "1.2.3"
        elif tag == -3:
            lib_name = "libA"
            lib_ver = 5
            dep_name = "libB"
            dep_ver = "1.0.1"

        # error check
        recreate_msg += (f"  # The next call to remove dependency should raise a LibraryHubException\n"
                         f"  lib_hub.remove_dependency({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_ver)}, {mk_str_parameter(dep_name)}, {mk_str_parameter(dep_ver)})\n")
        
        lib, error_msg = check_fn(lambda : lib_hub.remove_dependency(lib_name, lib_ver, dep_name, dep_ver),
                                  hub.LibraryHubException,
                                  True)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)
        else:
            # done with special case
            return
    # regular cases...
    # add all the dependencies
    for lib_idx, dep_name, dep_ver_spec, exception_expected in deps:
        lib_name, lib_ver, _, _ = libs[lib_idx]

        recreate_msg += \
            f"  lib_hub.add_dependency({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_ver)}, {mk_str_parameter(dep_name)}, {mk_str_parameter(dep_ver_spec)})\n"
        lib, error_msg = check_fn(lambda : lib_hub.add_dependency(lib_name, lib_ver, dep_name, dep_ver_spec),
                                  hub.LibraryHubException,
                                  exception_expected)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)

    # do the removes
    for lib_idx, dep_name, dep_ver, exception_expected in removes:
        lib_name, lib_ver, _, _ = libs[lib_idx]

        recreate_msg += \
            f"  lib_hub.remove_dependency({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_ver)}, {mk_str_parameter(dep_name)}, {mk_str_parameter(dep_ver)})\n"
        lib, error_msg = check_fn(lambda : lib_hub.remove_dependency(lib_name, lib_ver, dep_name, dep_ver),
                                  hub.LibraryHubException,
                                  exception_expected)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)
        

@pytest.mark.parametrize("hub_filename, deps, level, expected_contacts, exception_expected, start",
                         [("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           0,
                           [],
                           False,
                           0
                           ),

                          ("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           1,
                           [1],
                           False,
                           0
                           ),

                          ("tests/test1.txt",
                           [(5, "libB", "1.0.1", False),  #Tree
                            (3, "libF", "3.3.2", False),
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           1,
                           [1, 2],
                           False,
                           0),

                          ("tests/test1.txt",             # Tree
                           [(5, "libB", "1.0.1", False),
                            (3, "libF", "3.3.2", False),
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           2,
                           [1, 2, 3, 4],
                           False,
                           0),


                          ("tests/test1.txt",
                           [(5, "libB", "1.0.1", False),  # Tree
                            (3, "libF", "3.3.2", False),
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           None,
                           [1, 2, 3, 4, 5, 6, 7],
                           False, 0),


                          ("tests/test1.txt",
                           [(5, "libB", "1.0.1", False), # Directed Acyclic Graph
                            (3, "libF", "3.3.2", False),
                            (4, "libF", "3.3.2", False),                            
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           2,
                           [1, 2, 3, 4, 6],
                           False,
                           0),

                          ("tests/test1.txt",
                           [(5, "libB", "1.0.1", False), # Directed Acyclic Graph
                            (3, "libF", "3.3.2", False),
                            (4, "libF", "3.3.2", False),                            
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           5,
                           [1, 2, 3, 4, 5, 6, 7],
                           False,
                           0),


                          ("tests/test1.txt",
                           [(5, "libB", "1.0.1", False), # Directed Acyclic Graph
                            (3, "libF", "3.3.2", False),
                            (4, "libF", "3.3.2", False),                            
                            (2, "libD", "2.4.3", False),
                            (2, "libE", "3.3.3", False),
                            (1, "libF", "3.3.6", False),
                            (0, "libB", "1.0.0", False),
                            (0, "libC", "3.1.5", False),                            
                            ],
                           None,
                           [1, 2, 3, 4, 5, 6, 7],
                           False,
                           0),

                          ("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           -1,
                           [],
                           True,
                           0),
                          
                          ("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           'sam',
                           [],
                           True,
                           0),


                          ("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           -2,
                           [],
                           True,
                           0),

                          ("tests/test2.txt",
                           [(0, "libB", "1.0.0", False)],
                           -3,
                           [],
                           True,
                           0),
                          

                          ])
def test_get_contacts(hub_filename, deps, level, expected_contacts, exception_expected, start):
    libs = []
    try:
        with open(hub_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                row = [r.strip() for r in row] + [False]
                libs.append(tuple(row))
    except Exception:
        pytest.fail(f"Attempt to read the library information from {hub_filename} failed.")

    parts = add_libraries_to_hub(libs)
    recreate_msg = parts["recreate_msg"]
    if not parts["error_msg"] is None:
        pytest.fail("\n" + parts["error_msg"] + recreate_msg)

    # if we get to here, we can swap out the
    # recreate message
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n"
                    f"  lib_hub = hub.create_hub_from_file('{hub_filename}')\n")

    lib_hub = parts["hub"]
    libraries = parts["libraries"]
    
    # add all the dependencies
    for lib_idx, dep_name, dep_ver_spec, dep_exception_expected in deps:
        lib_name, lib_ver, _, _ = libs[lib_idx]

        recreate_msg += \
            f"  lib_hub.add_dependency({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_ver)}, {mk_str_parameter(dep_name)}, {mk_str_parameter(dep_ver_spec)})\n"
        lib, error_msg = check_fn(lambda : lib_hub.add_dependency(lib_name, lib_ver, dep_name, dep_ver_spec),
                                  hub.LibraryHubException,
                                  dep_exception_expected)
        if error_msg:
            pytest.fail("\n" + error_msg + recreate_msg)

    # do the work
    if exception_expected:
        comment = "\n  # Exception expected from the call to get_contacts\n"
    else:
        comment = "\n  # No exception expected from the call to get_contacts\n"

    if isinstance(level, int) and level < 0:
        if level == -2:
            start_name = "LibZ"
            start_ver = "1.1.1"
            level = 0
        else:
            start_name = "LibA"
            start_ver = "1.1"
            level = 0
    else:
        start_name, start_ver, _, _ = libs[start]

    recreate_msg += \
        comment + \
        f"  lib_hub.get_contacts({mk_str_parameter(start_name)}, {mk_str_parameter(start_ver)}, {mk_str_parameter(level)})\n"
    print("Exception expected:", exception_expected)
    actual, error_msg = check_fn(lambda : lib_hub.get_contacts(start_name, start_ver, level),
                                 hub.LibraryHubException,
                                 exception_expected)

    if error_msg:
        pytest.fail("\n" + error_msg + recreate_msg)

    if exception_expected and actual is None:
        # all good
        return

    # check the result
    expected = set()
    for idx in expected_contacts:
        _, _, reg_by, _ = libs[idx]
        expected.add(reg_by)

    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg:
        pytest.fail(error_msg)
    
    
