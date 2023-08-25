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

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.naive_bayes import GaussianNB

def train_test_split_model(*arrays, **kwargs):
    """Split arrays or matrices into random train and test subsets."""
    return train_test_split(*arrays, **kwargs)

def SVC_model(**kwargs):
    """C-Support Vector Classification."""
    return SVC(**kwargs)

def RandomForestClassifier_model(**kwargs):
    """A random forest classifier."""
    return RandomForestClassifier(**kwargs)

def KNeighborsClassifier_model(**kwargs):
    """Classifier implementing the k-nearest neighbors vote."""
    return KNeighborsClassifier(**kwargs)

def cross_val_score_model(estimator, X, y, **kwargs):
    """Evaluate a score by cross-validation."""
    return cross_val_score(estimator, X, y, **kwargs)

def GridSearchCV_model(estimator, param_grid, **kwargs):
    """Exhaustive search over a specified parameter grid."""
    return GridSearchCV(estimator, param_grid, **kwargs)

def GaussianNB_model(**kwargs):
    """Gaussian Naive Bayes (GaussianNB)"""
    return GaussianNB(**kwargs)

def SVR_model(**kwargs):
    """Epsilon-Support Vector Regression."""
    return SVR(**kwargs)

# tensorflow/keras functions
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, LSTM

def Sequential_model(layers):
    """Linear stack of layers."""
    model = Sequential()
    for layer in layers:
        model.add(layer)
    return model

def Dense_layer(units, **kwargs):
    """Regular densely-connected Neural Network (NN) layer."""
    return Dense(units, **kwargs)

def Conv2D_layer(filters, kernel_size, **kwargs):
    """2D convolution layer (e.g. spatial convolution over images)."""
    return Conv2D(filters, kernel_size, **kwargs)

def LSTM_layer(units, **kwargs):
    """Long Short-Term Memory layer - Hochreiter 1997."""
    return LSTM(units, **kwargs)

def compile_model(model, **kwargs):
    """Configures the model for training."""
    model.compile(**kwargs)
    return model

def fit_model(model, x, y, **kwargs):
    """Trains the model for a fixed number of epochs (iterations on a dataset)."""
    return model.fit(x, y, **kwargs)

def evaluate_model(model, x, y, **kwargs):
    """Returns the loss value & metrics values for the model in test mode."""
    return model.evaluate(x, y, **kwargs)
