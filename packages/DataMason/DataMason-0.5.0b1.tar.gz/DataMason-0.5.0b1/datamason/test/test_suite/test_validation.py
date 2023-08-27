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

import unittest
import pandas as pd
from datamason.validation import validate

class TestFunctions(unittest.TestCase):

    def test_data(self):
        try:
            # Test with invalid type data
            df_invalid_type = pd.DataFrame({'A': [1, '2', 3]})
            rules_valid = {'A': {'type': int, 'min_value': 1, 'max_value': 3}}
            
            errors_invalid_type, errors_out_of_range = validate.data(df_invalid_type, rules_valid)
            assert isinstance(errors_invalid_type, (list, tuple, str)), "errors_invalid_type should be an iterable"


            self.assertTrue("Type mismatch in column 'A' at index 1" in errors_invalid_type)


            # Test with out-of-range data
            df_out_of_range = pd.DataFrame({'A': [0, 1, 4]})
            errors_invalid_type, errors_out_of_range = validate.data(df_out_of_range, rules_valid)
            self.assertTrue("Value out of range in column 'A' at index 0" in errors_out_of_range)
            self.assertTrue("Value out of range in column 'A' at index 2" in errors_out_of_range)

            # Test with missing column
            df_missing_col = pd.DataFrame({'B': [1, 2, 3]})
            errors_invalid_type, errors_out_of_range = validate.data(df_missing_col, rules_valid)
            self.assertTrue("Column 'A' not found in DataFrame" in errors_invalid_type)

            # Test with valid data
            df_valid = pd.DataFrame({'A': [1, 2, 3]})
            errors_invalid_type, errors_out_of_range = validate.data(df_valid, rules_valid)
            self.assertEqual(errors_invalid_type, [])
            self.assertEqual(errors_out_of_range, [])

        except Exception as e:
            self.fail(f"An unexpected error occurred: {str(e)}")