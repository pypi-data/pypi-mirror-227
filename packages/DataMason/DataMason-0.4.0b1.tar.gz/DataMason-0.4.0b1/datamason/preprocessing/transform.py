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

def merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None):
try:
    return pd.merge(left, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def groupby(df, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, observed=False):
try:
    return df.groupby(by, axis, level, as_index, sort, group_keys, squeeze, observed)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def pivot_table(df, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False):
try:
    return pd.pivot_table(df, values, index, columns, aggfunc, fill_value, margins, dropna, margins_name, observed)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def cut(x, bins, right=True, labels=None, retbins=False, precision=3, include_lowest=False, duplicates='raise'):
try:
    return pd.cut(x, bins, right, labels, retbins, precision, include_lowest, duplicates)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def get_dummies(df, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None):
try:
    return pd.get_dummies(df, prefix, prefix_sep, dummy_na, columns, sparse, drop_first, dtype)

except Exception as e:
    print("An error occurred:", str(e))
    raise