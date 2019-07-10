
.. image:: https://travis-ci.org/diffpy/diffpy.pdfmorph.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.pdfmorph

.. image:: http://codecov.io/github/diffpy/diffpy.pdfmorph/coverage.svg?branch=master
   :target: http://codecov.io/github/diffpy/diffpy.pdfmorph?branch=master


PDFmorph
========================================================================

PDFmorph is a Python software package designed to increase the insight
researchers can obtain from measured atomic pair distribution functions 
(PDFs) in a model-independent way. The program was designed to help a 
researcher  answer the question: "has my material undergone a phase 
transition between these two measurements?"

When given two PDFs to compare, PDFmorph attempts to correct for benign 
effects like thermal expansion and increased thermal motion before 
"morphing" one PDF to a selected "target" (usually, the higher-temperature
PDF). After "stretching", "smearing", and "scaling" the PDF, PDF will
find the best fit between the morphed and target PDFs and plot them on 
top of each other with the difference curve plotted below.

Finally, we note that PDFmorph should work on other spectra that are not 
PDFs, though it has not been extensively tested beyond the PDF.

For more information on PDFmorph, please consult the documentation.

REQUIREMENTS
-----------------------------------------------------------------------

The PDFmorph application has a Command Line interface. If you are 
unfamiliar with the terminal or windows command prompt, it is recommended
that you consult online resources and become somewhat familiar before
using PDFmorph.

PDFmorph requires Python 3 and several third party libraries 
that are used by PDFmorph and its components.

* NumPy              - library for scientific computing with Python
* matplotlib         - Python 2D plotting library
* SciPy              - library for highly technical Python computing
* diffpy.utils       - `shared helper utilities <https://github.com/diffpy/diffpy.utils/>`_ for wx GUI

It is recommended that you use `Anaconda Python <https://www.anaconda.com/distribution/>`_ to conveniently 
install PDFmorph and its software dependencies with a few concise 
commands. For example, on Ubuntu Linux some of the required software 
can be installed using ::

	sudo apt-get install \
	python-setuptools python-wxtools python-numpy \ 
	python-matplotlib

To install the remaining packages, see installation instructions at 
their respective web-pages.

INSTALLATION
------------------------------------------------------------------------

If you're using Anaconda Python, you can install from the "conda-forge" 
channel of Anaconda packages ::

     conda config --add channels conda-forge
     conda install diffpy.pdfmorph

If you don't use Anaconda or prefer to install from sources, make sure 
the required software is all in place and run ::
	
	python setup.py install

By default the files are installed to standard system directories, 
which may require the use of ``sudo`` for write privileges. If 
administrator (root) access is not available, see the output from 
``python setup.py install --help`` for options to install as a regular 
user to user-writable locations. Note that installation to non-standard 
directories may require adjustments to the PATH and PYTHONPATH 
environment variables.

To ensure the installation worked, activate the relevant conda 
environment and type ::

	pdfmorph --version

If installed correctly, this command should return PDFmorph's current 
version number.

PDFmorph can then be started from a terminal ("Anaconda Prompt" on 
Windows) by executing the ``pdfmorph`` program.

With Anaconda, PDFmorph can be later upgraded to the latest released
version using ::

     conda update diffpy.pdfmorph

With other Python distributions the program can be upgraded to
the latest version as follows ::

     easy_install --upgrade diffpy.pdfmorph

For more information on how to use PDFmorph, please consult its online 
documentation.


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

For more information on PDFmorph, visit the `PDFmorph project web-page, <https://github.com/diffpy/diffpy.github.io/blob/source/products/pdfmorph.rst/>`_
or email Professor Simon Billinge at sb2896@columbia.edu


LICENSE
------------------------------------------------------------------------

For full license and copyright information, check `here. <https://github.com/diffpy/diffpy.pdfmorph/blob/master/LICENSE.txt/>`_ 
