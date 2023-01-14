"""
CMSC 14100
Autumn 2022

Test code for Homework #3
"""

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
import hw3

MODULE = "hw3"

TRUCK_WEIGHT_THRESHOLD = 4500

dsl_tests = \
    [ # above the truck weight limit
      ("rural",
       TRUCK_WEIGHT_THRESHOLD + 500,
       hw3.RURAL_TRUCK_SPEED_LIMIT),
      # at the truck weight limit
      ("rural",
       TRUCK_WEIGHT_THRESHOLD,
       hw3.RURAL_TRUCK_SPEED_LIMIT),
      # below the truck weight limit
      ("rural",
       TRUCK_WEIGHT_THRESHOLD - 500,
       hw3.RURAL_CAR_SPEED_LIMIT),
      # way below the truck weight limit
      ("rural",
       1000,
       hw3.RURAL_CAR_SPEED_LIMIT),
       # above the truck weight limit

      ("suburban",
       TRUCK_WEIGHT_THRESHOLD + 500,
       hw3.SUBURBAN_SPEED_LIMIT),
      # at the truck weight limit
      ("suburban",
       TRUCK_WEIGHT_THRESHOLD,
       hw3.SUBURBAN_SPEED_LIMIT),
      # below the truck weight limit
      ("suburban",
       TRUCK_WEIGHT_THRESHOLD - 500,
       hw3.SUBURBAN_SPEED_LIMIT),
      # way below the truck weight limit
      ("suburban",
       1000,
       hw3.SUBURBAN_SPEED_LIMIT),

       # above the truck weight limit
      ("urban",
       TRUCK_WEIGHT_THRESHOLD + 500,
       hw3.URBAN_SPEED_LIMIT),
      # at the truck weight limit
      ("urban",
       TRUCK_WEIGHT_THRESHOLD,
       hw3.URBAN_SPEED_LIMIT),
      # below the truck weight limit
      ("urban",
       TRUCK_WEIGHT_THRESHOLD - 500,
       hw3.URBAN_SPEED_LIMIT),
      # way below the truck weight limit
      ("urban",
       1000,
       hw3.URBAN_SPEED_LIMIT)]
@pytest.mark.parametrize("area_type, weight, expected",
                         dsl_tests)
def test_determine_speed_limit(area_type, weight, expected):
    """
    Do a single test for Exercise 1: determine_speed_limit
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "determine_speed_limit",
                                            area_type, weight)
    actual = hw3.determine_speed_limit(area_type, weight)
    helpers.check_result(actual, expected, recreate_msg)


def mk_over_limit_tests():
    """
    Construct the tests for is_over_limit from the determine_speed_limit tests
    """
    over_limit_tests = []
    for (area_type, weight, limit) in dsl_tests:
        # add a test below the speed limit
        over_limit_tests.append((area_type, weight, limit - 5, False))
        # add a test at the speed limit
        over_limit_tests.append((area_type, weight, limit, False))
        # add a test at the speed limit
        over_limit_tests.append((area_type, weight, limit + 5, True))
    return over_limit_tests

@pytest.mark.parametrize("area_type, weight, speed, expected",
                         mk_over_limit_tests())
def test_is_over_limit(area_type, weight, speed, expected):
    """
    Do a single test for Exercise 2: is_under_limit
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "is_over_limit",
                                            area_type, weight, speed)
    actual = hw3.is_over_limit(area_type, weight, speed)
    helpers.check_result(actual, expected, recreate_msg)



long_list = [0] * 1000
long_list[0] = -20
long_list[-1] = 10
long_list[500] = -5

neighbor_tests = [
    # has both neighbors
    ([30, 20, 40], 1, 1),
    ([20, 30, 40], 1, 0),
    ([40, 30, 20], 1, 2),
    ([40, 30, 10, 20], 2, 2),
    ([40, 5, 10, 20], 2, 1),
    ([40, 5, 10, 3], 2, 3),
    ([40, 40, 40, 40], 2, 1),


    # no left neighbor
    ([2, 3, -4], 0, 0),
    ([3, 2, -4], 0, 1),
    ([200, 300], 0, 0),
    ([300, 200], 0, 1),
    ([200, 200], 0, 0),

    # no right neighbor
    ([-2, 3, 4], 2, 1),
    ([-3, 4, 2], 2, 2),
    ([3, 4], 1, 0),
    ([4, 2], 1, 1),
    ([2, 2], 1, 0),

    # no left or right neighbor
    ([1], 0, 0),

    # long list tests
    (long_list, 0, 0),
    (long_list, len(long_list)-1, len(long_list)-2),
    (long_list, len(long_list)-2, len(long_list)-3),
    (long_list, 499, 500),
    (long_list, 500, 500),
    (long_list, 501, 500),
    (long_list, 502, 501)]



@pytest.mark.parametrize("values, idx, min_idx",
                         neighbor_tests)
def test_min_in_neighborhood(values, idx, min_idx):
    """
    Do a single test for Exercise 3: min_in_neighborhood
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "min_in_neighborhood",
                                            values, idx)
    actual = hw3.min_in_neighborhood(values, idx)
    helpers.check_result(actual, values[min_idx], recreate_msg)

@pytest.mark.parametrize("values, idx, min_idx",
                         neighbor_tests)
def test_idx_min_neighborhood(values, idx, min_idx):
    """
    Do a single test for Exercise 4: idx_min_neighborhood
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "idx_min_neighborhood",
                                            values, idx)
    actual = hw3.idx_min_neighborhood(values, idx)
    helpers.check_result(actual, min_idx, recreate_msg)

rtests = [
    ([], 0.0),
    ([1], 1.0),
    ([2], 1/2),
    ([1, 2, 3], 1/1 + 1/2 + 1/3),
    ([1, 1, 1], 3.0),
    ([-1, 1], 0.0),
    (list(range(-4,0)), -2.083333333333333),
    (list(range(1, 100)), 5.177377517639621)]


@pytest.mark.timeout(60)
@pytest.mark.parametrize("values, expected", rtests)
def test_sum_reciprocals(values, expected):
    """
    Do a single test for Exercise 5: sum_reciprocals
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "sum_reciprocals", values)
    actual = hw3.sum_reciprocals(values)
    # fix the type if the actual value is 0
    if actual == 0 and isinstance(actual, int):
        actual = 0.0
    helpers.check_result(actual, expected, recreate_msg)



mixed = ([TRUCK_WEIGHT_THRESHOLD] * 10 +
         [TRUCK_WEIGHT_THRESHOLD - 500] * 10 +
         [1000] * 10 +
         [TRUCK_WEIGHT_THRESHOLD + 200] * 5)
# randomly shuffle the values in mixed
random.shuffle(mixed)


cc_tests = [
    ([], 0),
    ([TRUCK_WEIGHT_THRESHOLD + 500],1),
    ([TRUCK_WEIGHT_THRESHOLD], 1),
    ([TRUCK_WEIGHT_THRESHOLD - 500],0),
    ([1000], 0),
    ([TRUCK_WEIGHT_THRESHOLD] * 10,10),
    ([TRUCK_WEIGHT_THRESHOLD] +
     [TRUCK_WEIGHT_THRESHOLD - 500] * 5 +
     [TRUCK_WEIGHT_THRESHOLD + 1], 2),
    (mixed, 15),
    ]
@pytest.mark.timeout(60)
@pytest.mark.parametrize("weights, expected", cc_tests)
def test_count_trucks(weights, expected):
    """
    Do a single test for Exercise 6: count_cars
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "count_trucks", weights)
    actual = hw3.count_trucks(weights)
    helpers.check_result(actual, expected, recreate_msg)


ldb_tests = [
    ([], 10, None),
    ([10], 10, 10),
    ([5], 10, None),
    ([10, 2, 1, 4, 6], 1, 10),
    ([10, 2, 1, 4, 6], 3, 6),
    ([0, 2, 1, 4, 5, -6, -3], 3, 0),
    ([10, 2, 10, 3, 10, 4], 5, 10),
    (list(range(1,100)), 2, 98)
    ]
@pytest.mark.timeout(60)
@pytest.mark.parametrize("values, divisor, expected", ldb_tests)
def test_largest_divisible_by(values, divisor, expected):
    """
    Do a single test for Exercise 7: largest_divisible_by
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "largest_divisible_by",
                                            values, divisor)
    actual = hw3.largest_divisible_by(values, divisor)
    helpers.check_result(actual, expected, recreate_msg)
