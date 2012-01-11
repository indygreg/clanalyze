# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# This file contains wrapper classes for Clang's Python classes. The purpose of
# the wrappers is to provide helpful and often used helpers to aid consumer
# implementations.
#
# TODO consider uplifting some of these to the official Clang bindings.

import clang.cindex
import sys

class Cursor(object):
    """Wrapper around Clang's cursor class.

    Aside from providing convenience APIs, this class also keeps a reference
    to the translation unit and Parser instance it was produced by.

    This class acts as a proxy to the original type.
    """

    __slots__ = (
        '_wrapped',
        'tu',
        'parser',
    )

    def __init__(self, cursor):
        self._wrapped = cursor
        self.tu = None
        self.parser = None

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name in ('_wrapped', 'tu', 'parser'):
            object.__setattr__(self, name, value)

        object.__setattr__(self._wrapped, name, value)

    def is_pointer(self):
        """Whether the entity is a pointer."""
        return self.kind == clang.cindex.TypeKind.POINTER

    @property
    def pointee_kind(self):
        """The kind of the type being pointed to."""
        assert(self.is_pointer())

        return self.get_pointee().kind

    def is_array(self):
        """Whether the entity is an array."""
        return self.kind == clang.cindex.TypeKind.CONSTANTARRAY

    @property
    def array_kind(self):
        """The kind inside the array."""
        assert(self.is_array())

        return self.get_array_element_type().kind

    def get_extent_characters(self):
        """Returns the characters representing the extent of this cursor."""
        pass

    def dump(self, fh=None):
        """Convenience method to dump cursor information to text.

        This might be useful when implementing cursor observers.

        If fh is not defined, it writes to stdout.
        """
        if fh is None:
            fh = sys.stdout

        location = self.location
        t = self.type

        print >>fh, 'CURSOR DUMP'
        print >>fh, '  Kind: ', self.kind
        print >>fh, '    Declaration: ', self.kind.is_declaration()
        print >>fh, '    Reference:   ', self.kind.is_reference()
        print >>fh, '    Expression:  ', self.kind.is_expression()
        print >>fh, '    Statement:   ', self.kind.is_statement()
        print >>fh, '    Attribute:   ', self.kind.is_attribute()
        print >>fh, '    Invalid:     ', self.kind.is_invalid()
        print >>fh, '  Definition:   ', self.is_definition()
        print >>fh, '  USR:          ', self.get_usr()
        print >>fh, '  Spelling:     ', self.spelling
        print >>fh, '  Display Name: ', self.displayname
        print >>fh, '  Location:      %s:%d[%d] (%d)' % ( location.file,
                location.line, location.column, location.offset )
        print >>fh, '  Access Level:  ', self.access_specifier

        # TODO extent
        print >>fh, '  Type:'
        print >>fh, '    Kind:          ', t.kind
        print >>fh, '    Canonical:     ', t.get_canonical().kind
        print >>fh, '    Const:         ', t.is_const_qualified()
        print >>fh, '    Volatile:      ', t.is_volatile_qualified()
        print >>fh, '    Restrict:      ', t.is_restrict_qualified()
        print >>fh, '    Pointee:       ', t.get_pointee().kind
        print >>fh, '    Result:        ', t.get_result().kind
        print >>fh, '    Array element: ', t.get_array_element_type().kind
        print >>fh, '    Array size:    ', t.get_array_size()

        print >>fh, '  # Children:   ', len(list(self.get_children()))

class Token(object):
    """Wrapper around Clang's Token class."""

    __slots__ = (
        '_wrapped',
        'tu',
        'parser'
    )

    def __init__(self, token):
        self._wrapped = token
        self.tu = None
        self.parser = None

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name in ('_wrapped', 'tu', 'parser'):
            object.__setattr__(self, name, value)

        object.__setattr__(self._wrapped, name, value)
