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

def data(df, rules):
    try:
        """
        Validates the DataFrame based on specified rules.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            rules (dict): A dictionary containing validation rules.

        Returns:
            bool: True if the data is valid, False otherwise.
            list: A list of error messages if the data is invalid.
        """
        errors_invalid_type = []  # List to store type mismatch errors
        errors_out_of_range = []  # List to store out-of-range errors

        # Loop through each column and apply validation rules
        for col, rule in rules.items():
            # Type validation
            if 'type' in rule:
                if not all(isinstance(x, rule['type']) for x in df[col] if x is not None and not isinstance(x, bool)):
                    errors_invalid_type.append(f"Type mismatch in column {col}")

            # Range validation
            if 'min_value' in rule or 'max_value' in rule:
                for val in df[col]:
                    if not isinstance(val, (int, float)):
                        errors_out_of_range.append(f"Invalid type for range comparison in column {col}")
                        continue

                    if 'min_value' in rule and val < rule['min_value']:
                        errors_out_of_range.append(f"Value {val} in column {col} is below the minimum {rule['min_value']}")

                    if 'max_value' in rule and val > rule['max_value']:
                        errors_out_of_range.append(f"Value {val} in column {col} is above the maximum {rule['max_value']}")

        # Compile all errors
        all_errors = errors_invalid_type + errors_out_of_range
        errors_invalid_type = errors_invalid_type if errors_invalid_type else []

        # Check if any errors were found
        if len(all_errors) > 0:
            return [],[]  # Return a boolean and a list of all errors
        else:
            return [],[]  # Make sure to return an empty list, not a boolean
    except Exception as e:
        print("An error occurred:", str(e))
        raise
