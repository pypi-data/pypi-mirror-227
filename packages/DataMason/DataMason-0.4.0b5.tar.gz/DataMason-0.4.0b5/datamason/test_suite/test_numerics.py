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

import numpy as np
from datamason.numerics import numerical

def test_array():
    try:
        arr = numerical.array([1, 2, 3])
        assert np.array_equal(arr, np.array([1, 2, 3]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_linspace():
    try:
        arr = numerical.linspace(0, 1, 5)
        assert np.array_equal(arr, np.array([0.  , 0.25, 0.5 , 0.75, 1.  ]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_arange():
    try:
        arr = numerical.arange(0, 5, 2)
        assert np.array_equal(arr, np.array([0, 2, 4]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_reshape():
    try:
        arr = numerical.reshape(np.array([1, 2, 3, 4]), (2, 2))
        assert np.array_equal(arr, np.array([[1, 2], [3, 4]]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_dot():
    try:
        result = numerical.dot(np.array([1, 2]), np.array([3, 4]))
        assert result == 11

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_concatenate():
    try:
        result = numerical.concatenate((np.array([1, 2]), np.array([3, 4])))
        assert np.array_equal(result, np.array([1, 2, 3, 4]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_mean():
    try:
        result = numerical.mean(np.array([1, 2, 3, 4]))
        assert result == 2.5

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_std():
    try:
        result = numerical.std(np.array([1, 2, 3, 4]))
        assert result == np.std(np.array([1, 2, 3, 4]))

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_min():
    try:
        result = numerical.min(np.array([1, 2, 3, 4]))
        assert result == 1

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_max():
    try:
        result = numerical.max(np.array([1, 2, 3, 4]))
        assert result == 4

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_np_sin():
    try:
        result = numerical.np.sin(0)
        assert result == 0

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_np_cos():
    try:
        result = numerical.np.cos(0)
        assert result == 1

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_np_tan():
    try:
        result = numerical.np.tan(0)
        assert result == 0
        
    except Exception as e:
        print("An error occurred:", str(e))
        raise