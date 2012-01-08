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

Requirements
============

Clanalyze requires Clang and the Clang Python bindings.

As part of developing Clanalyze, the author of Clanalyze needed to add
functionality to the Clang Python bindings. The state of those changes is
as follows:

* Support for C++ access specifiers - Patch not yet submitted.
