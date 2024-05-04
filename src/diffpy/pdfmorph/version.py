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

"""Definition of __version__ and __date__ for diffpy.pdfmorph.
"""


# obtain version information
from importlib.metadata import version

__version__ = version('diffpy.pdfmorph')

# we assume that tag_date was used and __version__ ends in YYYYMMDD
__date__ = __version__[-8:-4] + '-' + __version__[-4:-2] + '-' + __version__[-2:]

# End of file
