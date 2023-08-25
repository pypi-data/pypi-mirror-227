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

import matplotlib.pyplot as plt

def plot(x, y, **kwargs):
try:
    """Plot y versus x as lines and/or markers."""
    plt.plot(x, y, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def scatter(x, y, **kwargs):
try:
    """A scatter plot of y vs x with varying marker size and/or color."""
    plt.scatter(x, y, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def bar(x, height, **kwargs):
try:
    """Make a bar plot."""
    plt.bar(x, height, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def hist(x, **kwargs):
try:
    """Plot a histogram."""
    plt.hist(x, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def boxplot(x, **kwargs):
try:
    """Make a box and whisker plot."""
    plt.boxplot(x, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def pie(x, **kwargs):
try:
    """Plot a pie chart."""
    plt.pie(x, **kwargs)
    plt.show()

# seaborn functions
import seaborn as sns

except Exception as e:
    print("An error occurred:", str(e))
    raise
def distplot(a, **kwargs):
try:
    """Flexibly plot a univariate distribution of observations."""
    sns.distplot(a, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def heatmap(data, **kwargs):
try:
    """Plot rectangular data as a color-encoded matrix."""
    sns.heatmap(data, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def pairplot(data, **kwargs):
try:
    """Plot pairwise relationships in a dataset."""
    sns.pairplot(data, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def violinplot(x, y, **kwargs):
try:
    """Draw a combination of boxplot and kernel density estimate."""
    sns.violinplot(x, y, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def joinplot(x, y, **kwargs):
try:
    """Draw a plot of two variables with bivariate and univariate graphs."""
    sns.jointplot(x, y, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def countplot(x, **kwargs):
try:
    """Show the counts of observations in each categorical bin using bars."""
    sns.countplot(x, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def lmplot(x, y, data, **kwargs):
try:
    """Plot data and regression model fits across a FacetGrid."""
    sns.lmplot(x, y, data, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def regplot(x, y, **kwargs):
try:
    """Plot data and a linear regression model fit."""
    sns.regplot(x, y, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def kdeplot(data, **kwargs):
try:
    """Fit and plot a univariate or bivariate kernel density estimate."""
    sns.kdeplot(data, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise
def facetgrid(data, **kwargs):
try:
    """Multi-plot grid for plotting conditional relationships."""
    return sns.FacetGrid(data, **kwargs)

except Exception as e:
    print("An error occurred:", str(e))
    raise
def clustermap(data, **kwargs):
try:
    """Display a matrix dataset as a hierarchically-clustered heatmap."""
    sns.clustermap(data, **kwargs)
    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
    raise