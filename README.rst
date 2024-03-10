
.. image:: https://travis-ci.org/diffpy/diffpy.pdfmorph.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.pdfmorph

.. image:: http://codecov.io/github/diffpy/diffpy.pdfmorph/coverage.svg?branch=master
   :target: http://codecov.io/github/diffpy/diffpy.pdfmorph?branch=master


PDFmorph
========================================================================


PDFmorph is a Python software package designed to increase the insight 
researchers can obtain from measured atomic pair distribution functions 
(PDFs) in a model-independent way. The program was designed to help a 
researcher answer the question: "Has my material undergone a phase 
transition between these two measurements?"

One approach is to compare the two PDFs in a plot and view the difference 
curve underneath. However, significant signal can be seen in the 
difference curve from benign effects such as thermal expansion (peak 
shifts) and increased thermal motion (peak broadening) or a change in 
scale due to differences in incident flux, for example. PDFmorph will 
do its best to correct for these benign effects before computing and 
plotting the difference curve. One measured PDF (typically that collected
at higher temperature) is identified as the target PDF and the second 
PDF is then morphed by "stretching" (changing the r-axis to simulate a 
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

PDFmorph can be run with Python 2.7 and Python 3.5 or higher. We 
recommend using the Python 3 version. It makes use of several third party
libraries that you'll need to run the app and its components.

* NumPy              - library for scientific computing with Python
* matplotlib         - Python 2D plotting library
* SciPy              - library for highly technical Python computing
* diffpy.utils       - `shared helper utilities <https://github.com/diffpy/diffpy.utils/>`_ for wx GUI

These dependencies will be installed automatically if you use the conda
installation procedure described below.


INSTALLATION
------------------------------------------------------------------------

We recommend installing the software using conda. If you have anaconda
or mini-conda installed on your computer, you can proceed directly to
the instructions below. If not, we recommend that you install mini-
conda and test that it is working by opening a terminal and typing
``conda``.
 
To create and activate a conda environment to use this software, run 
the following command from the command line ::
	
	conda create -n pdfmorph_env python=3 --yes
	source activate pdfmorph_env

If you're using Windows, replace ``source activate pdfmorph`` with 
``activate pdfmorph_env``.

When you are finished with the session, exit the environment by running :: 

	source deactivate pdfmorph_env

or, on Windows, ``deactivate pdfmorph_env``.

For your future sessions with the application: Make sure to run the 
``source activate pdfmorph_env`` or ``activate pdfmorph_env`` commands 
from your command line beforehand to ensure access to the software.

Once in your desired conda environment, you can install from either the
"diffpy" or "conda-forge" channels of Anaconda packages by running 
either ::

	conda config --add channels conda-forge
	conda install diffpy.pdfmorph
 
If you do not use conda or prefer to install from sources, please 
consult online documentation.

With conda, PDFmorph can be later upgraded to the latest released
version using ::

     conda update diffpy.pdfmorph

With other Python distributions the program can be upgraded to
the latest version as follows ::

     pip install diffpy.pdfmorph


USING PDFmorph
------------------------------------------------------------------------

For detailed instructions and full tutorial, consult online documentation.

Once the required software, including PDFmorph is all installed, open
up a terminal and check installation has worked properly by running ::

	source activate pdfmorph_env      #if the environment isn't already active
	pdfmorph -h			  #get some helpful information
	pdfmorph --version

If installed correctly, this last command should return the version 
of PDFmorph that you have installed on your system. To begin using 
PDFmorph, run a command like ::

	pdfmorph <target PDF file> <morphed PDF file>

where both PDFs file are text files which contain PDF data, such as ``.gr``
or ``.cgr`` files that are produced by ``PDFgetX2``, ``PDFgetX3``, 
or ``PDFgui``. Though some file extensions other than ``.gr`` or ``.cgr``, 
but with the same content structure, have been shown to work with 
PDFmorph, it is recommended to stick with ``.gr`` files.

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

