
.. image:: https://travis-ci.org/diffpy/diffpy.pdfmorph.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.pdfmorph

.. image:: http://codecov.io/github/diffpy/diffpy.pdfmorph/coverage.svg?branch=master
   :target: http://codecov.io/github/diffpy/diffpy.pdfmorph?branch=master


PDFmorph
========================================================================

PDFmorph is a Python software package designed to increase the insight 
researchers can obtain from measured atomic pair distribution functions 
(PDFs) in a model-independent way. The program was designed to help a 
researcher answer the question: Has my material undergone a phase 
transition between these two measurements?

One approach is to compare the two PDFs in a plot and view the difference 
curve underneath. However, significant signal can be seen in the 
difference curve from benign effects such as thermal expansion (peak 
shifts) and increased thermal motion (peak broadening) or a change in 
scale due to differences in incident flux, for example. PDFmorph will 
do its best to correct for these benign effects before computing and 
plotting the difference curve. One measured PDF (typically that collected
under higher temperature) is identified as the target PDF and the second 
PDF is then morphed by "stretching" (chaning the r-axis to simulate a 
uniform lattice expansion), "smearing" (broadening peaks through a 
uniform convolution to simulate increased thermal motion), and "scaling" 
(self-explanatory). PDFmorph will vary the amplitude of the morphing 
transformations to obtain the best fit between the morphed and the target 
PDFs, then plot them on top of each other with the difference plotted 
below.

There are also a few other morphing transformations in the program.

Finally, we note that PDFmorph should work on other spectra that are not 
PDFs, though it has not been extensively tested beyond the PDF.


LICENSE
------------------------------------------------------------------------

This software is subject to license and copyright restrictions listed
`here. <https://github.com/diffpy/diffpy.pdfmorph/blob/master/LICENSE.txt/>`_


REQUIREMENTS
------------------------------------------------------------------------

PDFmorph is currently run from the command line, which requires opening
and typing into a terminal window or Windows command prompt. It is 
recommended that you consult online resources and become somewhat 
familiar before using PDFmorph.

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

For your future sessions with the application: Make sure to run the 
``source activate pdfmorph_env`` or ``activate pdfmorph_env`` commands 
from your command line beforehand to ensure access to the software.

Once in your desired conda environment, you can install from either the
"diffpy" or "conda-forge" channels of Anaconda packages by running 
either ::

	conda config --add channels diffpy
	conda install diffpy.pdfmorph

or ::

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

where both PDFs file are text files which contain PDF data, such as those
produced by ``PDFgetX2``, ``PDFgetX3``, or ``PDFgui``. Though some file
extensions other than .cgr, but with the same content structure, have
been shown to work with PDFmorph, it is recommended to stick with .cgr 
files such as those in the tutorial.

Enjoy!


DEVELOPMENT
------------------------------------------------------------------------

PDFmorph is an open-source software project on Github:
https://github.com/diffpy/diffpy.pdfmorph.

Feel free to fork the project and contribute! To install PDFmorph
in a development mode where the source files are used directly
rather than copied to a system directory, use ::

     python setup.py develop --user


CONTACTS
------------------------------------------------------------------------

For more information on PDFmorph, visit the `PDFmorph project web-page, <https://github.com/diffpy/diffpy.github.io/blob/source/products/pdfmorph.rst/>`_
or email Professor Simon Billinge at sb2896@columbia.edu

