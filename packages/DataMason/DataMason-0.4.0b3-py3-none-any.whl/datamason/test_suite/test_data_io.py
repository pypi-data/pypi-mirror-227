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
from datamason.data_io import io

def test_read_csv():
    try:
        data = io.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (150, 5)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_to_csv():
    try:
        data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        file_path = 'test_to_csv.csv'
        io.to_csv(data, file_path)
        read_data = pd.read_csv(file_path)
        assert read_data.equals(data)

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_read_excel():
    try:
        # Assuming an Excel file is available for testing
        file_path = 'test_read_excel.xlsx'
        data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        data.to_excel(file_path, index=False)
        read_data = io.read_excel(file_path)
        assert read_data.equals(data)
        
    except Exception as e:
        print("An error occurred:", str(e))
        raise