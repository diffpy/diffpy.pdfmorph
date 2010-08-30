#!/usr/bin/env python

import os.path

scriptname = os.path.basename(__file__)

__doc__ = """pdfmorph   Manipulate and compare PDFs.
Usage: pdfmorph [options] file1 file2

pdfmorph takes two PDF files, file1 and file2, and plots them on top of one
another, and produces a difference curve. Options may manipulate the PDF from
file1 before plotting.

Options:
  -h, --help      display this message
  -V, --version   show script version
  --automorph     smear, stretch and scale the PDF from file1 to best match
                  the PDF from file2 over the range defined by CMIN and CMAX.
  --cmin=CMIN     the minimum r-value to use for PDF comparisons
  --cmax=CMAX     the maximum r-value to use for PDF comparisons
  --noplot        do not show the plot
  --rmin=RMIN     the minimum r-value to show
  --rmax=RMAX     the maximum r-value to show
  --save=FILE     save full extent of manipulated PDF from file1 to FILE
  --scale=SCALE   A scale factor by which to multiply the PDF from file1. If
                  SCALE=auto, this will found automatically in order to match
                  the file1 PDF with the file2 PDF over the range defined by
                  CMIN and CMAX.
  --size=DIAM     apply a spherical attenuation factor to the PDF from file1.
                  If DIAM=auto, then figure out the best attenuation factor
                  while scaling the PDF.
  --smear=SIG     smear the PDF from file1 by Gaussian width SIG.
  --stretch=EPS   the amount to stretch the scale of the PDF from file1. This is
                  used to simulate isotropic expansion, where 1+EPS is the
                  expansion fraction.

  Note that transforms are performed in the order of scale, stretch, smear.

Report bugs to diffpy-dev@googlegroups.com.
"""

__id__ = "$Id$"

import sys
import os

from diffpy.pdfmorph import pdfplot, tools

def usage(style = None):
    """show usage info, for style=="brief" show only first 2 lines"""
    myname = os.path.basename(sys.argv[0])
    msg = __doc__
    if style == 'brief':
        msg = msg.split("\n")[1] + "\n" + \
                "Try `%s --help' for more information." % myname
    print msg
    return

def version():
    from diffpy.pdfmorph import __version__
    print __id__
    print "diffpy.pdfmorph", __version__

def main():
    import getopt
    # default parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hV",
                ["help", "version", "automorph", "cmin=", "cmax=", "save=",
                    "rmin=", "rmax=", "scale=", "size=", "smear=", "stretch=",
                    "noplot"])
    except getopt.GetoptError, errmsg:
        print >> sys.stderr, errmsg
        sys.exit(2)
    # process options
    cmin = None
    cmax = None
    eps = None
    noplot = False
    rmin = None
    rmax = None
    savefile = None
    scale = None
    sig = None
    size = None
    automorph = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-V", "--version"):
            version()
            sys.exit()
        elif "--automorph" == o:
            automorph = True
        elif "--smear" == o:
            sig = getFloat(a, 'smear')
        elif "--save" == o:
            savefile = a
        elif "--noplot" == o:
            noplot = True
        elif "--rmin" == o:
            rmin = getFloat(a, 'rmin')
        elif "--rmax" == o:
            rmax = getFloat(a, 'rmax')
        elif "--cmin" == o:
            cmin = getFloat(a, 'cmin')
        elif "--cmax" == o:
            cmax = getFloat(a, 'cmax')
        elif "--scale" == o:
            scale = a
            if scale != 'auto':
                scale = getFloat(a, 'scale')
        elif "--stretch" == o:
            eps = getFloat(a, 'stretch')
        elif "--size" == o:
            size = a
            if size != 'auto':
                size = getFloat(a, 'size')

    if len(args) != 2:
        usage('brief')
        sys.exit()

    file1, file2 = args
    labels = map(os.path.basename, args)

    r1, gr1 = getPDFFromFile(file1)
    r2, gr2 = getPDFFromFile(file2)

    morphed = False

    if automorph is True:
        scale, eps, sig, gr1 = tools.autoMorphPDF(r1, gr1, r2, gr2, rmin =
                cmin, rmax = cmax, scale = scale, eps = eps, sig = sig)
        morphed = True

    else:

        # rescale if requested, but not if we're auto-smearing
        if scale is not None:
            if scale == 'auto':
                scale = tools.estimateScale(r1, gr1, r2, gr2, rmin=cmin,
                        rmax=cmax)
            gr1 *= scale
            morphed = True

        # stretch if requested
        if eps is not None:
            gr1 = tools.expandSignal(r1, gr1, eps)
            morphed = True

        # smear if requested
        if sig is not None:
            gr1 = tools.broadenPDF(r1, gr1, sig)
            morphed = True

        if size is not None:
            if size == 'auto':
                size, scale = tools.estimateSize(r1, gr1, r2, gr2, rmin=cmin,
                        rmax=cmax, scale=scale)
            gr1 *= (scale or 1) * tools.sphericalFF(r1, size)


    # For recording purposes
    if scale is None:
        scale = 1
    if sig is None:
        sig = 0
    if eps is None:
        eps = 0
    if size is None:
        size = 0

    output = "# scale = %f\n" % scale
    output += "# eps = %f\n" % eps
    output += "# sig = %f\n" % sig
    output += "# size = %f" % size
    print output
    if savefile is not None:
        header = "# PDF created by %s\n" % scriptname
        header += "# from %s\n" % os.path.abspath(file1)
        header += output
        import numpy
        outfile = file(savefile, 'w')
        print >> outfile, header
        numpy.savetxt(outfile, zip(r1, gr1))
        outfile.close()

    # Now we can plot
    if not noplot:
        if morphed:
            labels[0] += " (morphed)"
        pdfplot.comparePDFs([(r1, gr1), (r2, gr2)],
                labels, rmin = rmin, rmax = rmax)
    return

def getFloat(val, name):
    f = val
    try: 
        f = float(val)
    except ValueError:
        msg = "Do not understand '%s' option"%name
        print >> sys.stderr, msg

    return f


def getPDFFromFile(fn):
    try:
        r, gr = tools.readPDF(fn)
    except IOError, (errno, errmsg):
        print >> sys.stderr, "%s: %s" % (fn, errmsg)
        sys.exit(1)
    except ValueError, errmsg:
        print >> sys.stderr, "Cannot read %s" % fn
        sys.exit(1)

    return r, gr


if __name__ == "__main__":
    main()
