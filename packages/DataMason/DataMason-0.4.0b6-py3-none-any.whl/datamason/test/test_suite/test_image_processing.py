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
from PIL import Image
from datamason.image_processing import image_processing

def test_resize_image():
    try:
        image = Image.new('RGB', (100, 100))
        result = image_processing.resize_image(image, (50, 50))
        assert result.size == (50, 50), f"Expected (50, 50), got {{result.size}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_rotate_image():
    try:
        image = Image.new('RGB', (100, 100))
        result = image_processing.rotate_image(image, 45)
        assert result is not None, "Result should not be None"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_equalize_histogram():
    try:
        image = Image.new('RGB', (100, 100))
        result = image_processing.equalize_histogram(image)
        assert result is not None, "Result should not be None"

    except Exception as e:
        print("An error occurred:", str(e))
        raise