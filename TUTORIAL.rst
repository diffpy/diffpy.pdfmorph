PDFmorph Tutorial
#################

Welcome! This will be a quick tutorial to accquaint users with PDFmorph
and some of what it can do. 

As we described in the README and installation instructions, please make
sure that you are familiar with working with your command line terminal
before using this application.

Before you've started this tutorial, please ensure that you've installed
all necessary software and dependencies.

PDFmorph Example
----------------

	1. Open your Terminal or Command Prompt.

	2. It it's not active already, activate your PDFmorph-equipped 
	   conda environment by typing in ::
	
		source activate <pdfmorph_env>

	   on Linux or ``activate <pdfmorph_env>`` on Windows.

		* If you need to list your available conda environments,
		  run the command ``conda info --envs`` or 
		  ``conda env list``

	3. Change directories with the ``cd`` command to a directory
	   containing PDF files. For instance, I will use the file
	   "ni_qmax25.cgr", found `here<https://github.com/diffpy/diffpy.pdfmorph/tree/master/tests/testdata>`_,
	   so I will run ``cd ~/diffpy.pdfmorph/diffpy/pdfmorph/tests/testdata``

	4. Using this file for an example (you can download it from the
	   link above!), run the following command ::

		pdfmorph ni_qmax25.cgr ni_qmax25.cgr

	   This should produce an image like this ::

		.. figure:: doc/images/morph_ex1.png
			:align: center

	   A few things to note:

		* The green line (the difference curve) is flat because
		  in this example, we used the same PDF twice (so, there
		  is no difference)

		* The red curve is the taget PDF, and the blue circles
		  represent the morphed PDF; this will become clearer 
		  with the next example.

	5. Now, using the files "ni_qmax25_e17.5_p5.0.cgr" as our target
	   and "ni_qmax25_psize30.cgr" as our morphed PDF (available 
	   from the same source as above), run the following to see the 
	   program's "morphing" capabilities ::

		pdfmorph ni_qmax25_e17.5_p5.0.cgr ni_qmax25_psize30.cgr

	   This should produce an image like this :: 

		.. figure:: doc/images/morph_ex2.png
			:align: center

	   Note how the difference curve is now showing the difference
	   between the two PDFs, after the program has "morphed" the 
	   second PDF to the target PDF.

	6. Now, try using your own data! Be sure to list the higher
	   temperature PDF as the target and the lower temperature 
	   PDF as the morphed pdf. Once you've selected your files, run ::

		pdfmorph <targetPDF> <morphedPDF>

Additional PDFmorph Features
----------------------------

Now that you've seen the capabilities of PDFmorph at its base level, 
see how you can modify the behavior of the program by running ::

	pdfmorph --help

This will generate an additional list of changes that you can make
and values that you can provide the program.

You can add any of these "options" by placing them before your two 
filenames. ::

	pdfmorph [options] <testfile 1> <testfile 2>

For example, running the command ::

	pdfmorph --scale=0.5 --smear=0.5 <targetPDF> <morphedPDF>

will scale targetPDF by a factor of 0.5 and will smear its peaks with a
Gaussian of width 0.5.

When the program fits these parameters without user input, it decides 
their values based on internal algorithmic calculations. When the user 
inputs these values, it overrides the "choice" that the program would 
make.

Using the list provided by running ``pdfmorph --help``, you should now 
be able to "morph" your PDFs in a number of highly customizable ways.

Bug Reports
-----------

Please enjoy using our software! If you come accross any bugs in the 
application, please report them to diffpy-dev@googlegroups.com
