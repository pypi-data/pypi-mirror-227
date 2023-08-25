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

import pandas as pd
from datamason.analyze import analysis

def test_summarize():
    try:
        data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        summary = analysis.summarize(data)
        assert isinstance(summary, dict)
        assert summary['mean']['A'] == 1.5
        assert summary['mean']['B'] == 3.5

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_find_correlations():
    try:
        data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        correlations = analysis.find_correlations(data)
        assert isinstance(correlations, pd.DataFrame)
        assert correlations.loc['A', 'B'] == 1.0

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_count_values():
    try:
        data = pd.Series([1, 2, 2, 3])
        counts = analysis.count_values(data)
        assert counts[1] == 1
        assert counts[2] == 2
        assert counts[3] == 1
        
    except Exception as e:
        print("An error occurred:", str(e))
        raise