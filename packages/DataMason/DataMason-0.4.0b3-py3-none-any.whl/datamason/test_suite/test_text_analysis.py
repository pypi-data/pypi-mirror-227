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

import nltk
from datamason.text_analysis import text_analysis
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer

def test_sent_tokenize_text():
    try:
        text = "Hello world. This is a test."
        result = text_analysis.sent_tokenize_text(text)
        expected_result = nltk.sent_tokenize(text)
        assert result == expected_result, f"Expected {{expected_result}}, got {{result}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_word_tokenize_text():
    try:
        text = "Hello world."
        result = text_analysis.word_tokenize_text(text)
        expected_result = nltk.word_tokenize(text)
        assert result == expected_result, f"Expected {{expected_result}}, got {{result}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_pos_tag_text():
    try:
        tokens = ["Hello", "world"]
        result = text_analysis.pos_tag_text(tokens)
        expected_result = nltk.pos_tag(tokens)
        assert result == expected_result, f"Expected {{expected_result}}, got {{result}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_freq_dist_text():
    try:
        tokens = ["a", "b", "a", "c", "a", "b"]
        result = text_analysis.freq_dist_text(tokens)
        expected_result = FreqDist(tokens)
        assert result == expected_result, f"Expected {{expected_result}}, got {{result}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise
def test_wordnet_lemmatizer():
    try:
        result = text_analysis.wordnet_lemmatizer()
        assert isinstance(result, WordNetLemmatizer), f"Expected WordNetLemmatizer instance, got {{result}}"

    except Exception as e:
        print("An error occurred:", str(e))
        raise