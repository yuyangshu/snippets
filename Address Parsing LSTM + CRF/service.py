import os
import re
import boto3

from collections import OrderedDict
from flair.models import SequenceTagger
from flask import Flask, jsonify, request

from common import *



s3_resource = boto3.resource(
    service_name="s3",
    endpoint_url=os.environ.get("S3_URL"),
    aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)
s3_resource.Bucket("aps-lstm-crf-model").download_file("final-model.pt", "final-model.pt")

tagger = SequenceTagger.load("final-model.pt")

app = Flask(__name__)



@app.route('/parser', methods=['POST'])
def parse():
    address = re.sub(", *", ' ', request.json['query'])
    country = "jp" if re.match("[\u3000-\u9fff\uf900-\ufaff\uff66-\uff9f]+", address) else "au"

    sentence = Sentence(remove_control_chars(address), use_tokenizer=tokenizers[country])
    tagger.predict(sentence)

    dictionary, previous_tag = OrderedDict(), ""
    for token in sentence:
        tag = token.get_tag("address_part").value

        if tag == previous_tag:
            dictionary[tag] += (' ' if country == "au" else '') + token.text
        else:
            dictionary[tag] = token.text
            previous_tag = tag

    response = []
    while len(dictionary) > 0:
        key, value = dictionary.popitem(last=False)
        response.append({
        "label": key,
        "value": re.sub(" *- *", '-', value)
    })

    return jsonify(response)

@app.route('/version')
def version():
    return "0.1"
