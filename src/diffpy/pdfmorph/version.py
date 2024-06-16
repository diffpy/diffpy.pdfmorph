#!/usr/bin/env python
##############################################################################
#
# Structure         by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2008 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Pavol Juhas
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Definition of __version__ for diffpy.pdfmorph.
"""


# obtain version information
from importlib.metadata import version

__version__ = version("diffpy.pdfmorph")

# End of file
