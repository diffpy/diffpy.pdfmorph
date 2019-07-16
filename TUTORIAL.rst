PDFmorph Tutorial
=================

Welcome! This will be a quick tutorial to accquaint users with PDFmorph
and some of what it can do. 

As we described in the README and installation instructions, please make
sure that you are familiar with working with your command line terminal
before using this application.

After all of the necessary software is installed, activate your PDFmorph-
equipped conda environment and change into a directory containing at
least two PDF files. If you need some test files to help you get started,
check `here<https://github.com/diffpy/diffpy.pdfmorph/tree/master/tests/testdata>`_.

Once you have two PDF files, run the command ::

	pdfmorph <testfile 1> <testfile 2>

and observe. PDFmorph should pop up a graph of your PDF data "morphed"
together, with a difference curve underneath.

To see the difference curve working, run ::

	pdfmorph <testfile 1> <testfile 1>

and see the difference curve completely flattened. 


Additional PDFmorph Features
----------------------------

Finally, see that by running ::

	pdfmorph --help

a list of additional modifications that you can run in your PDFmorph
program is generated. 

You can add any of these "options" by placing them before your two 
filenames. ::

	pdfmorph [options] <testfile 1> <testfile 2>

For example, running the command ::

	pdfmorph --scale=0.5 --smear=0.5 <testfile 1> <testfile 2>

will scale testfile 1 by a factor of 0.5 and will smear its peaks with a
Gaussian of width 0.5.

Using the list provided by running ``pdfmorph --help``, you should now 
be able to "morph" your PDFs in a number of highly customizable ways.

Bug Reports
-----------

Please enjoy using our software! If you come accross any bugs in the 
application, please report them to diffpy-dev@googlegroups.com
