
.. image:: https://travis-ci.org/diffpy/diffpy.pdfmorph.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.pdfmorph

.. image:: http://codecov.io/github/diffpy/diffpy.pdfmorph/coverage.svg?branch=master
   :target: http://codecov.io/github/diffpy/diffpy.pdfmorph?branch=master


PDFmorph
========================================================================
# FIXME - include uses, unique features
PDFmorph is a Python software package designed to increase the insight
researchers can get into spectra collected for atomic pair distribution 
functions.

REQUIREMENTS
------------------------------------------------------------------------

PDFmorph requires Python 3 and several third party libraries 
that are used by PDFmorph and its components.

* NumPy              - library for scientific computing with Python
* matplotlib         - Python 2D plotting library
* SciPy              - library for highly technical Python computing
* diffpy.utils       - shared helper utilities for wx GUI, https://github.com/diffpy/diffpy.utils

# FIXME - add link for instructions
If you can't use conda and need to build from the sources, instructions are [here].

INSTALLATION
------------------------------------------------------------------------

PDFmorph is an application which makes use of the Command Line Interface to
run. If you are unfamiliar with the CLI, consult online resources on how to get 
started with it on your machine.

It is recommended that you use Anaconda Python to run this application; to do so,
first make sure that you have installed it from Anaconda distribution here:
https://www.anaconda.com/distribution/.

The preferred method is to use Anaconda Python and install from the
"conda-forge" channel of Anaconda packages ::

     conda config --add channels conda-forge
     conda install diffpy.pdfmorph

# FIXME
To ensure the installation worked, activate the relevant conda environment and 
type ::

	pdfmorph --version

If installed correctly, this command should return PDFmorph's current version
number.

With Anaconda, PDFmorph can be later upgraded to the latest released
version using ::

     conda update diffpy.pdfmorph

#FIXME - easy_install?
With other Python distributions the program can be upgraded to
the latest version as follows ::

     easy_install --upgrade diffpy.pdfmorph

# FIXME - make sure information is correct here
Once installed, PDFmorph can be utilized by running the following command::

	pdfmorph <source filename> <target filename>

Where <source filename> is the PDF function you wish to compare and
<target filename> is the file you want PDFmorph to return.

# FIXME - add reference to online instrucitons
For more information on how to use PDFmorph, please consult online documentation
[here].


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


LICENSE
------------------------------------------------------------------------

For full license and copyright information, check `here <https://github.com/diffpy/diffpy.pdfmorph/blob/master/LICENSE.txt/>`_ 
