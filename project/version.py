"""
CMSC 14100 Project
Winter 2023
"""

class VersionException(Exception):
    """
    A simple exception for Version error conditions. You should not
    modify this Class and you will not use until Part 2 of the project.
    """
    pass


class Version:
    """
    A class to represent an exact semantic version that includes:

        - a major release number
        - a minor release number
        - a patch release number

    All three parts are required.

    Version should support the following functionality by implementing the
    appropriate dunder methods:

    - str(v) - constructs a version string major.minor.patch

    - v1 == v2 - version v1 and version v2 represent the same semantic version

    - v1 != v2 - version v1 and version v2 do not represent the
         same semantic version

    - v1 < v2 - version v1 comes earlier in the semantic version
         ordering than v2

    - v1 <= v2 - version v1 comes earlier in the semantic version
         ordering than v2 or v1 and v2 represent the same semantic version

    - v1 > v2 - version v1 comes later in the semantic version ordering
         than v2

    - v1 >= v2 - version v1 comes later in the semantic version ordering
         than v2 or v1 and v2 represent the same semantic version
    """
    def __init__(self, major, minor, patch):
        """
        Create a new Version instance from the specified release numbers.

        Inputs:

            major (int): the major release number
            minor (int): the minor release number
            patch (int): the patch release number
        """

        # Requirement: all attributes for this class
        # must be private.

        # The raise is used in place of our usual pass.
        # Replace it (all subsequent uses) with your code.
        raise NotImplementedError("TODO project 1") ### TODO


    def get_major(self):
        """ Return the major release number from the version"""
        raise NotImplementedError("TODO project 1") ### TODO


    def get_minor(self):
        """ Return the minor release number from the version"""
        raise NotImplementedError("TODO project 1") ### TODO


    def get_patch(self):
        """ Return the patch release number from the version"""
        raise NotImplementedError("TODO project 1") ### TODO


    def is_stable(self):
        """
        Is this version stable?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __str__(self):
        """
        Constructs a string representation of the version with
        the components separated by periods.

        Sample use: str(Version(3, 2, 1)) yields "3.2.1"
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __eq__(self, other):
        """
        Does this version (self) represent the same semantic version as other?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __ne__(self, other):
        """
        Does this version (self) represent a different semantic version
        than other?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __gt__(self, other):
        """
        Does this version (self) come later in the semantic version
        ordering than other?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __ge__(self, other):
        """
        Does this version (self) come later in the semantic version
        ordering than other or, alternatively, does it represent the
        same semantic version as other?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __lt__(self, other):
        """
        Does this version (self) come earlier in the semantic version
        ordering than other?
        """
        raise NotImplementedError("TODO project 1") ### TODO


    def __le__(self, other):
        """
        Does this version (self) come earlier in the semantic version
        ordering than other or, alternatively, does it represent the
        same semantic version as other?
        """
        raise NotImplementedError("TODO project 1") ### TODO
