#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphresolution import MorphResolutionDamping


class TestMorphScale(unittest.TestCase):
    def setUp(self):
        morph_file = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.x_morph, self.y_morph = numpy.loadtxt(morph_file, unpack=True)
        target_file = os.path.join(testdata_dir, "ni_qmax25_qdamp0.01.cgr")
        self.x_target, self.y_target = numpy.loadtxt(target_file, unpack=True)
        return

    def test_morph(self):
        """check MorphScale.morph()"""
        config = {"qdamp": 0.01}
        morph = MorphResolutionDamping(config)

        x_morph, y_morph, x_target, y_target = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)

        self.assertTrue(numpy.allclose(self.y_target, y_target))
        self.assertTrue(numpy.allclose(y_morph, y_target))
        return


# End of class TestMorphScale

if __name__ == '__main__':
    unittest.main()

# End of file
