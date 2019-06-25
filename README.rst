image here
image target here

image here
image target here


PDFmorph
========================================================================
# FIXME
add description, sample below
Code package for morphin' atomic pair distribution functions.


REQUIREMENTS
------------------------------------------------------------------------

PDFmorph requires Python 3.7 and several third party libraries 
that are used by PDFmorph and its components.

* setuptools         - tools for installing and setting up Python packages
* Sphinx             - documentation generator for reStructuredText files
* sphinx_rtd_theme   - user-friendly sphinx theme
* Doctr              - deploys docs from Travis CI to GitHub pages
* pip                - package installer for Python
* NumPy              - library for scientific computing with Python
* matplotlib         - Python 2D plotting library
* SciPy              - library for highly technical Python computing
* diffpy.utils       - shared helper utilities for wx GUI, 
https://github.com/diffpy/diffpy.utils
* Flake8             - tool for performing static analysis of source code to
check for discrepancies
* pytest             - framework to make test writing more illustrative
* codecov            - package to improve workflow
* coverage           - tool for measuring code coverage of Python programs
* pytest-env         - pytest plugin that allows you to add environment
variables

# FIXME - add link for instructions
If you can't use conda and need to build from the sources, instructions are [here].

INSTALLATION
------------------------------------------------------------------------

The preferred method is to use Anaconda Python and install from the
"diffpy" channel of Anaconda packages ::

     conda config --add channels diffpy
     conda install diffpy.pdfmorph

# FIXME
PDFmorph can then be started from a terminal...
[insert more instructions here]

With Anaconda, PDFmorph can be later upgratded to the latest released
version using ::

     conda update diffpy.pdfmorph

With other Python distributions the program can be upgraded to
the latest version as follows ::

     easy_install --upgrade diffpy.pdfmorph


Other Software
````````````````````````````````````````````````````````````````````````

[other software info]


DEVELOPMENT
------------------------------------------------------------------------

PDFmorph is an open-source software available in a git repository at
https://github.com/diffpy/diffpy.pdfmorph.

Feel free to fork the project and contribute! To install PDFmorph
in a development mode where the source files are used directly
rather than copied to a system directory, use ::

     python setup.py develop --user


CONTACTS
------------------------------------------------------------------------

For more information on PDFmorph, visit the project wep-page:

# FIXME - make a page for the project
[insert project page here, when it exists]

or email Professor Simon Billinge at sb2896@columbia.edu
