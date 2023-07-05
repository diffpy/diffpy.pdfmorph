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

from __future__ import print_function

import sys
from pathlib import Path

import numpy
from diffpy.pdfmorph.version import __version__
import diffpy.pdfmorph.tools as tools
import diffpy.pdfmorph.pdfplot as pdfplot
import diffpy.pdfmorph.morphs as morphs
import diffpy.pdfmorph.morph_helpers as helpers
import diffpy.pdfmorph.refine as refine


def create_option_parser():
    import optparse
    prog_short = Path(sys.argv[0]).name  # Program name, compatible w/ all OS paths

    class CustomParser(optparse.OptionParser):
        def __init__(self, *args, **kwargs):
            super(CustomParser, self).__init__(*args, **kwargs)

        def custom_error(self, msg):
            """custom_error(msg : string)

            Print a message incorporating 'msg' to stderr and exit.
            Does not print usage.
            """
            self.exit(2, "%s: error: %s\n" % (self.get_prog_name(), msg))

    parser = CustomParser(
        usage='\n'.join(
            [
                "%prog [options] FILE1 FILE2",
                "Manipulate and compare PDFs.",
                "Use --help for help.",
            ]
        ),
        epilog="Please report bugs to diffpy-dev@googlegroups.com.",
    )

    parser.add_option(
        '-V', '--version', action="version", help="Show program version and exit."
    )
    parser.version = __version__
    parser.add_option(
        '-s',
        '--save',
        metavar="SFILE",
        dest="savefile",
        help="Save manipulated PDF from FILE1 to SFILE. Use \'-\' for stdout.",
    )
    parser.add_option(
        '--sequence',
        dest="sequence",
        action="store_true",
        help=f"""Changes usage to \'{prog_short} [options] FILE DIRECTORY\'. FILE
will be morphed with each file in DIRECTORY as target.
Files in directory are sorted by alphabetical order unless
--temperature is enabled. Plotting and saving are disabled
when this option is enabled.""",
    )
    parser.add_option(
        '--temperature',
        dest="temperature_sort",
        action="store_true",
        help="""Used with --sequence to sort files in DIRECTORY by temperature.
File names in DIRECTORY should end in _#K.gr or _#K.cgr
to use this option.""",
    )
    parser.add_option(
        '--rmin', type="float", help="Minimum r-value to use for PDF comparisons."
    )
    parser.add_option(
        '--rmax', type="float", help="Maximum r-value to use for PDF comparisons."
    )
    parser.add_option(
        '--pearson',
        action="store_true",
        dest="pearson",
        help="Maximize agreement in the Pearson function. Note that this is insensitive to scale.",
    )
    parser.add_option(
        '--addpearson',
        action="store_true",
        dest="addpearson",
        help="""Maximize agreement in the Pearson function as well as
minimizing the residual.""",
    )

    # Manipulations
    group = optparse.OptionGroup(
        parser,
        "Manipulations",
        """These options select the manipulations that are to be applied to
the PDF from FILE1. The passed values will be refined unless specifically
excluded with the -a or -x options. If no option is specified, the PDFs from FILE1 and FILE2 will
be plotted without any manipulations.""",
    )
    parser.add_option_group(group)
    group.add_option(
        '-a',
        '--apply',
        action="store_false",
        dest="refine",
        help="Apply manipulations but do not refine.",
    )
    group.add_option(
        '-x',
        '--exclude',
        action="append",
        dest="exclude",
        metavar="MANIP",
        help="""Exclude a manipulation from refinement by name. This can
appear multiple times.""",
    )
    group.add_option(
        '--scale', type="float", metavar="SCALE", help="Apply scale factor SCALE."
    )
    group.add_option(
        '--smear',
        type="float",
        metavar="SMEAR",
        help="Smear peaks with a Gaussian of width SMEAR.",
    )
    group.add_option(
        '--stretch',
        type="float",
        metavar="STRETCH",
        help="Stretch PDF by a fraction STRETCH.",
    )
    group.add_option(
        '--slope',
        type="float",
        dest="baselineslope",
        help="""Slope of the baseline. This is used when applying the smear
factor. It will be estimated if not provided.""",
    )
    group.add_option(
        '--qdamp',
        type="float",
        metavar="QDAMP",
        help="Dampen PDF by a factor QDAMP. (See PDFGui manual.)",
    )
    group.add_option(
        '--radius',
        type="float",
        metavar="RADIUS",
        help="""Apply characteristic function of sphere with radius RADIUS.
If PRADIUS is also specified, instead apply characteristic function of spheroid with equatorial radius RADIUS and polar radius PRADIUS.""",
    )
    group.add_option(
        '--pradius',
        type="float",
        metavar="PRADIUS",
        help="""Apply characteristic function of spheroid with equatorial
radius RADIUS and polar radius PRADIUS. If only PRADIUS is specified, instead apply characteristic function of sphere with radius PRADIUS.""",
    )
    group.add_option(
        '--iradius',
        type="float",
        metavar="IRADIUS",
        help="""Apply inverse characteristic function of sphere with radius IRADIUS.  If IPRADIUS is also specified, instead apply inverse characteristic function of spheroid with equatorial radius IRADIUS and polar radius IPRADIUS.""",
    )
    group.add_option(
        '--ipradius',
        type="float",
        metavar="IPRADIUS",
        help="""Apply inverse characteristic function of spheroid with equatorial radius IRADIUS and polar radius IPRADIUS. If only IPRADIUS is specified, instead apply inverse characteristic function of sphere with radius IPRADIUS.""",
    )

    # Plot Options
    group = optparse.OptionGroup(
        parser, "Plot Options", """These options control plotting."""
    )
    parser.add_option_group(group)
    group.add_option(
        '-n',
        '--noplot',
        action="store_false",
        dest="plot",
        help="Do not show the plot.",
    )
    group.add_option(
        '--mlabel',
        metavar="MLABEL",
        dest="mlabel",
        help="Set label for morphed data to MLABEL on plot. Ignored if using file names as labels.",
    )
    group.add_option(
        '--tlabel',
        metavar="TLABEL",
        dest="tlabel",
        help="Set label for target data to TLABEL on plot. Ignored if using file names as labels.",
    )
    group.add_option(
        '--pmin', type="float", help="Minimum r-value to plot. Defaults to RMIN."
    )
    group.add_option(
        '--pmax', type="float", help="Maximum r-value to plot. Defaults to RMAX."
    )
    group.add_option(
        '--maglim', type="float", help="Magnify plot curves beyond MAGLIM by MAG."
    )
    group.add_option(
        '--mag', type="float", help="Magnify plot curves beyond MAGLIM by MAG."
    )
    group.add_option(
        '--lwidth', type="float", help="Line thickness of plotted curves."
    )

    # Defaults
    parser.set_defaults(sequence=False)
    parser.set_defaults(plot=True)
    parser.set_defaults(refine=True)
    parser.set_defaults(pearson=False)
    parser.set_defaults(addpearson=False)
    parser.set_defaults(mag=5)
    parser.set_defaults(lwidth=1.5)

    return parser


def main():
    parser = create_option_parser()
    (opts, pargs) = parser.parse_args()
    if opts.sequence:
        opts.plot = False  # Disable plotting
        opts.savefile = None  # Disable saving
        multiple_morphs(parser, opts, pargs, stdout_flag=True)
    else:
        single_morph(parser, opts, pargs, stdout_flag=True)


def multiple_morphs(parser, opts, pargs, stdout_flag):
    # Custom error messages since usage is distinct when --sequence tag is applied
    if len(pargs) < 2:
        parser.custom_error("You must supply FILE and DIRECTORY. Go to --help for usage.")
    elif len(pargs) > 2:
        parser.custom_error("Too many arguments. Go to --help for usage.")

    # Parse paths
    morph_file = Path(pargs[0])
    if not morph_file.is_file():
        parser.custom_error(f"{morph_file} is not a file. Go to --help for usage.")
    target_directory = Path(pargs[1])
    if not target_directory.is_dir():
        parser.custom_error(f"{target_directory} is not a directory. Go to --help for usage.")

    # Sort files in directory
    target_list = list(target_directory.iterdir())
    if opts.temperature_sort:
        # Sort by temperature
        target_list = tools.temperature_sort(target_list)
    else:
        # Default is alphabetical sort
        target_list.sort()

    # Morph morph_file against all other files in target_directory
    results = []
    for target_file in target_list:
        # Only morph morph_file against different files in target_directory
        if target_file.is_file and morph_file != target_file:
            results.append([
                target_file.name,
                single_morph(parser, opts, [morph_file, target_file], stdout_flag=False),
            ])

    # If print enabled
    if stdout_flag:
        # Input parameters used for every morph
        inputs = "\n# Input morphing parameters:"
        inputs += f"\n# scale = {opts.scale}"
        inputs += f"\n# stretch = {opts.stretch}"
        inputs += f"\n# smear = {opts.smear}"

        print(inputs)

        # Results from each morph
        for entry in results:
            outputs = f"\n# Target: {entry[0]}\n"
            outputs += "# Optimized morphing parameters:\n"
            outputs += "\n".join(f"# {i[0]} = {i[1]:.6f}" for i in entry[1])
            print(outputs)

    return results


def single_morph(parser, opts, pargs, stdout_flag):
    if len(pargs) < 2:
        parser.error("You must supply FILE1 and FILE2.")
    elif len(pargs) > 2:
        parser.error("Too many arguments.")

    # Get the PDFs
    x_morph, y_morph = getPDFFromFile(pargs[0])
    x_target, y_target = getPDFFromFile(pargs[1])

    # Get configuration values
    scale_in = 'None'
    stretch_in = 'None'
    smear_in = 'None'
    config = {}
    config["rmin"] = opts.rmin
    config["rmax"] = opts.rmax
    config["rstep"] = None
    if opts.rmin is not None and opts.rmax is not None and opts.rmax <= opts.rmin:
        e = "rmin must be less than rmax"
        parser.custom_error(e)

    # Set up the morphs
    chain = morphs.MorphChain(config)
    # Add the r-range morph, we will remove it when saving and plotting
    chain.append(morphs.MorphRGrid())
    refpars = []

    ## Scale
    if opts.scale is not None:
        scale_in = opts.scale
        chain.append(morphs.MorphScale())
        config["scale"] = opts.scale
        refpars.append("scale")
    ## Stretch
    if opts.stretch is not None:
        stretch_in = opts.stretch
        chain.append(morphs.MorphStretch())
        config["stretch"] = opts.stretch
        refpars.append("stretch")
    ## Smear
    if opts.smear is not None:
        smear_in = opts.smear
        chain.append(helpers.TransformXtalPDFtoRDF())
        chain.append(morphs.MorphSmear())
        chain.append(helpers.TransformXtalRDFtoPDF())
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
        config["radius"] = tools.nn_value(radii[0], "radius or pradius")
        chain.append(morphs.MorphSphere())
        refpars.append("radius")
    elif nrad == 2:
        config["radius"] = tools.nn_value(radii[0], "radius")
        refpars.append("radius")
        config["pradius"] = tools.nn_value(radii[1], "pradius")
        refpars.append("pradius")
        chain.append(morphs.MorphSpheroid())
    iradii = [opts.iradius, opts.ipradius]
    inrad = 2 - iradii.count(None)
    if inrad == 1:
        iradii.remove(None)
        config["iradius"] = tools.nn_value(iradii[0], "iradius or ipradius")
        chain.append(morphs.MorphISphere())
        refpars.append("iradius")
    elif inrad == 2:
        config["iradius"] = tools.nn_value(iradii[0], "iradius")
        refpars.append("iradius")
        config["ipradius"] = tools.nn_value(iradii[1], "ipradius")
        refpars.append("ipradius")
        chain.append(morphs.MorphISpheroid())

    ## Resolution
    if opts.qdamp is not None:
        chain.append(morphs.MorphResolutionDamping())
        refpars.append("qdamp")
        config["qdamp"] = opts.qdamp

    # Now remove non-refinable parameters
    if opts.exclude is not None:
        refpars = set(refpars) - set(opts.exclude)
        refpars = list(refpars)

    # Refine or execute the morph
    refiner = refine.Refiner(chain, x_morph, y_morph, x_target, y_target)
    if opts.pearson:
        refiner.residual = refiner._pearson
    if opts.addpearson:
        refiner.residual = refiner._add_pearson
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
            parser.custom_error(str(e))
    elif "smear" in refpars and opts.baselineslope is None:
        try:
            refiner.refine("baselineslope", baselineslope=-0.5)
        except ValueError as e:
            parser.custom_error(str(e))
    else:
        chain(x_morph, y_morph, x_target, y_target)

    # Get Rw for the morph range
    rw = tools.getRw(chain)
    pcc = tools.get_pearson(chain)
    # Replace the MorphRGrid with Morph identity
    chain[0] = morphs.Morph()
    chain(x_morph, y_morph, x_target, y_target)

    morphs_in = "\n# Input morphing parameters:"
    morphs_in += f"\n# scale = {scale_in}"
    morphs_in += f"\n# stretch = {stretch_in}"
    morphs_in += f"\n# smear = {smear_in}"

    # Output morph parameters
    morph_results = list(config.items())
    morph_results.sort()

    # Ensure Rw, Pearson last two outputs
    morph_results.append(("Rw", rw))
    morph_results.append(("Pearson", pcc))

    output = "\n# Optimized morphing parameters:\n"
    output += "\n".join(f"# {i[0]} = {i[1]:.6f}" for i in morph_results)

    # No stdout output when running morph sequence
    if stdout_flag:
        print(morphs_in)
        print(output)

    if opts.savefile is not None:
        path_name = Path(pargs[0]).absolute()
        header = "# PDF created by pdfmorph\n"
        header += f"# from {path_name}\n"

        header += morphs_in
        header += output

        # Print to stdout
        if opts.savefile == "-":
            outfile = sys.stdout
            print(header, file=outfile)
            numpy.savetxt(outfile, numpy.transpose([chain.x_morph_out, chain.y_morph_out]))
            # Do not close stdout

        # Save to file
        else:
            try:
                with open(opts.savefile, 'w') as outfile:
                    print(header, file=outfile)
                    numpy.savetxt(outfile, numpy.transpose([chain.x_morph_out, chain.y_morph_out]))
                    outfile.close()  # Close written file

                    path_name = Path(outfile.name).absolute()
                    save_message = f"\n# Morph saved to {path_name}"
                    print(save_message)
            except FileNotFoundError as e:
                save_fail_message = "\nUnable to save to designated location"
                print(save_fail_message)
                parser.custom_error(str(e))

    if opts.plot:
        pairlist = [chain.xy_morph_out, chain.xy_target_out]
        labels = [pargs[0], pargs[1]]  # Default is to use file names

        # If user chooses labels
        if opts.mlabel is not None:
            labels[0] = opts.mlabel
        if opts.tlabel is not None:
            labels[1] = opts.tlabel

        # Plot extent defaults to calculation extent
        pmin = opts.pmin if opts.pmin is not None else opts.rmin
        pmax = opts.pmax if opts.pmax is not None else opts.rmax
        maglim = opts.maglim
        mag = opts.mag
        l_width = opts.lwidth
        pdfplot.comparePDFs(
            pairlist, labels, rmin=pmin, rmax=pmax, maglim=maglim, mag=mag, rw=rw, l_width=l_width
        )

    return morph_results


def getPDFFromFile(fn):
    from diffpy.pdfmorph.tools import readPDF

    try:
        r, gr = readPDF(fn)
    except IOError as errmsg:
        print("%s: %s" % (fn, errmsg), file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Cannot read %s" % fn, file=sys.stderr)
        sys.exit(1)

    return r, gr


if __name__ == "__main__":
    main()
