
.. image:: https://travis-ci.org/diffpy/diffpy.pdfmorph.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.pdfmorph

.. image:: http://codecov.io/github/diffpy/diffpy.pdfmorph/coverage.svg?branch=master
   :target: http://codecov.io/github/diffpy/diffpy.pdfmorph?branch=master


PDFmorph
========================================================================

PDFmorph is a Python software package designed to increase the insight
researchers can obtain from measured atomic pair distribution functions (PDFs) 
in a model independent way. The program was designed to help a researcher 
answer the question: "has my material undergone a phase transition between 
these two measurements?".

One approach is to compare the two PDFs in a plot and view the difference curve
underneath. However, significant signal can be seen in the difference curve from
benign effects such as thermal expansion (peak shifts) and increased thermal 
motion (peak broadening) or a change in scale due to differences in incident flux,
for example. PDFmorph will do its best to correct for these benign effects before 
computing and plotting the difference curve. One measured PDF (typically the higher
temperature one) is identified as the target PDF and the second PDF is then "morphed"
by "stretching" (chaning the r-axis to simulate a uniform lattice expansion),
"smearing" (broadening peaks through a uniform convolution to simulate increased
thermal motion), and "scaling" (self-explanatory). PDFmorph will vary the amplitude
of the morphing transformations to obtain the best fit between the morphed and the
target PDFs, then plot them on top of each other with the difference plotted below.

There are also a few other morphing transformations in the program.

Finally, we note that PDFmorph should work on other spectra that are not PDFs,
though it has not been extensively texted beyond the PDF.

REQUIREMENTS
------------------------------------------------------------------------

PDFmorph requires Python 3 and several third party libraries 
that are used by PDFmorph and its components.

* NumPy              - library for scientific computing with Python
* matplotlib         - Python 2D plotting library
* SciPy              - library for highly technical Python computing
* diffpy.utils       - shared helper utilities for wx GUI, https://github.com/diffpy/diffpy.utils

It is recommended that you use `Anaconda Python <https://www.anaconda.com/distribution/>`_ to conveniently install PDFmorph and its software dependencies 
with a few concise commands. For example, on Ubuntu Linux some of the required
software can be installed using ::

	sudo apt-get install \
	python-setuptools python-wxtools python-numpy \ 
	python-matplotlib

To install the remaining packages, see installation instructions at their
respective web-pages.

INSTALLATION
------------------------------------------------------------------------

PDFmorph is an application which makes use of the Command Line Interface to
run. If you are unfamiliar with the CLI, consult online resources on how to get 
started with it on your machine.

If you're using Anaconda Python, you can install from the "conda-forge" 
channel of Anaconda packages ::

     conda config --add channels conda-forge
     conda install diffpy.pdfmorph

If you don't use Anaconda or prefer to install from sources, make sure the required
software is all in place and run ::
	
	python setup.py install

By default the files are installed to standard system directories, which may require
the use of ``sudo`` for write privileges. If administrator (root) access is not
available, see the output from ``python setup.py install --help`` for options to 
install as a regular user to user-writable locations. Note that installation to
non-standard directories may require adjustments to the PATH and PYTHONPATH 
environment variables.

To ensure the installation worked, activate the relevant conda environment and 
type ::

	pdfmorph --version

If installed correctly, this command should return PDFmorph's current version
number.

PDFmorph can then be started from a terminal ("Anaconda Prompt" on Windows) by
executing the ``pdfmorph`` program.

With Anaconda, PDFmorph can be later upgraded to the latest released
version using ::

     conda update diffpy.pdfmorph

With other Python distributions the program can be upgraded to
the latest version as follows ::

     easy_install --upgrade diffpy.pdfmorph

# FIXME - add reference to online instrucitons once merged
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

# FIXME - add link to diffpy.org/products/pdfmorph.html when that exists
For more information on PDFmorph, visit the `PDFmorph project web-page. <https://github.com/diffpy/diffpy.github.io/blob/source/products/pdfmorph.rst/>`_

or email Professor Simon Billinge at sb2896@columbia.edu


LICENSE
------------------------------------------------------------------------

For full license and copyright information, check `here. <https://github.com/diffpy/diffpy.pdfmorph/blob/master/LICENSE.txt/>`_ 
