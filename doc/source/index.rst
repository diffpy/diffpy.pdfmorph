PDFmorph Documentation
=============================

PDFmorph: An easy way to compare PDFs.

Sofwatware version 0.1.0.

Last updated July 15, 2019.

PDFmorph is a Python software package designed to increase the insight 
researchers can obtain from measured atomic pair distribution functions 
(PDFs) in a model-independent way. The program was designed to help a 
researcher answer the question: Has my material undergone a phase 
transition between these two measurements?

One approach is to compare the two PDFs in a plot and view the 
difference curve underneath. However, significant signal can be seen in 
the difference curve from benign effects such as thermal expansion (peak 
shifts) and increased thermal motion (peak broadening) or a change in 
scale due to differences in incident flux, for example. PDFmorph will 
do its best to correct for these benign effects before computing and 
plotting the difference curve. One measured PDF (typically that 
collected under higher temperature) is identified as the target PDF and 
the second PDF is then morphed by "stretching" (chaning the r-axis to 
simulate a uniform lattice expansion), "smearing" (broadening peaks 
through a uniform convolution to simulate increased thermal motion), and 
"scaling" (self-explanatory). PDFmorph will vary the amplitude of the 
morphing transformations to obtain the best fit between the morphed and 
the target PDFs, then plot them on top of each other with the difference 
plotted below.

There are also a few other morphing transformations in the program.

Finally, we note that PDFmorph should work on other spectra that are not 
PDFs, though it has not been extensively tested beyond the PDF.


Authors
-------

PDFmorph is developed by members of the Billinge Group at 
Columbia University and Brookhaven National Laboratory including 
Pavol Juhás, Christopher L. Farrow, Christopher Wright, Timothy Liu, 
Matthew Román, and Simon J. L. Billinge. 

For a detailed list of contributors, check `here 
<https://github.com/diffpy/diffpy.pdfmorph/graphs/contributors>`_.


Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   license
   release
   package



Indices
--------

* :ref:`genindex`
* :ref:`search`
