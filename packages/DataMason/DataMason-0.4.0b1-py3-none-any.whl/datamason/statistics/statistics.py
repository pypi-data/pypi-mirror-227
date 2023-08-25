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
try:
    """Calculate a linear least-squares regression."""
    return linregress(x, y)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def ttest_ind_statistics(a, b, *args, **kwargs):
try:
    """Calculate the T-test for the means of two independent samples."""
    return ttest_ind(a, b, *args, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def chisquare_statistics(f_obs, f_exp=None, *args, **kwargs):
try:
    """Calculate a one-way chi-square test."""
    return chisquare(f_obs, f_exp, *args, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def ols_statistics(endog, exog, *args, **kwargs):
try:
    """Ordinary Least Squares (OLS) model."""
    return sm.OLS(endog, exog, *args, **kwargs).fit()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def logit_statistics(endog, exog, *args, **kwargs):
try:
    """Logistic Regression model using Logit."""
    return sm.Logit(endog, exog, *args, **kwargs).fit()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def glm_statistics(endog, exog, family=None, *args, **kwargs):
try:
    """Generalized Linear Model (GLM)."""
    return sm.GLM(endog, exog, family, *args, **kwargs).fit()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def arima_statistics(endog, order, *args, **kwargs):
try:
    """AutoRegressive Integrated Moving Average (ARIMA) model."""
    return sm.tsa.ARIMA(endog, order, *args, **kwargs).fit()

except Exception as e:
    print("An error occurred:", str(e))
    raise