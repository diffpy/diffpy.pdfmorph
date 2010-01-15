#!/usr/bin/env python

import os.path

scriptname = os.path.basename(__file__)

__doc__ = """%(fn)s   Manipulate and compare PDFs.
Usage: %(fn)s [options] file1 file2

%(fn)s takes two PDF files, file1 and file2, and plots them on top of one
another, and produces a difference curve. Options may manipulate the PDF from
file1 before plotting.

Options:
  -h, --help      display this message
  -V, --version   show script version
  --automorph     broaden, expand and scale the PDF from file1 to best match
                  the PDF from file2 over the range defined by CMIN and CMAX.
  --broaden=SIG   broaden the PDF from file1 by Gaussian width SIG.
  --cmin=CMIN     the minimum r-value to use for PDF comparisons
  --cmax=CMAX     the maximum r-value to use for PDF comparisons
  --expand=EPS    the amount to expand the scale of the PDF from file1. This is
                  used to simulate isotropic expansion, where 1+EPS is the
                  expansion fraction.
  --noplot        do not show the plot
  --rmin=RMIN     the minimum r-value to show
  --rmax=RMAX     the maximum r-value to show
  --save=FILE     save full extent of manipulated PDF from file1 to FILE
  --scale=SCALE   A scale factor by which to multiply the PDF from file1. If
                  SCALE=auto, this will found automatically in order to match
                  the file1 PDF with the file2 PDF over the range defined by
                  CMIN and CMAX.

  Note that transforms are performed in the order of scale, expand, broaden.

Report bugs to diffpy-dev@googlegroups.com.
"""% {"fn" : scriptname }

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
                ["help", "version", "automorph", "broaden=", "expand=",
                    "cmin=", "cmax=", "save=", "rmin=", "rmax=", "scale=",
                    "noplot"])
    except getopt.GetoptError, errmsg:
        print >> sys.stderr, errmsg
        sys.exit(2)
    # process options
    cmin = None
    cmax = None
    eps=None
    noplot = False
    rmin = None
    rmax = None
    savefile = None
    scale=None
    sig = None
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
        elif "--broaden" == o:
            sig = getFloat(a, 'broaden')
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
        elif "--expand" == o:
            eps = getFloat(a, 'expand')

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
                cmin, rmax = cmax)
        morphed = True
    else:

        # rescale if requested, but not if we're auto-broadening
        if scale is not None:
            if scale == 'auto':
                scale = tools.estimatePDFScale(r1, gr1, r2, gr2, rmin=cmin,
                        rmax=cmax)
            gr1 *= scale
            morphed = True

        # expand if requested
        if eps is not None:
            gr1 = tools.expandSignal(r1, gr1, eps)
            morphed = True

        # broaden if requested, this might change and apply a new scale
        if sig is not None:
            sig, scale, gr1 = tools.autoBroadenPDF(r1, gr1, r2, gr2,
                    rmin = cmin, rmax = cmax)
            morphed = True

    # For recording purposes
    if scale is None:
        scale = 1
    if sig is None:
        sig = 0
    if eps is None:
        eps = 0

    output = "# scale = %f\n" % scale
    output += "# eps = %f\n" % eps
    output += "# sig = %f" % sig
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
        print >> sys.stderr ("Cannot read %s : " % (fn, errmsg))
        sys.exit(1)

    return r, gr


if __name__ == "__main__":
    main()
