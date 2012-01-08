# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# This file defines classes which represent declarations in C language
# files.

import clang.cindex
import collections

class Declaration(object):
    """The base class for all declarations.

    This class is never instantiated directly. It provides fields common to
    all declarations.

    Declarations are intended to be dumb containers. Most of the logic for
    populating data can be found in the built-in observers. The few exceptions
    are where it makes sense to consolidate redundancy, such as in the base
    class.

    Declarations all contain the following properties:

    end_location -- The source location where the declaration ends. Is a tuple
        of (filename, line, column, offset). Line and column are indexed from
        1. Offset is the byte offset in the source file.

    start_location -- The source location where the declaration starts. Is a
        tuple of (filename, line, column, offset). Line and column are indexed
        from 1. Offset is the byte offset in the source file.

    usr -- The Unified Symbol Resolution (USR) string for the entity. These
        are effectively global identifiers that can be used to test for
        type equality.

    TODO capture all fields from Clang bindings automatically.
    """

    __slots__ = (
        'end_location',
        'name',
        'spelling',
        'start_location',
        'usr',
    )

    def __init__(self, cursor):
        """Construct a declaration from a Clang cursor.

        This populates common data from the token behind a cursor.
        """
        self.name = cursor.displayname
        self.spelling = cursor.spelling
        self.usr = cursor.get_usr()

        start = cursor.extent.start
        end = cursor.extent.end
        # TODO normalize file to a sane type
        self.start_location = (start.file, start.line, start.column,
                start.offset)
        self.end_location = (end.file, end.line, end.column, end.offset)

        self._init()

    def _init(self):
        """Called during instance initialization.

        This is a convenience method so children don't need to override
        __init__.
        """
        pass

class Class(Declaration):
    """Represents the declaration of a C++ class.

    This class contains the following properties:

    fields -- Fields/member variables defined in this class.
      It is an ordered dictionary where keys are the field name and
      values are Field instances. The order is the order in which the fields
      were declared in the class definition.
    """

    __slots__ = (
        'fields',
    )

    def _init(self):
        self.fields = collections.OrderedDict()

class Field(Declaration):
    """Represents a C++ class field."""

    __slots__ = (

    )

    def _init(self):
        pass
