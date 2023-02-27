"""
CMSC 14100
Winter 2023

Test code for Project #1
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
import library
import version
import version_spec

MODULE = "library"

def mk_str_parameter(x):
    return str(x) if not isinstance(x, str) else f"'{x}'"

def gen_recreate_header(libraries, include_version_spec=False):
    msg = (f"\n\nTo recreate this test in ipython3, run:\n"
           f"  import {MODULE}\n")

    if include_version_spec:
        msg += f"  import version_spec\n"

    for i, lib_info in enumerate(libraries):
        if isinstance(lib_info, tuple):
            lib_name, lib_vstr, reg_by = lib_info
            msg += f"  lib{i} = {MODULE}.Library({mk_str_parameter(lib_name)}, {mk_str_parameter(lib_vstr)}, {mk_str_parameter(reg_by)})\n"
        elif isinstance(lib_info, str):
            msg += f"  lib{i} = '{lib_info}'\n"
        else:
            msg += f"  lib{i} = {lib_info}\n"
    return msg


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



libraries_to_make = [
    ("LibA", "3.2.1", "Armand Gamache"),
    ("LibB", "2.2.10", "Sam Spade"),
    ("LibC", "4.0.1", "Barbara Havers"),
    ("LibC", "4.0.3", "Thomas Lynley"),
    ("LibD", "0.1.10", "Kurt Wallander"),
    ("LibE", "0.5.23", "Tom Mathias"),
    ("LibF", "5.1.10", "Karen Pirie"),
    ("LibG", "5.1.10", "Vera Stanhope")
]



def make_libraries(libs_args, recreate_msg):
    """
    Make the needed libraries for subsequent tests
    """
    libraries = []
    # construct the necessary library versions
    for i, (name, vstr, reg_by) in enumerate(libs_args):
        name_p = mk_str_parameter(name)
        vstr_p = mk_str_parameter(vstr)
        reg_by_p = mk_str_parameter(reg_by)        

        recreate_msg += f"  lib{i} = {MODULE}.Library({name_p}, {vstr_p}, {reg_by_p})\n"
        lib, error_msg = check_fn(lambda : library.Library(name, vstr, reg_by),
                                  library.LibraryException,
                                  False)
        # should not fail, but you never know...
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)

        libraries.append(lib)
    return libraries, recreate_msg


def add_deps_to_libs(libraries, deps_args, recreate_msg):
    # add the dependencies to the libraries
    for i, (lib_idx, dep_idx, should_fail) in enumerate(deps_args):
        lib = libraries[lib_idx]
        if should_fail:
            recreate_msg += "\n  # should raise an exception\n"
        else:
            recreate_msg += "\n  # should not raise an exception \n"
        recreate_msg += f"  lib{lib_idx}.add_dependency(lib{dep_idx})\n"
        val, error_msg = check_fn(lambda : lib.add_dependency(libraries[dep_idx]),
                                  library.LibraryException,
                                  should_fail)
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)
    # no return value needed, update the libraries in place



@pytest.mark.parametrize("lib_idx, deps, level, expected_contacts, exception_expected",
                         [(0,
                           ((0, 1, False),
                            (0, 2, False)),
                           0,
                           [],
                           False),   # no contacts for level 0

                          (0,
                           ((0, 1, False),
                            (0, 2, False)),
                           1,
                           [1, 2],
                           False),

                          (0,
                           ((0, 1, False),
                            (0, 2, False)),
                           None,
                           [1, 2],
                           False),  # same answer for both None and level 0
                          
                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           None,
                           [1, 2, 3, 6, 7],
                           False),  # all the levels
                          
                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           1,
                           [1, 2],
                           False),  # level 1

                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           2,
                           [1, 2, 6],
                           False),  # level 2

                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           3,
                           [1, 2, 6, 7],
                           False),  # level 3

                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           4,
                           [1, 2, 3, 6, 7],
                           False),  # level 4

                          (0,
                           ((7, 3, False),
                            (6, 2, False),
                            (6, 7, False),
                            (1, 6, False),
                            (0, 1, False),
                            (0, 2, False)),
                           5,
                           [1, 2, 3, 6, 7],
                           False),  # more levels than tree has

                          (0,
                           ((6, 7, False),
                            (1, 6, False),
                            (2, 6, False),
                            (0, 1, False),
                            (0, 2, False)),  # directed acyclic graph
                           None,
                           [1, 2, 6, 7],
                           False),  # all the levels

                          (0,
                           [(0, 1, False)],
                           -1, 
                           [],
                           True),  # bad level
                          
                          (0,
                           [(0, 1, False)],
                           "hello",
                           [],
                           True),  # bad level

                          (7,
                           [],
                           None,
                           [],
                           False), # no deps

                          

                         ])
def test_get_dep_contacts(lib_idx, deps, level, expected_contacts, exception_expected):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")

    print(deps)
    libraries = []
    to_make = set([lib_idx])
    for from_idx, to_idx, _ in deps:
        to_make.add(from_idx)
        to_make.add(to_idx)

    # construct the necessary library versions
    for i, (name, vstr, reg_by) in enumerate(libraries_to_make):
        if i in to_make:
            recreate_msg += f"  lib{i} = {MODULE}.Library('{name}', '{vstr}', '{reg_by}')\n"
            lib, error_msg = check_fn(lambda : library.Library(name, vstr, reg_by),
                                      library.LibraryException,
                                      False)
            # should not fail, but you never know...
            if error_msg is not None:
                pytest.fail("\n" + error_msg + recreate_msg)
        else:
            # we don't use this one, make the slot empty
            # to make the indexes work out
            lib = None
        libraries.append(lib)

    add_deps_to_libs(libraries, deps, recreate_msg)

    recreate_msg += f"  lib{lib_idx}.get_dep_contacts({mk_str_parameter(level)})\n"

    # root
    lib = libraries[lib_idx]
    actual, error_msg = check_fn(lambda :  lib.get_dep_contacts(level),
                                   library.LibraryException,
                                   exception_expected)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    if exception_expected and actual is None:
        # all good.
        return

    # check the result
    expected = set()
    for idx in expected_contacts:
        _, _, reg_by = libraries_to_make[idx]
        expected.add(reg_by)

    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if not error_msg is None:
        pytest.fail(error_msg)
    

    
