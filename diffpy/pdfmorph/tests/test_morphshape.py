#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphshape import MorphSphere, MorphSpheroid


class TestMorphSphere(unittest.TestCase):
    def setUp(self):
        morph_file = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.x_morph, self.y_morph = numpy.loadtxt(morph_file, unpack=True)
        target_file = os.path.join(testdata_dir, "ni_qmax25_psize30.cgr")
        self.x_target, self.y_target = numpy.loadtxt(target_file, unpack=True)
        return

    def test_morph(self):
        """check MorphSphere.morph()"""
        config = {"radius": 17.5}
        morph = MorphSphere(config)

        x_morph, y_morph, x_target, y_target = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)

        self.assertTrue(numpy.allclose(self.y_target, y_target))
        self.assertTrue(numpy.allclose(y_morph, y_target))
        return


# End of class TestMorphSphere


class TestMorphSpheroid(unittest.TestCase):
    def setUp(self):
        morph_file = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.x_morph, self.y_morph = numpy.loadtxt(morph_file, unpack=True)
        target_file = os.path.join(testdata_dir, "ni_qmax25_e17.5_p5.0.cgr")
        self.x_target, self.y_target = numpy.loadtxt(target_file, unpack=True)
        return

    def test_morph(self):
        """check MorphSphere.morph()"""
        config = {
            "radius": 17.5,
            "pradius": 5.0,
        }
        morph = MorphSpheroid(config)

        x_morph, y_morph, x_target, y_target = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)

        self.assertTrue(numpy.allclose(self.y_target, y_target))
        self.assertTrue(numpy.allclose(y_morph, y_target))
        return


# End of class TestMorphSpheroid

if __name__ == '__main__':
    unittest.main()

# End of file
