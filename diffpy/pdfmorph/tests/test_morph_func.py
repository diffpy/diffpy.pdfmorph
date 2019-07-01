import pytest
import numpy as np
from diffpy.pdfmorph import pdfmorph, morph_default_config
from diffpy.pdfmorph.tests.test_morphstretch import heaviside

def test_stretch_with_morphfunc():
    #    # use the same setup as test_moprhchain
    lb, ub = 1, 2
    xref = np.arange(0.01, 5, 0.01)
    yref = heaviside(xref, lb, ub)
    # stretch 30% 
    stretch = 0.3
    xobj = xref.copy()
    yobj = heaviside(xref, lb * (1 + stretch), ub * (1 + stretch))
    cfg = morph_default_config(stretch=0.1) # off init
    morph_rv = pdfmorph(xobj, yobj, xref, yref, **cfg)
    morphed_cfg = morph_rv['morphed_config']
    # test morphed result
    assert np.allclose(stretch, abs(morphed_cfg['stretch']), 1) 
    # assert residual
    x1, y1, x0, y0 = morph_rv['morph_chain'].xyallout
    assert np.allclose(x0, x1)
    assert np.allclose(y0, y1)
