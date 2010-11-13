#!/usr/bin/env python
##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

import sys
import os
import os.path


from diffpy.pdfmorph import __version__
import diffpy.pdfmorph.tools as tools
import diffpy.pdfmorph.pdfplot as pdfplot
import diffpy.pdfmorph.morphs as morphs
import diffpy.pdfmorph.refine as refine

__id__ = "$Id$"

def createOptionParser():

    import optparse
    parser = optparse.OptionParser(
        usage = '\n'.join([
        "%prog [options] FILE1 FILE2",
        "Manipulate and compare PDFs.",
        ]),
        epilog="Please report bugs to diffpy-dev@googlegroups.com."
        )

    parser.add_option('-V', '--version', action="version",
        help="Show program version and exit.")
    parser.version = __version__
    parser.add_option('-a', '--apply', action="store_false", dest="refine",
            help="Apply manipulations but do not refine.")
    parser.add_option('-x', '--exclude', action="append", dest="exclude",
            metavar="MANIP",
            help="""Exclude a manipulation from refinement by name. This can
appear multiple times.""")
    parser.add_option('-n', '--noplot', action="store_false", dest="plot",
            help="Do not show the plot.")
    parser.add_option('-s', '--save', metavar="FILE", dest="savefile",
            help="Save manipulated PDF from FILE1 to FILE.")
    parser.add_option('--rmin', type="float",
            help="Minimum r-value to use for PDF comparisons.")
    parser.add_option('--rmax', type="float",
            help="Maximum r-value to use for PDF comparisons.")
    parser.add_option('--pmin', type="float",
            help="Minimum r-value to plot. Defaults to rmin.")
    parser.add_option('--pmax', type="float",
            help="Maximum r-value to plot. Defaults to rmax.")

    # Manipulations
    group = optparse.OptionGroup(parser, "Manipulations",
            """These options select the manipulations that are to be applied to
the PDF from FILE1. The passed values will be refined unless specifically
excluded with the -a or -x options.""")
    parser.add_option_group(group)
    group.add_option('--scale', type="float", metavar="SCALE",
            help="Apply scale factor SCALE.")
    group.add_option('--smear', type="float", metavar="SMEAR",
            help="Smear peaks with a Gaussian of width SMEAR.")
    group.add_option('--stretch', type="float", metavar="STRETCH",
            help="Stretch PDF by a fraction STRETCH.")
    group.add_option('--slope', type="float", dest="baselineslope",
            help="""Slope of the baseline. This is used when applying the smear
factor. It will be estimated if not provided.""")
    group.add_option('--qdamp', type="float", metavar="QDAMP",
            help="Dampen PDF by a factor QDAMP.")
    group.add_option('--radius', type="float", metavar="RADIUS",
            help="Apply characteristic function of sphere with radius RADIUS.")
    group.add_option('--eradius', type="float", metavar="ERADIUS",
            help="""Apply characteristic function of spheroid with equatorial
radius ERADIUS and polar radius PRADIUS. If only one of these is given, then
use a sphere instead.""")
    group.add_option('--pradius', type="float", metavar="PRADIUS",
            help="""Apply characteristic function of spheroid with equatorial
radius ERADIUS and polar radius PRADIUS. If only one of these is given, then
use a sphere instead.""")

    # Defaults
    parser.set_defaults(plot=True)
    parser.set_defaults(refine=True)

    return parser

def main():
    parser = createOptionParser()
    (opts, pargs) = parser.parse_args()

    if len(pargs) != 2:
        parser.error("You must supply FILE1 and FILE2")

    # Get the PDFs
    xobj, yobj = getPDFFromFile(pargs[0])
    xref, yref = getPDFFromFile(pargs[1])

    # Get configuration values
    pars = []
    for klass in morphs.morphs:
        pars.extend(klass.parnames)
    pars = set(pars)
    keys = [p for p in pars if hasattr(opts, p)]
    vals = [getattr(opts, k) for k in keys]
    items = [(k, v) for k, v in zip(keys, vals) if v is not None]
    config = dict(items)
    # We'll need these as well
    config.setdefault("rmin", None)
    config.setdefault("rmax", None)
    config.setdefault("rstep", None)

    # Set up the morphs
    chain = morphs.MorphChain(config)
    # Add the r-range morph, we will remove it when saving and plotting
    chain.append( morphs.MorphRGrid() )
    refpars = []
    if "scale" in config:
        chain.append( morphs.MorphScale() )
        refpars.append("scale")
    if "stretch" in config:
        chain.append( morphs.MorphStretch() )
        refpars.append("stretch")
    if "smear" in config:
        chain.append( morphs.MorphXtalPDFtoRDF() )
        chain.append( morphs.MorphSmear() )
        chain.append( morphs.MorphXtalRDFtoPDF() )
        refpars.append("smear")
        refpars.append("baselineslope")
        config.setdefault("baselineslope", -0.5)
    # We need exactly one of "radius", "eradius" or "pradius"
    radii = [config.get("eradius"), config.get("pradius")]
    rad = None
    if "radius" in config:
        rad = config["radius"]
    elif radii.count(None) == 1:
        radii.remove(None)
        rad = radii[0]
    if rad is not None:
        config["radius"] = rad
        chain.append( morphs.MorphSphere() )
        refpars.append("radius")
    elif radii.count(None) == 0:
        chain.append( morphs.MorphSpheroid() )
        refpars.append("eradius")
        refpars.append("pradius")
    if "qdamp" in config:
        chain.append( MorphResolutionDamping() )
        refpars.append("qdamp")

    # Now remove non-refinable parameters
    if opts.exclude is not None:
        refpars = set(refpars) - set(opts.exclude)
        refpars = list(refpars)

    # Refine or execute the morph
    if opts.refine and refpars:
        try:
            # This works better when we adjust scale and smear first.
            if "smear" in refpars:
                rptemp = ["smear"]
                if "scale" in refpars:
                    rptemp.append("scale")
                refine.refine(chain, xobj, yobj, xref, yref, *rptemp)
            refine.refine(chain, xobj, yobj, xref, yref, *refpars)
        except ValueError, e:
            parser.error(str(e))
    elif "smear" in refpars and opts.baselineslope is None:
        try:
            refine.refine(chain, xobj, yobj, xref, yref, "baselineslope",
                    baselineslope = -0.5)
        except ValueError, e:
            parser.error(str(e))
    else:
        chain(xobj, yobj, xref, yref)

    # Get Rw for the morph range
    rw = tools.getRw(chain)
    # Replace the MorphRGrid with Morph identity
    chain[0] = morphs.Morph()
    chain(xobj, yobj, xref, yref)

    items = config.items()
    items.sort()
    output = "\n".join("# %s = %f"%i for i in items)
    output += "\n# Rw = %f" % rw
    print output
    if opts.savefile is not None:
        header = "# PDF created by pdfmorph\n"
        header += "# from %s\n" % os.path.abspath(pargs[0])

        header += output
        outfile = file(opts.savefile, 'w')
        print >> outfile, header
        import numpy
        numpy.savetxt(outfile, zip(chain.xobjout, chain.yobjout))
        outfile.close()

    if opts.plot:
        pairlist = [chain.xyobjout, chain.xyrefout]
        labels = ["objective", "reference"]
        pmin = opts.pmin
        pmin = opts.pmin if opts.pmin is not None else opts.rmin
        pmax = opts.pmax if opts.pmax is not None else opts.rmax
        pdfplot.comparePDFs(pairlist, labels, rmin = pmin, rmax = pmax)

    return


def getPDFFromFile(fn):
    from diffpy.pdfmorph.tools import readPDF
    try:
        r, gr = readPDF(fn)
    except IOError, (errno, errmsg):
        print >> sys.stderr, "%s: %s" % (fn, errmsg)
        sys.exit(1)
    except ValueError, errmsg:
        print >> sys.stderr, "Cannot read %s" % fn
        sys.exit(1)

    return r, gr


if __name__ == "__main__":
    main()
