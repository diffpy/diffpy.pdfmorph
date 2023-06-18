#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
# testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphscale import MorphScale


class TestMorphScale(unittest.TestCase):
    def setUp(self):
        self.x_morph = numpy.arange(0.01, 5, 0.01)
        self.y_morph = numpy.ones_like(self.x_morph)
        self.x_target = numpy.arange(0.01, 5, 0.01)
        self.y_target = 3 * numpy.ones_like(self.x_target)
        return

    def test_morph(self):
        """check MorphScale.morph()"""
        config = {"scale": 2.0}
        morph = MorphScale(config)

        x_morph, y_morph, x_target, y_target = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)

        self.assertTrue(numpy.allclose(2 * self.y_morph, y_morph))
        self.assertTrue(numpy.allclose(self.y_target, y_target))
        return


# End of class TestMorphScale

if __name__ == '__main__':
    unittest.main()

# End of file
