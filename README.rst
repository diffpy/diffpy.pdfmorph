image here
image target here

image here
image target here


PDFmorph
========================================================================
add description, sample below
Code package for morphin' atomic pair distribution functions.

PDFmorph is a user-friendly software package. [more info here]


REQUIREMENTS
------------------------------------------------------------------------

PDFmorph requires Python 3.7 and several third party libraries 
that are used by PDFmorph and its components.

* NumPy        - library for scientific computing with Python
* matplotlib   - Python 2D plotting library
* [insert more requirements here]

We recommend to use 'Anaconda Python <https://ww.anaconda.com/download>'_
which allows to conveniently install PDFmorph and all its software
dependencies with a single command. For other Python distributions
it is necessary to install the required software separately. As an
example, on Ubuntu Linux some of the required software can be
installed using ::

     sudo apt-get install \
         python-setuptools python-wxtools python-numpy \
         python-matplotlib

To install the remaining packages see the installation instructions
at their respective web pages.


INSTALLATION
------------------------------------------------------------------------

The preferred method is to use Anaconda Python and install from the
"diffpy" channel of Anaconda packages ::

     conda config --add channels diffpy
     conda install diffpy.pdfmorph

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

[insert project page here, when it exists]

or email Professor Simon Billinge at sb2896@columbia.edu
