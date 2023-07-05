#!/usr/bin/env python


import unittest
from pathlib import Path

from diffpy.pdfmorph.pdfmorphapp import create_option_parser, single_morph, multiple_morphs

thisfile = locals().get('__file__', 'file.py')
tests_dir = Path(thisfile).parent.resolve()
testsequence_dir = tests_dir.joinpath("testdata").joinpath("testsequence")


class TestMorphSequence(unittest.TestCase):
    def setUp(self):
        self.parser = create_option_parser()
        filenames = ["174K.gr", "180K.gr", "186K.gr", "192K.gr", "198K.gr", "204K.gr", "210K.gr"]
        (self.opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0", "-n"])
        self.testfiles = []
        for filename in filenames:
            self.testfiles.append(testsequence_dir.joinpath(filename))
        return

    def test_morphsequence(self):
        # Run multiple single morphs
        single_results = []
        morph_file = self.testfiles[-1]
        for target_file in self.testfiles[:-1]:
            pargs = [morph_file, target_file]
            single_results.append(single_morph(self.parser, self.opts, pargs, stdout_flag=False))
        pargs = [morph_file, testsequence_dir]

        # Run a morph sequence
        sequence_results = multiple_morphs(self.parser, self.opts, pargs, stdout_flag=False)

        # Compare results
        for idx in range(len(self.testfiles[:-1])):
            assert sequence_results[idx][1] == single_results[idx]


if __name__ == '__main__':
    unittest.main()
