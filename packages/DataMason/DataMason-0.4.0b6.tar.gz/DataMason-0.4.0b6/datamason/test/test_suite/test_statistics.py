#     Copyright (c) 2023, Kevan White (Thyripian)
#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:
#       Compliance with MIT License clauses.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from scipy.stats import ttest_ind, chisquare
from statsmodels.formula.api import ols, logit, glm

import numpy as np
from datamason.statistics import statistics
from scipy.stats import linregress

def test_linregress_statistics():
    try:
        # Testing with valid input
        x = np.array([1, 2, 3, 4])
        y = np.array([2, 4, 6, 8])
        result = statistics.linregress_statistics(x, y)
        expected_result = linregress(x, y)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_ttest_ind_statistics():
    try:
        # Testing with example input
        result = statistics.ttest_ind_statistics(*example_input)
        expected_result = ttest_ind(*example_input)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_chisquare_statistics():
    try:
        # Testing with example input
        result = statistics.chisquare_statistics(*example_input)
        expected_result = chisquare(*example_input)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_ols_statistics():
    try:
        # Testing with example input
        result = statistics.ols_statistics(*example_input)
        expected_result = ols(*example_input)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_logit_statistics():
    try:
        # Testing with example input
        result = statistics.logit_statistics(*example_input)
        expected_result = logit(*example_input)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_glm_statistics():
    try:
        # Testing with example input
        result = statistics.glm_statistics(*example_input)
        expected_result = glm(*example_input)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise

def test_ttest_ind_statistics():
    try:
        a = [1, 2, 3]
        b = [4, 5, 6]
        result = statistics.ttest_ind_statistics(a, b)
        assert result is not None, "Result should not be None"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_arima_statistics():
    try:
        data = [1, 2, 3, 4, 5, 6]
        result = statistics.arima_statistics(data, order=(1, 0, 0))
        assert result is not None, "Result should not be None"

    except Exception as e:
        print("An error occurred:", str(e))
        raise