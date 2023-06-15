#!/usr/bin/env python


import unittest
from diffpy.pdfmorph.pdfmorphapp import create_option_parser


class TestCreateOptionParser(unittest.TestCase):
    def setUp(self):
        self.parser = create_option_parser()
        return

    # Check numerical inputs parsed correctly into parser
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
