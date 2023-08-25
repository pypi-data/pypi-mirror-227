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

def merge(left, right, **kwargs):
try:
    """Merge DataFrame or named Series objects with a database-style join."""
    return pd.merge(left, right, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def groupby(data, by, **kwargs):
try:
    """Group DataFrame using a mapper or by a Series of columns."""
    return data.groupby(by, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def pivot_table(data, values, index, columns, **kwargs):
try:
    """Create a spreadsheet-style pivot table as a DataFrame."""
    return pd.pivot_table(data, values=values, index=index, columns=columns, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def cut(x, bins, **kwargs):
try:
    """Bin values into discrete intervals."""
    return pd.cut(x, bins, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def get_dummies(data, **kwargs):
try:
    """Convert categorical variable into dummy/indicator variables."""
    return pd.get_dummies(data, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def transpose(data, **kwargs):
try:
    """Transpose index and columns."""
    return data.transpose(**kwargs)

# scikit-learn functions
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler

except Exception as e:
    print("An error occurred:", str(e))
    raise
def PCA_transform(n_components, **kwargs):
try:
    """Principal component analysis (PCA)"""
    return PCA(n_components=n_components, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def OneHotEncoder_transform(**kwargs):
try:
    """Encode categorical features as a one-hot numeric array."""
    return OneHotEncoder(**kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def SelectKBest_transform(k, **kwargs):
try:
    """Select features according to the k highest scores."""
    return SelectKBest(k=k, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def StandardScaler_transform(**kwargs):
try:
    """Standardize features by removing the mean and scaling to unit variance."""
    return StandardScaler(**kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise