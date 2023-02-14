"""
CMSC 14100 Project
Winter 2023
"""

from version import Version

class VersionSpecException(Exception):
    """
    A simple exception for Version error conditions. You should not
    modify this Class and you will not use until Part 2 of the project.
    """
    pass

class VersionSpecification:
    """
    A class to represent a semantic version specification that includes:

        - an optional specifier (~, ^, or +)
        - a version string (major.minor.patch)

    VersionSpec should support the ``str`` functionality by implementing the
    appropriate dunder method.
    """

    def __init__(self, spec_str):
        """
        Construct an instance of the VersionSpec class.

        Inputs:

            spec_str [str]: a version string, optionally augmented
              with a prefix of "~", "^" or "+"
        """

        # You are required to have a Version attribute and
        # to make appropriate use of it in your code.

        # This raise is used in place of our usual pass.
        # Replace it (all subsequent uses) with your code.
        raise NotImplementedError("TODO project 1") ### TODO


    def satisfies_specification(self, ver):
        """
        Determine whether a given version meets the specification.

        Inputs:

            ver [Version]: the version to check

        Returns [bool]: True if the specified version meets the specification,
          and False otherwise.
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __str__(self):
        """ Yields the augmented semantic version string """
        raise NotImplementedError("TODO project 1") ### TODO
