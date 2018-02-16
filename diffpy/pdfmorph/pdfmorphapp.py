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

import numpy
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
    parser.add_option('-s', '--save', metavar="FILE", dest="savefile",
            help="Save manipulated PDF from FILE1 to FILE.")
    parser.add_option('--rmin', type="float",
            help="Minimum r-value to use for PDF comparisons.")
    parser.add_option('--rmax', type="float",
            help="Maximum r-value to use for PDF comparisons.")
    parser.add_option('--pearson', action="store_true", dest="pearson",
            help="Maximize agreement in the Pearson function. Note that this is insensitive to scale.")
    parser.add_option('--addpearson', action="store_true", dest="addpearson",
            help="""Maximize agreement in the Pearson function as well as
minimizing the residual.""")


    # Manipulations
    group = optparse.OptionGroup(parser, "Manipulations",
            """These options select the manipulations that are to be applied to
the PDF from FILE1. The passed values will be refined unless specifically
excluded with the -a or -x options.""")
    parser.add_option_group(group)
    group.add_option('-a', '--apply', action="store_false", dest="refine",
            help="Apply manipulations but do not refine.")
    group.add_option('-x', '--exclude', action="append", dest="exclude",
            metavar="MANIP",
            help="""Exclude a manipulation from refinement by name. This can
appear multiple times.""")
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
            help="Dampen PDF by a factor QDAMP. (See PDFGui manual.)")
    group.add_option('--radius', type="float", metavar="RADIUS",
            help="""Apply characteristic function of sphere with radius RADIUS.
If PRADIUS is also specified, instead apply characteristic function of spheroid with equatorial radius RADIUS and polar radius PRADIUS.""")
    group.add_option('--pradius', type="float", metavar="PRADIUS",
            help="""Apply characteristic function of spheroid with equatorial
radius RADIUS and polar radius PRADIUS. If only PRADIUS is specified, instead apply characteristic function of sphere with radius PRADIUS.""")
    group.add_option('--iradius', type="float", metavar="IRADIUS",
            help="""Apply inverse characteristic function of sphere with radius IRADIUS.  If IPRADIUS is also specified, instead apply inverse characteristic function of spheroid with equatorial radius IRADIUS and polar radius IPRADIUS.""")
    group.add_option('--ipradius', type="float", metavar="IPRADIUS",
            help="""Apply inverse characteristic function of spheroid with equatorial radius IRADIUS and polar radius IPRADIUS. If only IPRADIUS is specified, instead apply inverse characteristic function of sphere with radius IPRADIUS.""")

    # Plot Options
    group = optparse.OptionGroup(parser, "Plot Options",
            """These options control plotting.""")
    parser.add_option_group(group)
    group.add_option('-n', '--noplot', action="store_false", dest="plot",
            help="Do not show the plot.")
    group.add_option('--pmin', type="float",
            help="Minimum r-value to plot. Defaults to RMIN.")
    group.add_option('--pmax', type="float",
            help="Maximum r-value to plot. Defaults to RMAX.")
    group.add_option('--maglim', type="float",
            help="Magnify plot curves beyond MAGLIM by MAG.")
    group.add_option('--mag', type="float",
            help="Magnify plot curves beyond MAGLIM by MAG.")


    # Defaults
    parser.set_defaults(plot=True)
    parser.set_defaults(refine=True)
    parser.set_defaults(pearson=False)
    parser.set_defaults(addpearson=False)
    parser.set_defaults(mag=5)

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
    config = {}
    config["rmin"] = opts.rmin
    config["rmax"] = opts.rmax
    config["rstep"] = None
    if opts.rmin is not None and opts.rmax is not None and \
            opts.rmax <= opts.rmin:
        e = "rmin must be less than rmax"
        parser.error(e)

    # Set up the morphs
    chain = morphs.MorphChain(config)
    # Add the r-range morph, we will remove it when saving and plotting
    chain.append( morphs.MorphRGrid() )
    refpars = []

    ## Scale
    if opts.scale is not None:
        chain.append( morphs.MorphScale() )
        config["scale"] = opts.scale
        refpars.append("scale")
    ## Stretch
    if opts.stretch is not None:
        chain.append( morphs.MorphStretch() )
        config["stretch"] = opts.stretch
        refpars.append("stretch")
    ## Smear
    if opts.smear is not None:
        chain.append( morphs.MorphXtalPDFtoRDF() )
        chain.append( morphs.MorphSmear() )
        chain.append( morphs.MorphXtalRDFtoPDF() )
        refpars.append("smear")
        config["smear"] = opts.smear
        config["baselineslope"] = opts.baselineslope
        if opts.baselineslope is None:
            refpars.append("baselineslope")
            config["baselineslope"] = -0.5
    ## Size
    radii = [opts.radius, opts.pradius]
    nrad = 2 - radii.count(None)
    if nrad == 1:
        radii.remove(None)
        config["radius"] = radii[0]
        chain.append( morphs.MorphSphere() )
        refpars.append("radius")
    elif nrad == 2:
        config["radius"] = radii[0]
        refpars.append("radius")
        config["pradius"] = radii[1]
        refpars.append("pradius")
        chain.append( morphs.MorphSpheroid() )
    iradii = [opts.iradius, opts.ipradius]
    inrad = 2 - iradii.count(None)
    if inrad == 1:
        iradii.remove(None)
        config["iradius"] = iradii[0]
        chain.append( morphs.MorphISphere() )
        refpars.append("iradius")
    elif inrad == 2:
        config["iradius"] = iradii[0]
        refpars.append("iradius")
        config["ipradius"] = iradii[1]
        refpars.append("ipradius")
        chain.append( morphs.MorphISpheroid() )

    ## Resolution
    if opts.qdamp is not None:
        chain.append( morphs.MorphResolutionDamping() )
        refpars.append("qdamp")
        config["qdamp"] = opts.qdamp

    # Now remove non-refinable parameters
    if opts.exclude is not None:
        refpars = set(refpars) - set(opts.exclude)
        refpars = list(refpars)

    # Refine or execute the morph
    refiner = refine.Refiner(chain, xobj, yobj, xref, yref)
    if opts.pearson:
        refiner.residual = refiner._pearson
    if opts.addpearson:
        refiner.residual = refiner._addpearson
    if opts.refine and refpars:
        try:
            # This works better when we adjust scale and smear first.
            if "smear" in refpars:
                rptemp = ["smear"]
                if "scale" in refpars:
                    rptemp.append("scale")
                refiner.refine(*rptemp)
            refiner.refine(*refpars)
        except ValueError as e:
            parser.error(str(e))
    elif "smear" in refpars and opts.baselineslope is None:
        try:
            refiner.refine("baselineslope", baselineslope = -0.5)
        except ValueError as e:
            parser.error(str(e))
    else:
        chain(xobj, yobj, xref, yref)

    # Get Rw for the morph range
    rw = tools.getRw(chain)
    pcc = tools.getPearson(chain)
    # Replace the MorphRGrid with Morph identity
    chain[0] = morphs.Morph()
    chain(xobj, yobj, xref, yref)

    items = list(config.items())
    items.sort()
    output = "\n".join("# %s = %f"%i for i in items)
    output += "\n# Rw = %f" % rw
    output += "\n# Pearson = %f" % pcc
    print(output)
    print(config, refpars)
    if opts.savefile is not None:
        header = "# PDF created by pdfmorph\n"
        header += "# from %s\n" % os.path.abspath(pargs[0])

        header += output
        if opts.savefile == "-":
            outfile = sys.stdout
        else:
            outfile = open(opts.savefile, 'w')
        print(header, file=outfile)
        numpy.savetxt(outfile, numpy.transpose([chain.xobjout,
                                                chain.yobjout]))
        outfile.close()

    if opts.plot:
        pairlist = [chain.xyobjout, chain.xyrefout]
        labels = ["objective", "reference"]
        # Plot extent defaults to calculation extent
        pmin = opts.pmin if opts.pmin is not None else opts.rmin
        pmax = opts.pmax if opts.pmax is not None else opts.rmax
        maglim = opts.maglim
        mag = opts.mag
        pdfplot.comparePDFs(pairlist, labels, rmin = pmin, rmax = pmax, maglim
                = maglim, mag = mag, rw = rw)

    return


def getPDFFromFile(fn):
    from diffpy.pdfmorph.tools import readPDF
    try:
        r, gr = readPDF(fn)
    except IOError as errmsg:
        print("%s: %s" % (fn, errmsg), file=sys.stderr)
        sys.exit(1)
    except ValueError as errmsg:
        print("Cannot read %s" % fn, file=sys.stderr)
        sys.exit(1)

    return r, gr


if __name__ == "__main__":
    main()
