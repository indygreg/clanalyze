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

Licensing
=========

Clanalyze is currently licensed under version 2.0 of the Mozilla Public License.
The full license can be seen at https://www.mozilla.org/MPL/2.0/. If this
license is not satisfactory, please contact the author for consideration on
issuing a version with a different license.

