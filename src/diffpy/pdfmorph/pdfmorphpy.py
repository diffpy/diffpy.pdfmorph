#!/usr/bin/env python

<<<<<<< Updated upstream
from pathlib import Path

from diffpy.pdfmorph.pdfmorphapp import create_option_parser, multiple_morphs, multiple_targets, single_morph
=======
from diffpy.pdfmorph.pdfmorphapp import create_option_parser, single_morph, multiple_targets, multiple_morphs
>>>>>>> Stashed changes


def pdfmorph(file1, file2, **kwargs):
    """Run PDFmorph at Python level.

    Parameters
    ----------
    file1: str
        Path-like object to the file to be morphed.
    file2: str
        Path-like object to the target file.
    kwargs: dict
        See the PDFmorph manual for options.

    Returns
    -------
    dict:
        Summary of morphs.
    """

    parser = create_option_parser()

    inputs = []
    for key, value in kwargs.items():
        inputs.append(f"--{key}")
        inputs.append(f"{value}")
    (opts, pargs) = parser.parse_args(inputs)
    pargs = [file1, file2]

    return single_morph(parser, opts, pargs)


def pdfmorph_multiple_targets(file, dir, **kwargs):
    """Run PDFmorph with multiple targets at Python level.

    Parameters
    ----------
    file1: str
        Path-like object to the file to be morphed.
    file2: str
        Path-like object to the target file.
    kwargs: dict
        See the PDFmorph manual for options.

    Returns
    -------
    dict:
        Summary of morphs.
    """

    parser = create_option_parser()

    inputs = []
    for key, value in kwargs.items():
        inputs.append(f"--{key}")
        inputs.append(f"{value}")
    (opts, pargs) = parser.parse_args(inputs)
    pargs = [file, dir]

    return multiple_targets(parser, opts, pargs)


def pdfmorph_multiple_morphs(dir, file, **kwargs):
    """Run PDFmorph for multiple morphs at Python level.

    Parameters
    ----------
    file1: str
        Path-like object to the file to be morphed.
    file2: str
        Path-like object to the target file.
    kwargs: dict
        See the PDFmorph manual for options.

    Returns
    -------
    dict:
        Summary of morphs.
    """

    parser = create_option_parser()

    inputs = []
    for key, value in kwargs.items():
        inputs.append(f"--{key}")
        inputs.append(f"{value}")
    (opts, pargs) = parser.parse_args(inputs)
    pargs = [dir, file]

    return multiple_morphs(parser, opts, pargs)
