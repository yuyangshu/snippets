import os
import re
import time
import random

import boto3
import pandas

from common import *



def generate_training_data():
    source_bucket = "datascience-avs-staged"
    prefix = "training_csv/"
    random.seed(623)

    client = boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get('S3_URL'),
        aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY')
    )
    response = client.list_objects_v2(
        Bucket=source_bucket,
        Prefix=prefix
    )
    files_to_download = [item["Key"] for item in response['Contents'] if item["Size"] > 0]

    train_file = open("output/train-reduced.txt", 'w')
    dev_file = open("output/dev-reduced.txt", 'w')
    test_file = open("output/test-reduced.txt", 'w')

    for filename in files_to_download:
        print("processing " + filename)

        object = client.get_object(
            Bucket=source_bucket,
            Key=filename
        )
        if object["ContentLength"] == 0:
            continue

        df = pandas.read_csv(
            object["Body"],
            dtype=str,
            keep_default_na=False,
            error_bad_lines=False
        )

        for _, row in df.iterrows():
            if row["country_code"] not in components.keys():
                continue

            country, tokens, tags = row["country_code"], [], []

            # downsample
            if random.random() > 0.03:
                continue

            target = random.random()
            if target < 0.05:
                target_file = test_file
            elif target < 0.25:
                target_file = dev_file
            else:
                target_file = train_file

            for key in components[country]:
                if row.get(key):
                    filtered_field = remove_control_chars(row[key])
                    parsed_field = Sentence(filtered_field, use_tokenizer=tokenizers[country])

                    for token in parsed_field:
                        target_file.write(f"{token.text} {key}\n")

            target_file.write('\n')

    train_file.close()
    dev_file.close()
    test_file.close()



if __name__ == "__main__":
    print(f"data generation started at {time.asctime()}")
    generate_training_data()
    print(f"data generation finished at {time.asctime()}")
