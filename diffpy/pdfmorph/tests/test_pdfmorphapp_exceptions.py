#!/usr/bin/env python


import unittest
import pytest
from pathlib import Path


from diffpy.pdfmorph.pdfmorphapp import create_option_parser, single_morph, multiple_morphs

thisfile = locals().get('__file__', 'file.py')
tests_dir = Path(thisfile).parent.resolve()
testdata_dir = tests_dir.joinpath("testdata")
testsequence_dir = testdata_dir.joinpath("testsequence")
nickel_PDF = testdata_dir.joinpath("nickel_ss0.01.cgr")
serial_JSON = testdata_dir.joinpath("testsequence_serialfile.json")

class TestExceptions(unittest.TestCase):
    def setUp(self):
        self.parser = create_option_parser()

    def test_length_exceptions(self):
        # Ensure only two pargs given for morphing
        (opts, pargs) = self.parser.parse_args(["toofewfiles"])
        with pytest.raises(SystemExit):
            single_morph(self.parser, opts, pargs, stdout_flag=False)
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)
        (opts, pargs) = self.parser.parse_args(["too", "many", "files"])
        with pytest.raises(SystemExit):
            single_morph(self.parser, opts, pargs, stdout_flag=False)
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Make sure rmax greater than rmin
        (opts, pargs) = self.parser.parse_args([f"{nickel_PDF}", f"{nickel_PDF}", "--rmin", "10", "--rmax", "1"])
        with pytest.raises(SystemExit):
            single_morph(self.parser, opts, pargs, stdout_flag=False)

        # Make sure we save to a directory that exists (user must create the directory if non-existing)
        (opts, pargs) = self.parser.parse_args([f"{nickel_PDF}", f"{nickel_PDF}", "-s",
                                                "/nonexisting_directory/no_way_this_exists/nonexisting_path"])
        with pytest.raises(SystemExit):
            single_morph(self.parser, opts, pargs, stdout_flag=False)
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Ensure first parg is a FILE and second parg is a DIRECTORY
        (opts, pargs) = self.parser.parse_args([f"{nickel_PDF}", f"{nickel_PDF}"])
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)
        (opts, pargs) = self.parser.parse_args([f"{testsequence_dir}", f"{testsequence_dir}"])
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Try sorting by non-existing field
        (opts, pargs) = self.parser.parse_args([f"{nickel_PDF}", f"{testsequence_dir}", "--sort-by", "fake_field"])
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)
        (opts, pargs) = self.parser.parse_args([f"{nickel_PDF}", f"{testsequence_dir}", "--sort-by", "fake_field",
                                               "--serial-file", f"{serial_JSON}"])
        with pytest.raises(SystemExit):
            multiple_morphs(self.parser, opts, pargs, stdout_flag=False)
