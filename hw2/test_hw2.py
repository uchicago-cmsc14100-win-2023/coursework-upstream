"""
CMSC 14100
Autumn 2022

Test code for Homework #2
"""

import os
import sys

import pytest
import test_helpers as helpers

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position
import hw2

MODULE = "hw2"

def check_result(actual, expected, recreate_msg):
    """
    Do the work of checking the result when the correctness test is
    equality.
    """
    # We expect a result is not None
    helpers.check_not_none(actual, recreate_msg)

    # We expect a result of the right type
    helpers.check_type(actual, expected, recreate_msg)

    if isinstance(expected, float):
        # The expected result is a float. Check that the actual
        # value is close enought to the expected value
        helpers.check_float_equals(actual, expected, recreate_msg)
    else:
        # We expect a result that is the same as expected
        helpers.check_equals(actual, expected, recreate_msg)

@pytest.mark.parametrize("a, x, expected",
                         [(0, 0, 0),
                          (5, 2, 12),
                          (5, 0, 0),
                          (9, 1, 10),
                          (9, -2, -20),
                          (-11, 2, -20)])
def test_add_one_and_multiply(a, x, expected):
    """
    Do a single test for Exercise 1: add_one_and_multiply
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "add_one_and_multiply",
                                            a, x)
    actual = hw2.add_one_and_multiply(a, x)
    check_result(actual, expected, recreate_msg)


@pytest.mark.parametrize("a, b, n, expected",
                         [(2, 4, 2, False),
                          (2, 7, 5, False),
                          (1, 10, 4, True),
                          (8, -8, 5, True),
                          (-8, 7, 5, False)])
def test_have_different_remainders(a, b, n, expected):
    """
    Do a single test for Exercise 2: have_different_remainders
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "have_different_remainders",
                                            a, b, n)
    actual = hw2.have_different_remainders(a, b, n)
    check_result(actual, expected, recreate_msg)



@pytest.mark.parametrize("amount, principle, rate, expected",
                         [(11937.5, 10000.0, 3.875, 5.0),
                          (10193.75, 10000.0, 3.875, 0.5),
                          (1250.0, 1000.0, 6.25, 4.0),
                          (1332.0, 750.0, 7.76, 10.0),
                          (1999.5, 1500.0, 7.4, 4.5)])
def test_compute_time(amount, principle, rate, expected):
    """
    Do a single test for Exercise 3: compute_time
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "compute_time",
                                            amount, principle, rate)
    actual = hw2.compute_time(amount, principle, rate)
    check_result(actual, expected, recreate_msg)


##### Speeding test cases #####

@pytest.mark.parametrize("weight,expected",
                         [(hw2.TRUCK_WEIGHT_THRESHOLD + 500, True),
                          (hw2.TRUCK_WEIGHT_THRESHOLD, True),
                          (hw2.TRUCK_WEIGHT_THRESHOLD - 1, False),
                          (1000, False)])
def test_is_truck(weight, expected):
    """
    Do a single test for Exercise 4: is_truck
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "is_truck", weight)
    actual = hw2.is_truck(weight)
    check_result(actual, expected, recreate_msg)

@pytest.mark.parametrize("speed,expected",
                         [(hw2.URBAN_SPEED_LIMIT, False),
                          (hw2.URBAN_SPEED_LIMIT-1, False),
                          (hw2.URBAN_SPEED_LIMIT+1, True)])

def test_urban_is_speeding(speed, expected):
    """
    Do a single test for Exercise 5: urban_is_speeding
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "urban_is_speeding", speed)
    actual = hw2.urban_is_speeding(speed)
    check_result(actual, expected, recreate_msg)


rural_speeding_tests = \
    [ # Truck above the weight limit
      # above truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT+1, True),
      # at truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT, False),
      # below truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT-1, False),
      # Truck at the weight limit
      # Above truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT+1, True),
      # At truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT, False),
      # Below truck speed limit
      (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT-1, False),
      # car
      # Above car speed limit
      (1000, hw2.RURAL_CAR_SPEED_LIMIT+1, True),     
      # At car speed limit
      (1000, hw2.RURAL_CAR_SPEED_LIMIT, False),    
      # At truck speed limit, below car speed limit
      (1000, hw2.RURAL_TRUCK_SPEED_LIMIT, False)]

@pytest.mark.parametrize("weight, speed, expected", rural_speeding_tests)
def test_rural_is_speeding(weight, speed, expected):
    """
    Do a single test for Exercise 5: rural_is_speeding
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "rural_is_speeding",
                                            weight, speed)
    actual = hw2.rural_is_speeding(weight, speed)
    check_result(actual, expected, recreate_msg)


# Tests for trucks
truck_tests = \
    [# Truck above the weight limit
     # Above rural truck limit in a rural setting
     (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT + 10, False, False),
     # Above rural speed limit in a rural setting
     (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT + 10, True, False),

     # Truck above weight limit
     # At rural speed limit in a rural setting
     (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT, False, True),
     # At rurl speed limit in an urban setting
     (hw2.TRUCK_WEIGHT_THRESHOLD + 500, hw2.RURAL_TRUCK_SPEED_LIMIT, True, False),

     # Truck at weight limit
     # Above rural speed limit in a rural setting
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT + 10, False, False),
     # Above rural speed limit in an urban setting
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT + 10, True, False),

     # At rural speed limit in a rural setting
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT, False, True),
     # At rural speed limit in an urban setting
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.RURAL_TRUCK_SPEED_LIMIT, True, False),

     # Below urban speed limit
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.URBAN_SPEED_LIMIT-1, True, True),
     # At urban speed limit
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.URBAN_SPEED_LIMIT, True, True),
     # Above urban speed limit
     (hw2.TRUCK_WEIGHT_THRESHOLD, hw2.URBAN_SPEED_LIMIT+1, True, False)]



# Tests for cars (aka, non-trucks)
car_tests = \
    [(1000, hw2.RURAL_CAR_SPEED_LIMIT+10, False, False), # Above rural car limit
     (1000, hw2.RURAL_CAR_SPEED_LIMIT+10, True, False),

     # At rural car speed limit
     # In a rural setting
     (1000, hw2.RURAL_CAR_SPEED_LIMIT, False, True),
     # In an urban setting
     (1000, hw2.RURAL_CAR_SPEED_LIMIT, True, False),    # but is speeding in an urban setting

     # Below rural speed limit, above urban limit
     # In a rural setting
     (1000, hw2.RURAL_CAR_SPEED_LIMIT - 10, False, True),
     # In an urban setting
     (1000, hw2.RURAL_CAR_SPEED_LIMIT - 10, True, False),


     # Urban setting
     # Below urban limit
     (1000, hw2.URBAN_SPEED_LIMIT - 1, True, True),
     # At urban limit
     (1000, hw2.URBAN_SPEED_LIMIT, True, True),
     # Above urban limit
     (1000, hw2.URBAN_SPEED_LIMIT + 1, True, False)]


@pytest.mark.parametrize("weight, speed, is_urban, expected",
                         truck_tests + car_tests)
def test_is_not_speeding(weight, speed, is_urban, expected):
    """
    Do a single test for Exercise 6: is_not_speeding
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "is_not_speeding",
                                            weight, speed, is_urban)
    actual = hw2.is_not_speeding(weight, speed, is_urban)
    check_result(actual, expected, recreate_msg)
