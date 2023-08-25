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

import numpy as np
import pandas as pd
from datamason.visualization import visualize
import seaborn as sns

def test_plot():
    try:
        x = [1, 2, 3]
        y = [4, 5, 6]
        visualize.plot(x, y, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_scatter():
    try:
        x = np.random.rand(10)
        y = np.random.rand(10)
        visualize.scatter(x, y, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_bar():
    try:
        x = ['A', 'B', 'C']
        y = [4, 5, 6]
        visualize.bar(x, y, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_hist():
    try:
        data = np.random.randn(100)
        visualize.hist(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_boxplot():
    try:
        data = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)})
        visualize.boxplot(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_pie():
    try:
        x = [45, 30, 25]
        visualize.pie(x, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_distplot():
    try:
        data = np.random.randn(100)
        visualize.distplot(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_heatmap():
    try:
        data = sns.load_dataset('flights').pivot('month', 'year', 'passengers')
        visualize.heatmap(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_pairplot():
    try:
        data = sns.load_dataset('iris')
        visualize.pairplot(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_violinplot():
    try:
        data = sns.load_dataset('tips')
        visualize.violinplot(data, x='day', y='total_bill', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_joinplot():
    try:
        data = sns.load_dataset('tips')
        visualize.joinplot(data, x='total_bill', y='tip', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_countplot():
    try:
        data = sns.load_dataset('tips')
        visualize.countplot(data, x='day', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_lmplot():
    try:
        data = sns.load_dataset('tips')
        visualize.lmplot(data, x='total_bill', y='tip', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_regplot():
    try:
        data = sns.load_dataset('tips')
        visualize.regplot(data, x='total_bill', y='tip', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_kdeplot():
    try:
        data = sns.load_dataset('tips')
        visualize.kdeplot(data, x='total_bill', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_facetgrid():
    try:
        data = sns.load_dataset('tips')
        visualize.facetgrid(data, col='time', row='sex', render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_clustermap():
    try:
        data = sns.load_dataset('flights').pivot('month', 'year', 'passengers')
        visualize.clustermap(data, render=False)

    except Exception as e:
        print("An error occurred:", str(e))
        raise