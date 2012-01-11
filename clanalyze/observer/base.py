# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

class TokenObserver(object):
    """Base class for observers handling the token stream.

    These observers consume the tokenized source code before it is turned
    into an AST.

    This class is useful for accessing details lost during the translation to
    an AST, such as the presence and locations of braces, comments, and raw
    identifiers.

    TODO support filtering
    """

    def process_token(self, token):
        """Handler called when an individual token is processed.

        This method must be implemented by child classes. It is called
        by the parser for every token present in the original translation unit.

        token -- wrapper.Token instance of the token to be processed. The
            instance contains references to the original translation unit and
            Parser the token was derived from.
        """
        raise Exception('process_token must be implemented.')

class CursorObserver(object):
    """Base class for observers handling the raw cursor stream from the parser.

    Consumers wishing to consume the low-level cursors emitted from translation
    units must derive from this class.

    This class is useful for extracting details from the parsed AST. Clanalyze
    uses this internally to create higher-level representations of parsed
    entities, like classes and functions.
    """

    """Define which cursor kinds this observer handles.

    This is used as an optimization so process_cursor() isn't called more than
    necessary and so the implementation in observers isn't burdened with type
    checking.

    If True, all cursor kinds will be sent to the observer. Otherwise, define
    an iterable of clang.cindex.CursorKind to perform filtering.
    """
    PROCESS_KINDS = True

    def __init__(self):
        pass

    def process_cursor(self, cursor):
        """Handler called when an individual cursor is processed.

        This method must be implemented by child classes. It is called by the
        parser for every cursor present in the original translation unit.

        cursor -- wrapper.Cursor instance of the cursor to be processed. This
            wrapper contains references to the original translation unit and
            Parser if the observer needs to access them.
        """
        raise Exception('process_cursor must be implemented.')

class DefinitionObserver(object):
    """Base class for observers handling higher-level entity definitions.

    This observer type is used to react to derived entities from the AST, such as
    class and function definitions.

    This observer can be thought of a convenience layer over consuming the raw
    AST cursor stream. Clanalyze does a lot of heavy lifting to convert the
    AST to simple data structures so you don't need to burden yourself with the
    Clang API.
    """

    def process_class_definition(self, c):
        """Process a class definition.

        Takes a declaration.Class instance describing the class that was
        defined.
        """
        pass
