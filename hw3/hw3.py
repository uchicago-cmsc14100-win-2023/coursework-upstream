"""
CMSC 14100
Winter 2023

Homework #3

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URL of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.


[RESUBMISSIONS ONLY: Explain how you addressed the grader's comments
 for your original submission.  If you did not submit a solution for the
 initial deadline, please state that this submission is new.]
"""

# Provided function
def is_car(weight):
    """
    Does a vehicle qualify as a car?

    Inputs:
        weight [float]: vehicle's weight

    Returns [bool]: True, if the vehicle qualifies as a car.
        False, otherwise.
    """
    return weight < 4500


#######
# Constants used in Exercises 1-2
#######

URBAN_SPEED_LIMIT = 25
SUBURBAN_SPEED_LIMIT = 55
RURAL_CAR_SPEED_LIMIT = 70
RURAL_TRUCK_SPEED_LIMIT = 55


def determine_speed_limit(area_type, weight):
    """
    Determine the speed limit for a vehicle based on the type of area
    in which it is travelling and its weight.

    Inputs:
        area_type [string]: one of "urban", "suburban", and "rural"
        weight [float]: the weight of the vehicle

    Returns [int]: the speed limit for the vehicle
    """
    # Verify that the parameters have sensible values
    assert area_type in ("urban", "suburban", "rural")
    assert weight > 0


    ### Replace pass with your solution
    pass


def is_over_limit(area_type, weight, speed):
    """
    Your docstring here.
    """
    # Verify that the parameters have sensible values
    assert area_type in ("urban", "suburban", "rural")
    assert weight > 0
    assert speed >= 0

    ### Replace pass with your solution
    pass


def min_in_neighborhood(values, location):
    """
    Your docstring here.
    """
    # Verify that the list has at least one element
    assert len(values) > 0
    # Verify that location is a legal non-negative index for values.
    assert 0 <= location < len(values)

    ### Replace pass with your solution

    ### Restrictions: You may NOT use helper functions (including the built-in
    ###    min and max functions and the list index method) for this task
    pass


def idx_min_neighborhood(values, location):
    """
    Your docstring here.
    """
    # Verify that the list has at least one element
    assert len(values) > 0
    # Verify that location is a legal (non-negative) index for values.
    assert 0 <= location < len(values)

    ### Replace pass with your solution

    ### Restrictions: You may NOT use helper functions (including the built-in
    ###    min and max functions and the list index method) for this task.
    pass


def sum_reciprocals(vals):
    """
    Your docstring here.
    """
    ### Replace pass with your solution
    pass


def count_trucks(vehicle_weights):
    """
    Your docstring here.
    """
    ### Replace pass with your solution
    pass


def largest_divisible_by(vals, divisor):
    """
    Your docstring here.
    """
    ### Replace the next line with your solution
    raise NotImplementedError("Implementation missing")
