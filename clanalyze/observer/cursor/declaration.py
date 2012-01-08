# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import CursorObserver
from ...declaration import Class, Field

import clang.cindex

class ClassExpander(CursorObserver):
    """Expands class declarations into a high-level data structure.

    This is a built-in observer which takes class declaration cursors and
    converts them into object types defined in this package. It then passes
    these objects to other observers through the parser.
    """

    PROCESS_KINDS = [clang.cindex.CursorKind.CLASS_DECL]

    # Set of cursor kinds to ignore when processing classes.
    IGNORE_KINDS = [
        clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL
    ]

    def process_cursor(self, cursor):
        # We only care about cursors that also define the class.
        if not cursor.is_definition():
            return

        cl = Class(cursor)

        # We descend into all cursors contained within the class definition
        # and extract information as we encounter it.
        for c, level in cursor.parser.emit_child_cursors(cursor):
            if c.kind in ClassExpander.IGNORE_KINDS:
                continue

            if c.kind == clang.cindex.CursorKind.FIELD_DECL:
                field = ClassExpander.create_field(c)
                cl.fields[field.name] = field

        cursor.parser.notify_definition_observers('process_class_definition',
                cl)

    @staticmethod
    def create_field(cursor):
        """Construct a field from a cursor."""
        field = Field(cursor)

        return field
