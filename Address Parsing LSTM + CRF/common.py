import re

import spacy

from flair.data import Sentence
from flair.tokenization import SpacyTokenizer
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings



def remove_control_chars(s):
    # remove control characters
    s = re.sub("[\x00-\x1f\x7f\u0080-\u009f]+", '', s)
    # replace `NO-BREAK SPACE`
    return re.sub("\u00a0+", ' ', s)



components = {
    "au": ["house_name", "unit", "house_number", "street", "suburb", "city", "state", "postcode", "country"],
    "jp": ["state", "city", "street", "house_number", "unit", "postcode", "country"]
}

tokenizers = {
    "au": SpacyTokenizer(spacy.load("en_core_web_sm")),
    "jp": SpacyTokenizer(spacy.load("ja_core_news_sm"))
}

embeddings = StackedEmbeddings([
    FlairEmbeddings('multi-forward'),
    FlairEmbeddings('multi-backward')
])

# stacked embedding is recommended but traditional embeddings are trained on single languages
# embeddings = {
#     "au": StackedEmbeddings([
#         WordEmbeddings('en'),
#         FlairEmbeddings('mix-forward'),
#         FlairEmbeddings('mix-backward'),
#     ]),
#     "jp": StackedEmbeddings([
#         WordEmbeddings('ja'),
#         FlairEmbeddings('ja-forward'),
#         FlairEmbeddings('ja-backward'),
#     ])
# }
