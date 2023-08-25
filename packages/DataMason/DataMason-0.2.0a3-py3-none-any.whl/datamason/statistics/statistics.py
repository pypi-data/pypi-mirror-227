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

def linregress_statistics(x, y):
    """Calculate a linear least-squares regression."""
    return linregress(x, y)

def ttest_ind_statistics(a, b, *args, **kwargs):
    """Calculate the T-test for the means of two independent samples."""
    return ttest_ind(a, b, *args, **kwargs)

def chisquare_statistics(f_obs, f_exp=None, *args, **kwargs):
    """Calculate a one-way chi-square test."""
    return chisquare(f_obs, f_exp, *args, **kwargs)

def ols_statistics(endog, exog, *args, **kwargs):
    """Ordinary Least Squares (OLS) model."""
    return sm.OLS(endog, exog, *args, **kwargs).fit()

def logit_statistics(endog, exog, *args, **kwargs):
    """Logistic Regression model using Logit."""
    return sm.Logit(endog, exog, *args, **kwargs).fit()

def glm_statistics(endog, exog, family=None, *args, **kwargs):
    """Generalized Linear Model (GLM)."""
    return sm.GLM(endog, exog, family, *args, **kwargs).fit()

def arima_statistics(endog, order, *args, **kwargs):
    """AutoRegressive Integrated Moving Average (ARIMA) model."""
    return sm.tsa.ARIMA(endog, order, *args, **kwargs).fit()
