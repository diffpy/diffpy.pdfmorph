#!/usr/bin/env python

"""Unit tests for tools.py
"""


import os
import pytest

import numpy

from pathlib import Path

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')
testsequence_dir = os.path.join(testdata_dir, 'testsequence')

import diffpy.pdfmorph.tools as tools


##############################################################################
class TestTools:
    @pytest.fixture
    def setup(self):
        morph_file = os.path.join(testdata_dir, "nickel_ss0.01.cgr")
        self.x_morph, self.y_morph = numpy.loadtxt(morph_file, unpack=True)
        self.rho0 = 0.0917132
        return

    def test_estimateBaselineSlope(self, setup):
        """check estimateBaselineSlope() using calculated data"""
        slope = tools.estimateBaselineSlope(self.x_morph, self.y_morph)
        slopecalc = -4 * numpy.pi * self.rho0
        assert numpy.allclose(slopecalc, slope, 1e-2)
        return

    def test_estimateScale(self, setup):
        """check estimateScale() using calculated data"""
        import random

        x = random.random()
        scale = tools.estimateScale(self.y_morph, x * self.y_morph)
        assert x, scale
        return

    def test_nn_value(self, setup):
        import random

        # Values with 6 and 7 decimals (limit of assertAlmostEqual)
        test_values = [10.0000001, 10.00000001, 0.9999999, 0.99999999]

        # Random values
        for i in range(100):
            test_values.append(random.uniform(0, 65535))

        # Check positive and negative
        for value in test_values:
            pytest.approx(tools.nn_value(value, name=None), abs(value))
            pytest.approx(tools.nn_value(-value, name=None), abs(-value))

    def test_temperature_sort(self, setup):
        sequence_files = [*os.listdir(testsequence_dir)]

        # Fisher-Yates randomization
        import random
        length = len(sequence_files)
        for i in range(length - 1, 0, -1):
            j = random.randint(0, i)
            sequence_files[i], sequence_files[j] = sequence_files[j], sequence_files[i]

        # Prepare and run through temperature_sort
        path_sequence = []
        for file in sequence_files:
            path_sequence.append(Path(file))
        sorted_path_sequence = tools.temperature_sort(path_sequence)
        sorted_sequence = []
        for path in sorted_path_sequence:
            sorted_sequence.append(path.name)

        # Temperature sort should produce same result as alphanumerical if leading character is removed
        sequence_files.sort(key=lambda entry: entry[2:])
        assert sequence_files == sorted_sequence


# End of class TestRoutines

if __name__ == '__main__':
    TestTools()

# End of file
