#!/usr/bin/env python


import unittest
from pathlib import Path

from diffpy.pdfmorph.pdfmorphapp import create_option_parser, single_morph, multiple_morphs

thisfile = locals().get('__file__', 'file.py')
tests_dir = Path(thisfile).parent.resolve()
testdata_dir = tests_dir.joinpath("testdata")
testsequence_dir = testdata_dir.joinpath("testsequence")


class TestMorphSequence(unittest.TestCase):
    def setUp(self):
        self.parser = create_option_parser()
        filenames = ["g_174K.gr", "f_180K.gr", "e_186K.gr", "d_192K.gr", "c_198K.gr", "b_204K.gr", "a_210K.gr"]
        self.testfiles = []
        for filename in filenames:
            self.testfiles.append(testsequence_dir.joinpath(filename))
        return

    def test_morphsequence(self):
        # Parse arguments sorting by field
        (self.opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0",
                                                     "-n", "--sort-by", "temperature"])

        # Run multiple single morphs
        single_results = {}
        morph_file = self.testfiles[-1]
        for target_file in self.testfiles[:-1]:
            pargs = [morph_file, target_file]
            # store in same format of dictionary as multiple_morphs
            single_results.update({target_file.name: single_morph(self.parser, self.opts, pargs, stdout_flag=False)})
        pargs = [morph_file, testsequence_dir]

        # Run a morph sequence
        sequence_results = multiple_morphs(self.parser, self.opts, pargs, stdout_flag=False)

        # Compare results
        assert sequence_results == single_results

        # Check using a serial file produces the same result
        sfn = "testsequence_serialfile.json"
        s_file = testdata_dir.joinpath(sfn).resolve().as_posix()
        (self.opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0",
                                                     "-n", "--sort-by", "temperature",
                                                     "--serial-file", s_file])
        pargs = [morph_file, testsequence_dir]
        s_sequence_results = multiple_morphs(self.parser, self.opts, pargs, stdout_flag=False)
        assert s_sequence_results == sequence_results


if __name__ == '__main__':
    unittest.main()
