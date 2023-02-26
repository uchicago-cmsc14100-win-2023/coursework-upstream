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


@pytest.mark.parametrize("name, vstr, reg_by, exception_expected",
                         [ ("LibA", "3.10.200", "Sam Spade", False),
                           ("LibB", "37654321.0.2009999999999", "Sam Spade", False),
                           ("LibC", "3.10", "Armand Gamache", True),
                           ("LibD", "3.10.", "Karen Pirie", True),
                           ("LibE", "1000.", "Jimmy Perez", True),
                           ("LibF", "1000", "Vera Stanhope", True),
                           ("LibG", "3.3.-1", "Barbara Havers", True),
                           (5, "3.3.3", "x", True),
                           (5, 5, 5, True),                           
                          ])
def test_library_construction(name, vstr, reg_by, exception_expected):
    recreate_msg = gen_recreate_header([(name, vstr, reg_by)])

    lib0, error_msg = check_fn(lambda : library.Library(name, vstr, reg_by),
                               library.LibraryException, exception_expected)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)


@pytest.mark.parametrize("name, vstr, reg_by, expected",
                         [("LibA", "0.10.2000", "Sam Spade", False),
                          ("LibB", "9.1001.2000", "Sam Spade", True),
                          ("LibC", "9.0.2000", "Sam Spade", True),
                          ("LibD", "9.0.0", "Sam Spade", True),                                                    
                          ])
def test_library_is_stable(name, vstr, reg_by, expected):
    recreate_msg = gen_recreate_header([(name, vstr, reg_by)]) + \
        f"  expected = {expected}\n" + \
        f"  actual = lib0.is_stable()\n"

    lib0, error_msg = check_fn(lambda : library.Library(name, vstr, reg_by),
                               library.LibraryException,
                               False)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    try:
        actual = lib0.is_stable()
    except Exception as e:
        error_msg = (f"Unexpected exception caught during call to is_stable:\n"
                     f"   {e.__class__.__name__}: {e}\n"
                     f"\nException {traceback.format_exc()}")
        pytest.fail("\n" + error_msg + recreate_msg)

    error_msg = helpers.check_result(actual, expected, recreate_msg)
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
                          (3, (900, 2000, 3000), None),   # generate an exception
                          (None, (900, 2000, 3000), None)   # generate an exception                          
                          ])
def test_satisfies_version_req(vs_str, v_tuple, expected):
    name = "LibA"
    vstr = ".".join([str(r) for r in v_tuple])
    reg_by = "Sam Spade"
    
    # set up recreation message
    if isinstance(vs_str, str):
        ver_spec_str = f"version_spec.VersionSpecification('{vs_str}')"
    else:
        ver_spec_str = str(vs_str)
    recreate_msg = gen_recreate_header([(name, vstr, reg_by)], True) + \
        f"  ver_spec = {ver_spec_str}\n" + \
        f"  expected = {expected}\n" + \
        f"  actual = lib0.satisfies_version_req(ver_spec)\n"


    # set up the version specification
    if isinstance(vs_str, str):
        # construct the version specification
        ver_spec, error_msg = check_fn(lambda : version_spec.VersionSpecification(vs_str),
                                       version_spec.VersionSpecException,
                                       False)
        # should not fail, but you never know...
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)
        exception_expected = False
    else:
        # not a version string...intended to generate an exception
        ver_spec = vs_str
        exception_expected = True    


    # construct the library version
    lib0, error_msg = check_fn(lambda : library.Library(name, vstr, reg_by),
                               library.LibraryException,
                               False)
    # should not fail, but you never know...
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)
    
    actual, error_msg = check_fn(lambda : lib0.satisfies_version_req(ver_spec),
                                 library.LibraryException,
                                 exception_expected)

    if exception_expected and actual is None and error_msg is None:
        return

    if actual is None and error_msg:
        pytest.fail(error_msg + "\n" + recreate_msg)

    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)


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

            
        
COMES_BEFORE = -1
EQUALS = 0
COMES_AFTER = 1
FAILURE = 2

ilv_tests = [
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


def is_later_helper(l0_parts, l1_parts, expected, recreate_msg):
    # construct the necessary instance for lib0
    lib0, error_msg = check_fn(lambda : library.Library(*l0_parts),
                               library.LibraryException,
                               False)
    if error_msg is not None:
        return "\n" + error_msg + recreate_msg
    
    if isinstance(l1_parts, tuple):
        # construct the necessary instance for lib1
        lib1, error_msg = check_fn(lambda : library.Library(*l1_parts),
                                   library.LibraryException,
                                   False)
        if error_msg is not None:
            return "\n" + error_msg + recreate_msg

        # are the names the different?
        exception_expected = l0_parts[0] != l1_parts[0]
    else:
        # just copy over the bad value
        lib1 = l1_parts
        exception_expected = True
            
    actual, error_msg = check_fn(lambda : lib0.is_later_version(lib1),
                                 library.LibraryException,
                                 exception_expected)
    if exception_expected and actual is None and error_msg is None:
        return None
    
    if error_msg is not None:
        return "\n" + error_msg + recreate_msg        

    # check the result
    return helpers.check_result(actual, expected, recreate_msg)


@pytest.mark.parametrize("l0_parts, l1_parts, relationship",
                         ilv_tests)
def test_library_is_later_version(l0_parts, l1_parts, relationship):
    name = "libA"
    reg_by = "Sam Spade"
    lib0 = (name, ".".join([str(r) for r in l0_parts]), reg_by)
    lib1 = (name, ".".join([str(r) for r in l1_parts]), reg_by)            
    recreate_msg = gen_recreate_header([lib0, lib1]) + f"  lib0.is_later_version(lib1)"

    # lib0 comes after lib1
    expected = (relationship == COMES_AFTER)
    error_msg = is_later_helper(lib0, lib1, expected,
                                recreate_msg)
    if error_msg is not None:
        pytest.fail(error_msg)

        
@pytest.mark.parametrize("lib0, lib1",
                         [(("libA", "1.1.1", "Sam Spade"), ("libB", "1.1.1", "Sam Spade")),
                          (("libA", "1.1.1", "Sam Space"), 5),
                          (("libA", "1.1.1", "Sam Space"), None),
                          ])
def test_library_is_later_errors(lib0, lib1):
    recreate_msg = gen_recreate_header([lib0, lib1]) + \
        f"  lib0.is_later_version(lib1)    # should raise an exception \n"

    error_msg = is_later_helper(lib0, lib1, None, recreate_msg)
    if error_msg is not None:
        pytest.fail("\n" + error_msg + recreate_msg)

    

    
        

add_dep_tests = [
    (0, (1,), []),
    (7, (0, 1, 2), []),    # Add multiple libraries

    (4, (0, 1, 2), []),    # unstable library can depend on stable libraries
    (4, (0, 1, 2, 5), []), # unstable library can depend on both stable and unstable libraries    

    (0, (1, 1), [1]),      # repeat the same library
    (0, (1, 2, 3), [2]),   # repeat the same name
    (0, (1, 2, 4), [2]),   # stable library cannot depend on an unstable library
    (0, (1, 2, 4, 6), [2]),   # can still add after failure

    (7, (0, 1, 2, 0, 1, 2), [3, 4, 5]), # checking that multiple libraries were actually added.
    
]
@pytest.mark.parametrize("lib_idx, dep_idxs, exception_expected_idxs",
                         add_dep_tests)
def test_add_dependency(lib_idx, dep_idxs, exception_expected_idxs):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")

    libraries = []
    # construct the necessary library versions
    to_make = set([lib_idx]) | set(dep_idxs)
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

    lib = libraries[lib_idx]
    for i, dep_idx in enumerate(dep_idxs):
        # is this specific occurrence of dep_idx expected to fail
        should_fail = i in exception_expected_idxs

        recreate_msg += f"  lib{lib_idx}.add_dependency(lib{dep_idx})"
        if should_fail:
            recreate_msg += "    # should raise an exception\n"
        else:
            recreate_msg += "\n"

        val, error_msg = check_fn(lambda : lib.add_dependency(libraries[dep_idx]),
                                  library.LibraryException,
                                  should_fail)
                                  
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)


remove_dep_tests = [
    # (lib, (to add), (to remove), (idx of removes that should cause exceptions))
    (0, (1,), [1], []),              # add one, remove one
    (0, (1, 2, 6), [2], []),         # remove something other than the first
    (0, (1, 2, 6), [2, 6, 1], []),   # remove them all

    (0, [1, 2, 6], [2, 2], [1]),     # the second one should fail
    (0, [1, 2, 6], [2, 2, 6], [1]),  # the second one should fail, but not the first or the third
    (6, [2], [3], [0]),              # try to remove a library of the same name, but a different version
    (6, [], [1], [0]),               # try to remove a library when there are no dependencies.
]            
@pytest.mark.parametrize("lib_idx, dep_idxs, remove_idxs, exception_expected_idxs",
                         remove_dep_tests)
def test_remove_dependency(lib_idx, dep_idxs, remove_idxs, exception_expected_idxs):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")

    libraries = []
    # construct the library versions needed
    to_make = set([lib_idx]) | set(dep_idxs)
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


    # make the dependencies, none should fail
    lib = libraries[lib_idx]
    for i, dep_idx in enumerate(dep_idxs):
        recreate_msg += f"  lib{lib_idx}.add_dependency(lib{dep_idx}) \n"
        val, error_msg = check_fn(lambda : lib.add_dependency(libraries[dep_idx]),
                                  library.LibraryException,
                                  False)
        # should not fail
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)


    # now try to do the removes.
    for i, dep_idx in enumerate(remove_idxs):
        should_fail = i in exception_expected_idxs
        
        recreate_msg += f"  lib{lib_idx}.remove_dependency(lib{dep_idx})"
        if should_fail:
            recreate_msg += "    # should raise an exception\n"
        else:
            recreate_msg += "\n"
        
        val, error_msg = check_fn(lambda : lib.remove_dependency(libraries[dep_idx]),
                                  library.LibraryException,
                                  should_fail)
                                  
        # should not fail
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)

    # now try add the removed items, all the adds should succeed.
    added_already = []
    for i, dep_idx in enumerate(remove_idxs):
        should_fail = i in exception_expected_idxs
        if should_fail:
            # skip this one: the remove did not succeed, so
            # we don't need to check the add
            continue
        
        if dep_idx in added_already:
            continue

        added_already.append(dep_idx)

        recreate_msg += f"  lib{lib_idx}.add_dependency(lib{dep_idx})\n"
        val, error_msg = check_fn(lambda : lib.add_dependency(libraries[dep_idx]),
                                  library.LibraryException,
                                  False)
                                  
        # the add will succeed, if the remove was done properly
        if error_msg is not None:
            pytest.fail("\n" + error_msg + recreate_msg)
            

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


@pytest.mark.parametrize("libs_args, deps_args",
                         [
                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0",  "Sam Spade")], 
                              [(0, 1, False)]),   # valid depedency

                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libA", "1.0.0", "Armand Gamache")], 
                              [(0, 1, True)]),   # Cannot depend on a library of the same name

                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0", "Sam Spade"),
                               ("libC", "3.1.5", "Barbara Havers"),
                               ("libD", "2.4.3", "Thomas Lynley"),
                               ("libE", "3.3.3", "Kurt Wallander"), 
                               ], 
                              [(3, 1, False),
                               (1, 3, True),    # cycle: 1 -> 3 -> 1
                               (2, 4, False),
                               (0, 2, False),
                               (0, 1, False),
                               ]),

                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0", "Sam Spade"),
                               ("libC", "3.1.5", "Barbara Havers"),
                               ("libD", "2.4.3", "Thomas Lynley")], 
                              [(3, 0, False),
                               (2, 3, False),
                               (1, 2, False),
                               (0, 2, True)]),   # cycle 0 -> 2 -> 3 -> 0

                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0", "Sam Spade"),
                               ("libC", "3.1.5", "Barbara Havers"),
                               ("libD", "2.4.3", "Thomas Lynley"),
                               ("libE", "3.3.3", "Kurt Wallander"), 
                               ], 
                              [(4, 1, False),
                               (3, 4, False),
                               (1, 3, True),   # cycle 1 -> 3 -> 4 -> 1
                               (0, 2, False),  # OK to add after the cycle fails
                               (0, 1, False),
                               ]),

                             
                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0", "Sam Spade"),
                               ("libC", "3.1.5", "Barbara Havers"),
                               ("libD", "2.4.3", "Thomas Lynley"),
                               ("libE", "3.3.3", "Kurt Wallander"), 
                               ], 
                              [(3, 4, False),
                               (2, 4, False),
                               (1, 3, False),
                               (0, 2, False),
                               (0, 1, False),  # ALL OK
                               ]),

                             ([("libA", "1.2.3", "Armand Gamache"), 
                               ("libB", "1.0.0", "Sam Spade"),
                               ("libC", "3.1.5", "Barbara Havers"),
                               ("libD", "2.4.3", "Thomas Lynley"),
                               ("libE", "3.3.3", "Kurt Wallander"), 
                               ], 
                              [(4, 2, False),
                               (3, 4, False),
                               (1, 3, False),
                               (0, 1, False),  # 0 -> 1 -> 3 OK
                               (2, 3, True),  # cycle: 2 -> 3 -> 4 -> 2 
                               ]),

                         ])                         
def test_add_cycles_dependency(libs_args, deps_args):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")

    libraries, recreate_msg = make_libraries(libs_args, recreate_msg)
    add_deps_to_libs(libraries, deps_args, recreate_msg)

            

@pytest.mark.parametrize("lib",
                         [("libA", "1.2.3", "Armand Gamache")
                          ])
def test_get_lib_name(lib):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")
    
    libraries, recreate_msg = make_libraries([lib], recreate_msg)
    try:
        actual = libraries[0].get_name()
    except Exception as e:
        error_msg = (f"Unexpected exception caught during call to get_name:\n"
                     f"   {e.__class__.__name__}: {e}\n"
                     f"\nException {traceback.format_exc()}")
        pytest.fail("\n" + error_msg + recreate_msg)

    recreate_msg += "  lib0.get_name()\n"
    
    # check the result
    expected = lib[0]
    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if not error_msg is None:
        pytest.fail("\n" + error_msg)

        
@pytest.mark.parametrize("lib, expected",
                         [(("libA", "1.2.3", "Armand Gamache"), (1, 2, 3)),
                          (("libA", "999.2000.3", "Armand Gamache"), (999, 2000, 3)),
                          ])
def test_get_lib_version(lib, expected):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")
    
    libraries, recreate_msg = make_libraries([lib], recreate_msg)
    try:
        actual = libraries[0].get_version()
    except Exception as e:
        error_msg = (f"Unexpected exception caught during call to get_version:\n"
                     f"   {e.__class__.__name__}: {e}\n"
                     f"\nException {traceback.format_exc()}")
        pytest.fail("\n" + error_msg + recreate_msg)

    recreate_msg += "  lib0.get_version()\n"

    # check the result
    expected = version.Version(*expected)
    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if not error_msg is None:
        pytest.fail("\n" + error_msg)


@pytest.mark.parametrize("lib",
                         [("libA", "1.2.3", "Armand Gamache")
                          ])
def test_get_lib_registered_by(lib):
    recreate_msg = (f"\n\nTo recreate this test in ipython3, run:\n"
                    f"  import {MODULE}\n")
    
    libraries, recreate_msg = make_libraries([lib], recreate_msg)
    try:
        actual = libraries[0].get_registered_by()
    except Exception as e:
        error_msg = (f"Unexpected exception caught during call to get_registered_by:\n"
                     f"   {e.__class__.__name__}: {e}\n"
                     f"\nException {traceback.format_exc()}")
        pytest.fail("\n" + error_msg + recreate_msg)

    recreate_msg += "  lib0.get_registered_by()\n"
    
    # check the result
    expected = lib[2]
    error_msg = helpers.check_result(actual, expected, recreate_msg)
    if not error_msg is None:
        pytest.fail("\n" + error_msg)
        

    
