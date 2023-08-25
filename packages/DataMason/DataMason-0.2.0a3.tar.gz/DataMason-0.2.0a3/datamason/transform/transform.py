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
    """Merge DataFrame or named Series objects with a database-style join."""
    return pd.merge(left, right, **kwargs)

def groupby(data, by, **kwargs):
    """Group DataFrame using a mapper or by a Series of columns."""
    return data.groupby(by, **kwargs)

def pivot_table(data, values, index, columns, **kwargs):
    """Create a spreadsheet-style pivot table as a DataFrame."""
    return pd.pivot_table(data, values=values, index=index, columns=columns, **kwargs)

def cut(x, bins, **kwargs):
    """Bin values into discrete intervals."""
    return pd.cut(x, bins, **kwargs)

def get_dummies(data, **kwargs):
    """Convert categorical variable into dummy/indicator variables."""
    return pd.get_dummies(data, **kwargs)

def transpose(data, **kwargs):
    """Transpose index and columns."""
    return data.transpose(**kwargs)

# scikit-learn functions
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler

def PCA_transform(n_components, **kwargs):
    """Principal component analysis (PCA)"""
    return PCA(n_components=n_components, **kwargs)

def OneHotEncoder_transform(**kwargs):
    """Encode categorical features as a one-hot numeric array."""
    return OneHotEncoder(**kwargs)

def SelectKBest_transform(k, **kwargs):
    """Select features according to the k highest scores."""
    return SelectKBest(k=k, **kwargs)

def StandardScaler_transform(**kwargs):
    """Standardize features by removing the mean and scaling to unit variance."""
    return StandardScaler(**kwargs)
