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
from datamason.validation import validate

def test_data():
    try:
        # Test with valid data
        df_valid = pd.DataFrame({'A': [1, 2, 3], 'B': [4.0, 5.0, 6.0]})
        rules_valid = {'A': {'type': int, 'min_value': 1, 'max_value': 3}, 'B': {'type': float, 'min_value': 4.0, 'max_value': 6.0}}
        result_valid, errors_valid = validate.data(df_valid, rules_valid)
        assert result_valid == True, f"Expected True, got {{result_valid}}. Errors: {{errors_valid}}"

        # Test with invalid type
        df_invalid_type = pd.DataFrame({'A': [1, '2', 3], 'B': [4.0, 5.0, 6.0]})
        result_invalid_type, errors_invalid_type = validate.data(df_invalid_type, rules_valid)
        assert result_invalid_type == False, f"Expected False, got {{result_invalid_type}}"
        assert "Type mismatch in column 'A'" in errors_invalid_type

        # Test with invalid min_value
        df_invalid_min = pd.DataFrame({'A': [0, 2, 3], 'B': [4.0, 5.0, 6.0]})
        result_invalid_min, errors_invalid_min = validate.data(df_invalid_min, rules_valid)
        assert result_invalid_min == False, f"Expected False, got {{result_invalid_min}}"
        assert "Values below 1 found in column 'A'" in errors_invalid_min

        # Test with invalid max_value
        df_invalid_max = pd.DataFrame({'A': [1, 2, 4], 'B': [4.0, 5.0, 7.0]})
        result_invalid_max, errors_invalid_max = validate.data(df_invalid_max, rules_valid)
        assert result_invalid_max == False, f"Expected False, got {{result_invalid_max}}"
        assert "Values above 3 found in column 'A'" in errors_invalid_max

    except Exception as e:
        print("An error occurred:", str(e))
        raise