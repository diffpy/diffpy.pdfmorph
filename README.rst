
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


LICENSE
------------------------------------------------------------------------

This software is subject to license and copyright restrictions listed
`here. <https://github.com/diffpy/diffpy.pdfmorph/blob/master/LICENSE.txt/>`_


REQUIREMENTS
------------------------------------------------------------------------

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

To install these packages, please see installation instructions at 
their respective web-pages.


INSTALLATION
------------------------------------------------------------------------

To create and activate a conda environment to use this software, run 
the following command from the command line ::
	
	conda create -n pdfmorph_env python=3
	source activate pdfmorph_env

If you're using Windows, replace ``source activate pdfmorph`` with ::
	
	activate pdfmorph_env

When you are finished with the session, exit the environment by running :: 

	source deactivate pdfmorph_env

or ::

	deactivate pdfmorph_env

If you use this conda environment, make sure to run the ``source activate 
pdfmorph_env`` or ``activate pdfmorph_env`` commands from your command 
line before every session using the applicaiton.

If you're using Anaconda Python, you can install from the "conda-forge" 
channel of Anaconda packages ::

     conda config --add channels conda-forge
     conda install diffpy.pdfmorph

If you don't use Anaconda or prefer to install from sources, please 
consult online documentation.

With Anaconda, PDFmorph can be later upgraded to the latest released
version using ::

     conda update diffpy.pdfmorph

With other Python distributions the program can be upgraded to
the latest version as follows ::

     easy_install --upgrade diffpy.pdfmorph


USING PDFmorph
------------------------------------------------------------------------

For detailed instructions and full tutorial, consult online documentation.

Once the required software, including PDFmorph is all installed, open
up a terminal and check installation has worked properly by running ::

	source activate pdfmorph_env
	pdfmorph -h			#get some helpful information
	pdfmorph --version

If installed correctly, this last command should return the latest 
version of PDFmorph. To begin using PDFmorph, run a command like ::

	pdfmorph <target PDF file> <morphed PDF file>

to see PDFmorph in action.


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

