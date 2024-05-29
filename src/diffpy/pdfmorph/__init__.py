#!/usr/bin/env python
##############################################################################
#
# pdfmorph          by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Tools for manipulating and comparing PDFs.
"""

# top-level import
from diffpy.pdfmorph.pdfmorph_api import morph_default_config, pdfmorph, plot_morph  # noqa: F401

# key used when saving multiple morphs
__save_morph_as__ = "save_morph_as"

# End of file
