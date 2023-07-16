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
        filenames = ["g_174K.gr", "f_180K.gr", "e_186K.gr", "d_192K.gr", "c_198K.gr", "b_204K.gr", "a_210K.gr"]
        (self.opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0", "-n", "--temperature"])
        self.testfiles = []
        for filename in filenames:
            self.testfiles.append(testsequence_dir.joinpath(filename))
        return

    def test_parser_numerical(self):
        renamed_dests = {"slope": "baselineslope"}

        # Check values parsed correctly
        n_names = ["--rmin", "--rmax", "--scale", "--smear", "--stretch", "--slope", "--qdamp"]
        n_values = ["2.5", "40", "2.1", "-0.8", "0.0000005", "-0.0000005", ".00000003"]
        n_names.extend(["--radius", "--pradius", "--iradius", "--ipradius", "--pmin", "--pmax"])
        n_values.extend(["+0.5", "-0.2", "+.3", "-.1", "2.5", "40"])
        n_names.extend(["--lwidth", "--maglim", "--mag"])
        n_values.extend(["1.6", "50", "5"])
        n_total = len(n_names)
        n_input = []
        for idx in range(n_total):
            n_input.append(n_names[idx])
            n_input.append(n_values[idx])
        n_input.append("leftover")  # One leftover
        n_opts, n_args = self.parser.parse_args(n_input)
        n_opts_dict = vars(n_opts)
        for idx in range(n_total):
            n_parsed_name = n_names[idx][2:]
            n_parsed_val = n_opts_dict.get(n_parsed_name)
            if n_parsed_val is None:
                assert n_parsed_name in renamed_dests  # Ensure .get() failed due to destination renaming
                n_parsed_name = renamed_dests.get(n_parsed_name)
                n_parsed_val = n_opts_dict.get(n_parsed_name)
            assert isinstance(n_parsed_val, float)  # Check if is float
            assert n_parsed_val == float(n_values[idx])  # Check correct value parsed
        assert len(n_args) == 1  # Check one leftover

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
