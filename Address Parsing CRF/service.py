import os
import re
import boto3
import pycrfsuite

from collections import OrderedDict
from flask import Flask, jsonify, request

from common import *



s3_resource = boto3.resource(
    service_name="s3",
    endpoint_url=os.environ.get("S3_URL"),
    aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)
s3_resource.Bucket("aps-crf-model").download_file("model_dump", "model_dump")

tagger = pycrfsuite.Tagger()
tagger.open("model_dump")

app = Flask(__name__)



@app.route('/parser', methods=['POST'])
def parse():
    address = request.json['query']
    country = "jp" if re.match("[\u3000-\u9fff\uf900-\ufaff\uff66-\uff9f]+", address) else "au"

    # remove control characters and no-break spaces
    processed_address = remove_control_chars(address)

    tokens = [re.sub("[,.]$", '', item) for item in processed_address.split()]
    features = [
        feature_from_token(
            tokens[i - 1] if i > 0 else None,                   # previous token
            tokens[i],                                          # current token
            tokens[i + 1] if i < len(tokens) - 1 else None      # next token
        ) for i in range(len(tokens)
    )]

    tags = tagger.tag(features)

    dictionary, previous_tag = OrderedDict(), ""
    for token, tag in zip([item["token.lower()"] for item in features], tags):
        if tag == previous_tag:
            dictionary[tag] += ('' if country == "jp" else ' ') + token
        else:
            dictionary[tag] = token
            previous_tag = tag

    response = []
    while len(dictionary) > 0:
        key, value = dictionary.popitem(last=False)
        response.append({
        "label": key,
        "value": value
    })

    return jsonify(response)

@app.route('/version')
def version():
    return "0.1"
