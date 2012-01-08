=========
Clanalyze
=========

Clanalyze is a C language analyzer. The goal of Clanalyze is to provide a
framework by which people can easily consume parsed C language files, including
C, C++, and Objective-C.

Using Clanalyze, it is possible to easily write tools that:

* Check C/C++ style conventions
* Perform compiler-like warnings
* Build documentation from C/C++ source files
* Perform static analysis

Clanalyze is built on top of Clang, the C language compiler that is part of the
LLVM project. Clanalyze supplements the low-level Python bindings provided by
Clang with higher-level, easier-to-consume APIs for tool writers.

Clanalyze was originally authored by Gregory Szorc <gregory.szorc@gmail.com>.

Requirements
============

Clanalyze requires Clang and the Clang Python bindings.

As part of developing Clanalyze, the author of Clanalyze needed to add
functionality to the Clang Python bindings. The state of those changes is
as follows:

* Support for C++ access specifiers - Patch not yet submitted.

Until all the above changes are merged into Clang's source tree and released,
you probably don't have them available on your machine. Fortunately, the
Clang Python bindings are located in a self-contained .py file. So, all you
need to do is fetch an updated copy of that file and make it available in your
PYTHONPATH.

TODO Create GitHub Clang branch with all Python changes applied.

Technical Overview
==================

Clanalyze provides a basic observer framework for entities (i.e. Python classes)
wishing to react to events/entities in parsed C-family source code.

The general usage looks something like the following:

# Create a clanalyze.parser.Parser() instance
# Register observers with the parser
# Parse source code using Parser.parse()
# (Observers get called for observed events, perform side-effects)
# Profit

Writing Observers
-----------------

To do something useful with Clanalyze, you'll want to write an observer.
Writing an observer is as simple as creating a Python class that uses one
of the built-in abstract observer base classes as its parent.

You have the following choices for observers:

* DefinitionObserver - Consumes high-level entity definitions, such as classes,
  structs, and functions which are derived from the AST. Basically, Clanalyze
  takes the low-level AST cursor stream and converts it into friendly Python
  objects.  This is a real value-add of Clanalyze, as it saves you from having to
  reimplement low-level logic interacting with the Clang parser.

* CursorObserver - Consumes raw Clang AST cursor stream. This is very low-level
  and very close to the Clang API. If you are using this API, Clanalyze doesn't
  really provide much incremental benefit over consuming the Python Clang API
  directly.

When writing observers, it is important to conform to the API they have
provided. See the documentation in the base classes for details.

Licensing
=========

Clanalyze is currently licensed under version 2.0 of the Mozilla Public License.
The full license can be seen at https://www.mozilla.org/MPL/2.0/. If this
license is not satisfactory, please contact the author for consideration on
issuing a version with a different license.

