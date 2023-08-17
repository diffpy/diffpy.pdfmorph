#!/usr/bin/env python


import pytest
import filecmp
from pathlib import Path

from diffpy.pdfmorph.pdfmorphapp import create_option_parser, single_morph, multiple_morphs

thisfile = locals().get('__file__', 'file.py')
tests_dir = Path(thisfile).parent.resolve()
testdata_dir = tests_dir.joinpath("testdata")
testsequence_dir = testdata_dir.joinpath("testsequence")
testsaving_dir = testdata_dir.joinpath("testsaving")
test_saving_succinct = testsaving_dir.joinpath("succinct")
test_saving_verbose = testsaving_dir.joinpath("verbose")
tssf = testdata_dir.joinpath("testsequence_serialfile.json")


class TestMorphSequence:
    @pytest.fixture
    def setup_default(self):
        self.parser = create_option_parser()
        filenames = ["g_174K.gr", "f_180K.gr", "e_186K.gr", "d_192K.gr", "c_198K.gr", "b_204K.gr", "a_210K.gr"]
        self.testfiles = []
        for filename in filenames:
            self.testfiles.append(testsequence_dir.joinpath(filename))
        return

    def test_morphsequence(self, setup_default):
        # Parse arguments sorting by field
        (opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0",
                                                     "-n", "--sort-by", "temperature"])

        # Run multiple single morphs
        single_results = {}
        morph_file = self.testfiles[0]
        for target_file in self.testfiles[1:]:
            pargs = [morph_file, target_file]
            # store in same format of dictionary as multiple_morphs
            single_results.update({target_file.name: single_morph(self.parser, opts, pargs, stdout_flag=False)})
        pargs = [morph_file, testsequence_dir]

        # Run a morph sequence
        sequence_results = multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Compare results
        assert sequence_results == single_results

        # Check using a serial file produces the same result
        s_file = tssf.resolve().as_posix()
        (opts, pargs) = self.parser.parse_args(["--scale", "1", "--stretch", "0",
                                                "-n", "--sort-by", "temperature",
                                                "--serial-file", s_file])
        pargs = [morph_file, testsequence_dir]
        s_sequence_results = multiple_morphs(self.parser, opts, pargs, stdout_flag=False)
        assert s_sequence_results == sequence_results

    def test_morph_outputs(self, setup_default, tmp_path):
        morph_file = self.testfiles[0]
        target_file = self.testfiles[-1]

        # Save multiple succinct morphs
        tmp_succinct = tmp_path.joinpath("succinct")
        tmp_succinct_name = tmp_succinct.resolve().as_posix()

        (opts, pargs) = self.parser.parse_args(["--multiple", "--sort-by", "temperature", "-s", tmp_succinct_name,
                                                "-n", "--snf", tssf])
        pargs = [morph_file, testsequence_dir]
        multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Save a single succinct morph
        ssm = tmp_succinct.joinpath("single_succinct_morph.cgr")
        ssm_name = ssm.resolve().as_posix()
        (opts, pargs) = self.parser.parse_args(["-s", ssm_name, "-n"])
        pargs = [morph_file, target_file]
        single_morph(self.parser, opts, pargs, stdout_flag=False)

        # Check the saved files are the same for succinct
        common = []
        for item in tmp_succinct.glob('**/*.*'):
            common.append(item.resolve().as_posix())
        assert filecmp.cmpfiles(tmp_succinct, test_saving_succinct, common=common)

        # Save multiple succinct morphs
        tmp_verbose = tmp_path.joinpath("verbose")
        tmp_verbose_name = tmp_verbose.resolve().as_posix()

        (opts, pargs) = self.parser.parse_args(["--multiple", "--sort-by", "temperature", "-s", tmp_verbose_name,
                                                "-n", "--snf", tssf, "--verbose"])
        pargs = [morph_file, testsequence_dir]
        multiple_morphs(self.parser, opts, pargs, stdout_flag=False)

        # Save a single succinct morph
        ssm = tmp_verbose.joinpath("single_succinct_morph.cgr")
        ssm_name = ssm.resolve().as_posix()
        (opts, pargs) = self.parser.parse_args(["-s", ssm_name, "-n", "--verbose"])
        pargs = [morph_file, target_file]
        single_morph(self.parser, opts, pargs, stdout_flag=False)

        # Check the saved files are the same for verbose
        common = []
        for item in tmp_verbose.glob('**/*.*'):
            common.append(item.resolve().as_posix())
        assert filecmp.cmpfiles(tmp_verbose, test_saving_verbose, common=common)


if __name__ == '__main__':
    TestMorphSequence()
