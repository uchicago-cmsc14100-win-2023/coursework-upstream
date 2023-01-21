"""
CMSC 14100
Autumn 2022

Test code for Homework #4
"""

import copy
import json
import os
import sys

import random
import pytest
import test_helpers as helpers


# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position
import hw4

MODULE = "hw4"
EMPTY = hw4.EMPTY

long_tests = json.load(open("tests/long_tests.json"))


fit_tests = [
    ([], 10, 0),
    ([10], 10, 1),
    ([5], 10, 1),
    ([10], 5, 0),
    ([10, 5], 12, 1),
    ([1, 1, 2, 3, 4, 5], 16, 6)
] + long_tests["fit"]

@pytest.mark.timeout(60)
@pytest.mark.parametrize("vals, target, expected", fit_tests)
def test_how_many_fit(vals, target, expected):
    """
    Do a single test for Exercise 1: how_many_fit
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "how_many_fit", vals, target)
    vals_copy = vals[:]
    actual = hw4.how_many_fit(vals_copy, target)

    # verify that the function did not modify the list input
    helpers.check_list_unmodified("vals", vals, vals_copy, recreate_msg)
    
    # Check that the actual result matches the expected result
    helpers.check_result(actual, expected, recreate_msg)
    

all_group_names = [f"Group-{n}" for n in ["A", "B", "C", "D", "E", "F"]]

passenger_tests = [
    ([], [], []),
    (["Group-A"], [1], ["Group-A-1"]),
    (["Group-A"], [3], ["Group-A-1", "Group-A-2", "Group-A-3"]),
    (["Group-A", "Group-B", "Group-C", "Group-D","Group-E", "Group-F"],
     [1, 1, 2, 3, 4, 5],
     ["Group-A-1", "Group-B-1", "Group-C-1", "Group-C-2", "Group-D-1",
      "Group-D-2", "Group-D-3", "Group-E-1", "Group-E-2", "Group-E-3",
      "Group-E-4", "Group-F-1", "Group-F-2", "Group-F-3", "Group-F-4",
      "Group-F-5"])
] + long_tests["passengers"]

@pytest.mark.timeout(60)
@pytest.mark.parametrize("names, sizes, expected", passenger_tests)
def test_gen_passengers(names, sizes, expected):
    """
    Do a single test for Exercise 2: gen_passengers
    """
    
    recreate_msg = helpers.gen_recreate_msg(MODULE, "gen_passengers", names, sizes)

    names_copy = names[:]     
    sizes_copy = sizes[:]

    actual = hw4.gen_passengers(names_copy, sizes_copy)

    # verify that the function did not modify the list inputs
    helpers.check_list_unmodified("names", names, names_copy, recreate_msg)
    helpers.check_list_unmodified("sizes", sizes, sizes_copy, recreate_msg)

    # We expect a result is not None
    helpers.check_not_none(actual, recreate_msg)

    # Check that the actual result matches the expected result
    helpers.check_1D_list(actual, expected, "list[str]", recreate_msg)    


def check_bus(actual, expected, recreate_msg, extra_str=""):
    """
    Compare an actual and expected bus data structure.
    """

    # We expect a result is not None
    helpers.check_not_none(actual, recreate_msg)

    if actual == expected:
        return

    msg = (f"\n\n{extra_str}The function returned a value for the bus of the wrong type.\n"
           f"  Expected type of the bus: list[str] \n")
    actual_type = type(actual)
    msg2 = f"  Actual type of the bus: {actual_type.__name__}\n"

    assert isinstance(actual, list), msg + msg2 + recreate_msg

    helpers.check_length(actual, expected, recreate_msg, "of the bus")

    msg3 = (f"\n\n{extra_str}The type of the actual value is incorrect.\n"
            "  The actual value at index {} has type {}.\n"
            "  The expected type is {}.\n")

    msg4 = (f"\n\n{extra_str}The values do not match:\n"
            "  The actual value at index {} is {}\n"
            "  The expected value is {}\n")

    for i, (actual_val, expected_val) in enumerate(zip(actual, expected)):
        assert isinstance(actual_val, type(expected_val)), \
            msg3.format(i, type(actual_val).__name__, type(expected_val).__name__) \
              + recreate_msg

        # Actual and expected values known to be strings.
        actual_val_str = '"' + actual_val + '"'
        expected_val_str = '"' + expected_val + '"'
        assert actual_val == expected_val, \
            msg4.format(i, actual_val_str, expected_val_str) + recreate_msg
        


fill_bus_tests = [
    (all_group_names[:1], [1], (1, 1), ["Group-A-1"]),
    (all_group_names[:1], [1], (1, 3), ["Group-A-1,Empty,Empty"]),
    (all_group_names[:1], [1], (2, 1), ["Group-A-1", "Empty"]),
    (all_group_names[:1], [1], (3, 3), ["Group-A-1,Empty,Empty",
                                        "Empty,Empty,Empty",
                                        "Empty,Empty,Empty"]),                                        
    (all_group_names[:2], [2, 2], (4, 1), ["Group-A-1","Group-A-2","Group-B-1","Group-B-2"]),
    (all_group_names[:2], [2, 2], (1, 4), ["Group-A-1,Group-A-2,Group-B-1,Group-B-2"]),
    (all_group_names[:2], [2, 2], (2, 2), ["Group-A-1,Group-A-2", "Group-B-1,Group-B-2"]),
    (all_group_names[:2], [2, 2], (3, 5),
     ["Group-A-1,Group-A-2,Group-B-1,Group-B-2,Empty",
      "Empty,Empty,Empty,Empty,Empty",
      "Empty,Empty,Empty,Empty,Empty",]),      
    (all_group_names[:4], [2, 2, 1, 3], (3, 3),
     ["Group-A-1,Group-A-2,Group-B-1",
      "Group-B-2,Group-C-1,Group-D-1",
      "Group-D-2,Group-D-3,Empty"]),
    (all_group_names[:4], [10, 5, 4, 2], (7, 3),
     ["Group-A-1,Group-A-2,Group-A-3",
      "Group-A-4,Group-A-5,Group-A-6",
      "Group-A-7,Group-A-8,Group-A-9",
      "Group-A-10,Group-B-1,Group-B-2",
      "Group-B-3,Group-B-4,Group-B-5",
      "Group-C-1,Group-C-2,Group-C-3",
      "Group-C-4,Group-D-1,Group-D-2"])
    ] + long_tests["fill"]
@pytest.mark.timeout(60)
@pytest.mark.parametrize("names, sizes, bus_config, expected", fill_bus_tests)
def test_fill_bus(names, sizes, bus_config, expected):
    """
    Do a single test for Exercise 4: fill_bus
    """
    
    recreate_msg = helpers.gen_recreate_msg(MODULE, "fill_bus", names, sizes, bus_config)

    names_copy = names[:]
    sizes_copy = sizes[:]

    actual = hw4.fill_bus(names_copy, sizes_copy, bus_config)

    # verify that the function did not modify the list inputs
    helpers.check_list_unmodified("names", names, names_copy, recreate_msg)
    helpers.check_list_unmodified("sizes", sizes, sizes_copy, recreate_msg)    
    
    check_bus(actual, expected, recreate_msg)

    
mk_fleet_tests = \
    [(['Group-A'], [1], (1, 1), [['Group-A-1']]),
     (['Group-A'], [1], (1, 3), [['Group-A-1,Empty,Empty']]),
     (['Group-A'], [1], (2, 1), [['Group-A-1', 'Empty']]),
     (['Group-A'],
      [1],
      (3, 3),
      [['Group-A-1,Empty,Empty', 'Empty,Empty,Empty', 'Empty,Empty,Empty']]),
     (['Group-A', 'Group-B'],
      [2, 2],
      (4, 1),
      [['Group-A-1', 'Group-A-2', 'Group-B-1', 'Group-B-2']]),
     (['Group-A', 'Group-B'],
      [2, 2],
      (1, 4),
      [['Group-A-1,Group-A-2,Group-B-1,Group-B-2']]),
     (['Group-A', 'Group-B'],
      [2, 2],
      (2, 2),
      [['Group-A-1,Group-A-2', 'Group-B-1,Group-B-2']]),
     (['Group-A', 'Group-B'],
      [2, 2],
      (3, 5),
      [['Group-A-1,Group-A-2,Group-B-1,Group-B-2,Empty',
        'Empty,Empty,Empty,Empty,Empty',
        'Empty,Empty,Empty,Empty,Empty']]),
     (['Group-A', 'Group-B', 'Group-C', 'Group-D'],
      [2, 2, 1, 3],
      (3, 3),
      [['Group-A-1,Group-A-2,Group-B-1',
        'Group-B-2,Group-C-1,Group-D-1',
        'Group-D-2,Group-D-3,Empty']]),
     (['Group-A', 'Group-B', 'Group-C', 'Group-D'],
      [10, 5, 4, 2],
      (7, 3),
      [['Group-A-1,Group-A-2,Group-A-3',
        'Group-A-4,Group-A-5,Group-A-6',
        'Group-A-7,Group-A-8,Group-A-9',
        'Group-A-10,Group-B-1,Group-B-2',
        'Group-B-3,Group-B-4,Group-B-5',
        'Group-C-1,Group-C-2,Group-C-3',
        'Group-C-4,Group-D-1,Group-D-2']]),
     (["Mets","Cubs", "Giants", 'Yankees', 'Dodgers', 'Phillies', 'Orioles'],
      [6, 1, 1, 9, 1, 3, 4],
      (3, 3),
      [['Mets-1,Mets-2,Mets-3',
        'Mets-4,Mets-5,Mets-6',
        'Cubs-1,Giants-1,Empty'],
       ['Yankees-1,Yankees-2,Yankees-3',
        'Yankees-4,Yankees-5,Yankees-6',
        'Yankees-7,Yankees-8,Yankees-9'],
       ['Dodgers-1,Phillies-1,Phillies-2',
        'Phillies-3,Orioles-1,Orioles-2',
        'Orioles-3,Orioles-4,Empty']]),
     (["Mets","Cubs", "Giants", 'Yankees', 'Dodgers', 'Phillies', 'Orioles'],
      [6, 1, 1, 9, 1, 3, 4],
      (10, 2),
      [['Mets-1,Mets-2',
        'Mets-3,Mets-4',
        'Mets-5,Mets-6',
        'Cubs-1,Giants-1',
        'Yankees-1,Yankees-2',
        'Yankees-3,Yankees-4',
        'Yankees-5,Yankees-6',
        'Yankees-7,Yankees-8',
        'Yankees-9,Dodgers-1',
        'Empty,Empty'],
       ['Phillies-1,Phillies-2',
        'Phillies-3,Orioles-1',
        'Orioles-2,Orioles-3',
        'Orioles-4,Empty',
        'Empty,Empty',
        'Empty,Empty',
        'Empty,Empty',
        'Empty,Empty',
        'Empty,Empty',
        'Empty,Empty']])] + long_tests["fleet"]
      



@pytest.mark.timeout(60)
@pytest.mark.parametrize("names, sizes, bus_config, expected", mk_fleet_tests)
def test_mk_fleet(names, sizes, bus_config, expected):
    """
    Do a single test for exercise 5: mk_fleet
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "mk_fleet",
                                            names, sizes, bus_config)

    names_copy = names[:]
    sizes_copy = sizes[:]

    actual = hw4.mk_fleet(names_copy, sizes_copy, bus_config)

    # verify that the function did not modify the list inputs
    helpers.check_list_unmodified("names", names, names_copy, recreate_msg)
    helpers.check_list_unmodified("sizes", sizes, sizes_copy, recreate_msg)    

    helpers.check_not_none(actual, recreate_msg)

    helpers.check_type(actual, expected, recreate_msg, "list[list[str]]")
    helpers.check_length(actual, expected, recreate_msg, "buses")

    print(actual)
    print(expected)
    for i, (actual_val, expected_val) in enumerate(zip(actual, expected)):
        print(actual_val)
        print(expected_val)

        check_bus(actual_val, expected_val, recreate_msg,
                  f"Checking element {i} in the list of buses")
        
