"""
CMSC 14100
Winter 2023
"""
from version import Version, VersionException
from version_spec import VersionSpecification, VersionSpecException


class LibraryException(Exception):
    """
    A simple exception for described error conditions. You should not
    modify this Class at all.
    """
    pass


class Library:
    """
    A class to represent a published library. This class will have public
    attributes for:

        - A name
        - A version, and
        - The name of the person who registered the library

    Library should support the ``str`` functionality by implementing the
    appropriate dunder method.
    """

    def __init__(self,
                 name,
                 version_str,
                 registered_by,
                 ):
        """
        Create a new library.

        Inputs:

            name(str): The name of the library

            version_str (str): The semantic version number

            registered_by (str): The name of the developer who
              registered the library

        Raises:

            LibraryException - if the supplied version string is not a
              valid version string.

        """
        raise NotImplementedError("TODO project 2") ### TODO


    def is_stable(self):
        """
        Is this library stable, that is, does it have a stable version number.

        Returns (bool):

            True if the library has a stable version number, False otherwise.
        """
        raise NotImplementedError("TODO project 2") ### TODO


    def satisfies_version_req(self, version_spec):
        """
        Checks if this Library satisfies the version specification

        Inputs:

            version_spec (VersionSpecification): the version specification
              that is of interest

        Raises:

            LibraryException - if version_spec is not an instance of the
              VersionSpecification class

        Returns (bool):

            Returns True if the library's version satisfies the provided
            version specification and False, otherwise.
        """
        raise NotImplementedError("TODO project 2") ### TODO


    def is_later_version(self, other):
        """
        Does this library's version come after the other library's
        version in the semantic version ordering?

        Inputs:

            other (Library): the library to check

        Raises:

            LibraryException - if other is not an instance of the Library class

            LibraryException - if other does not have the same library name as
              this library

        Returns (bool):

            Returns True if this library's version comes later in the
              semantic version ordering than other's.  False, otherwise.
        """
        raise NotImplementedError("TODO project 2") ### TODO


    def add_dependency(self, dep):
        """
        Add dep as a library that this one depends upon.

        Inputs:

            dep (Library): the library to add as a dependency

        Raises:

            LibraryException - if dep is not an instance of the Library class

            LibraryException - if this library is stable and dep is not a stable
              library.

            LibraryException - if this library already depends on a library with
              the same name as dep.
        """
        raise NotImplementedError("TODO project 2") ### TODO


    def remove_dependency(self, dep):
        """
        Remove dep from dependencies for this library

        Inputs:

            dep (Library): the library that to remove as a dependency


        Raises:

            LibraryException - if dep is not an instance of the Library class

            LibraryException - if this library is not dependent on the
              library dep.
        """
        raise NotImplementedError("TODO project 2") ### TODO


    def __str__(self):
        """
        Construct a string:
        """
        raise NotImplementedError("TODO project 2") ### TODO
