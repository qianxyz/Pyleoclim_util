''' Tests for pyleoclim.core.ui.Scalogram

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}

Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
5. for more details, see https://docs.pytest.org/en/stable/usage.html
'''
import numpy as np
import pandas as pd

from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal

import pytest
import pyleoclim as pyleo

# Tests below
class TestUiScalogramSignifTest:
    ''' Tests for Scalogram.signif_test()
    '''

    @pytest.mark.parametrize('wave_method',['wwz','cwt'])
    def test_signif_test_t0(self, wave_method):
        ''' Test scalogram.signif_test() with default parameters
        '''
        ts = pyleo.utils.gen_ts(model='colored_noise',nt=500)
        scal = ts.wavelet(method=wave_method)
        scal_signif = scal.signif_test(number=5, qs = [0.8, 0.9, .95])
        scal_signif.plot(mute=True,signif_thresh=0.99)

    @pytest.mark.parametrize('ar1_method',['ar1asym', 'ar1sim'])
    def test_signif_test_t1(self,ar1_method):
        ''' Test scalogram.signif_test() with default parameters
        '''
        ts = pyleo.utils.gen_ts(model='colored_noise',nt=500)
        scal = ts.wavelet(method='cwt')
        scal_signif = scal.signif_test(method=ar1_method,number=1)
