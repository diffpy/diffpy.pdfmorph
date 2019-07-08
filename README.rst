FIXME - testing correctness of these links

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
* diffpy.utils       - shared helper utilities for wx GUI, 
https://github.com/diffpy/diffpy.utils

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
"diffpy" channel of Anaconda packages ::

     conda config --add channels diffpy
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
This program is part of the DiffPy open-source projects at Columbia
University and is available subject to the conditions and terms laid out below.

Copyright © 2009-2019, Trustees of Columbia University in the City of New York,
all rights reserved.

For more information please visit the diffpy web-page at http://diffpy.org or
email Prof. Simon Billinge at sb2896@columbia.edu.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the names of COLUMBIA UNIVERSITY, MICHIGAN STATE UNIVERSITY nor the
    names of their contributors may be used to endorse or promote products
    derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
