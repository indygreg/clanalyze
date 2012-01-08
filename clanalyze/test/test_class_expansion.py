# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from clanalyze.observer.base import DefinitionObserver
from clanalyze.parser import Parser
import unittest

class RecordDefinitionObserver(DefinitionObserver):
    def __init__(self):
        self.class_count = 0

    def process_class_definition(self, c):
        self.class_count += 1

class TestSimpleClassExpansion(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.definition_observer = RecordDefinitionObserver()

        self.parser.add_observer(self.definition_observer)

    def test_notify_definition_fired(self):
        # TODO proper path
        self.parser.parse(filename='clanalyze/test/class_empty.cpp')

        self.assertEqual(1, self.definition_observer.class_count)
