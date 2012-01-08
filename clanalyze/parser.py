# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# This file contains code for parsing C language files and interfacing with
# the Clang Python bindings.

from .observer.base import CursorObserver, DefinitionObserver
from .observer.cursor.declaration import ClassExpander
from . import wrapper

import clang.cindex
import os.path

class Parser(object):
    """Interface for parsing C language files.

    This is the heart of Clanalyze. Any time you wish to parse a C language
    file, you create an instance of this class. Next, you register 1 or more
    observers with the parser instance. Then, you parse files with the
    parser and it notifies the observers. Finally, you collect data from the
    observers (if they didn't push data during observation) and do something
    with it.
    """

    __slots__ = (
        '_cursor_observers',
        '_definition_observers',
    )

    EXPAND_CURSORS = set([
        clang.cindex.CursorKind.TRANSLATION_UNIT,
        clang.cindex.CursorKind.NAMESPACE
    ])

    def __init__(self):
        # Load basic built-in observers by default. These observers implement
        # a lot of the business logic, such as expanding class declarations
        # into Clanalyze object type instances. This minimizes the logic in
        # this file.
        self._cursor_observers = [ClassExpander()]
        self._definition_observers = []

    def add_observer(self, obs):
        """Add an observer to the parser instance.

        The observers get notified when specific events occur.
        """
        added = False
        if isinstance(obs, CursorObserver):
            self._cursor_observers.append(obs)
            added = True

        if isinstance(obs, DefinitionObserver):
            self._definition_observers.append(obs)
            added = True

        if not added:
            raise Exception('Observer instance is not a recognized type: %s' %
                    added)

    def remove_observer(self, obs):
        """Remove an observer instance from the parser."""
        self._cursor_observers = [o for o in self._cursor_observers if o != obs]
        self._definition_observers = [o for o in self._definition_observers if
                o != obs]

    def parse(self, filename=None, fh=None, content=None, clang_args=None):
        """Parse an entity and send results to observers.

        This is the method that does all the heavy lefting. It takes input
        from a file, file handle, or string and parses it.

        Arguments:

        filename -- The filename to load source from.
        fh -- The file handle to load source from.
        content -- String containing raw source to parse.
        clang_args -- Arguments that would be passed to Clang compiler to
          compiler this file.
        """
        args = clang_args or []

        # We first convert the input to a set of lines. Along the way we
        # perform input validation.
        lines = []
        source_count = 0
        input_filename = 'INPUT.C'
        if filename is not None:
            if not os.path.exists(filename):
                raise Exception('Passed filename does not exist: %s' %
                        filename)

            with open(filename, 'r') as f:
                lines = [l for l in f]

            input_filename = filename
            source_count += 1

        if fh is not None:
            source_count += 1
            lines = [l for l in fh]

        if content is not None:
            source_count += 1
            raise Exception('Parsing from strings is not yet supported.')

        if source_count == 0:
            raise Exception('No sources given to parse().')
        elif source_count > 1:
            raise Exception('Multiple sources given to parse().')

        index = clang.cindex.Index.create()
        # TODO preserve source filename.
        tu = index.parse(input_filename, args=args,
                unsaved_files=[(input_filename, ''.join(lines))])

        # Clang silently fails if Translation Unit parsing fails. libclang
        # returns null and Python effectively returns None.
        # TODO Submit Python binding patch to escalate error, as None is not
        # the Python way, IMO.
        if not tu:
            raise Exception('Unknown error in Clang when parsing.')

        assert(tu.cursor.kind == clang.cindex.CursorKind.TRANSLATION_UNIT)
        for child, level in self.emit_toplevel_cursors(tu.cursor, 0):
            cursor = wrapper.Cursor(child)
            cursor.tu = tu
            cursor.parser = self

            kind = cursor.kind

            for observer in self._cursor_observers:
                if (observer.PROCESS_KINDS is True or kind in
                observer.PROCESS_KINDS):
                    observer.process_cursor(cursor)

    def emit_toplevel_cursors(self, cursor, level=0):
        """Generator to descend into cursors."""

        yield (cursor, level)

        for child in cursor.get_children():
            yield (child, level)

            if child.kind in self.EXPAND_CURSORS:
                for t in self.emit_toplevel_cursors(child, level + 1): yield t

    def emit_child_cursors(self, cursor, level=0):
        """Generator to descend into cursor and emit all children.

        This emits a tuple of a wrapped cursor and the descendent's distance
        from another cursor. Consumers of the tuples can detect when the
        children of a cursor have finished by noticing a decrease in the numeric
        level.

        This should ideally be a static method. However, the required import in
        built-in observers would fail because of a cyclic import. Keeping it
        an instance and allowing observers to call a method on the passed
        parser instance is manageable.
        """
        for child in cursor.get_children():
            wrapped = wrapper.Cursor(child)
            if isinstance(cursor, wrapper.Cursor):
                wrapped.tu = cursor.tu
                wrapper.parser = cursor.parser

            yield (wrapped, level)

            for t in self.emit_child_cursors(child, level + 1): yield t

    def notify_definition_observers(self, method, *args):
        """Notify definition observers to a new definition.

        This is a pseudo-private method. It is intended to be called by the
        built-in cursor observers which generate higher-level objects derived
        from the AST.

        method -- str method to call on definition observers.
        args -- Set of arguments to pass to called method.
        """

        # TODO need a story for error handling
        for obs in self._definition_observers:
            f = getattr(obs, method)
            f(*args)
