import os
import time
import pickle

import boto3
import pandas

from sklearn.model_selection import train_test_split

from common import *



source_bucket = "datascience-avs-staged"
prefix = "training_csv/"

def get_training_data():
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

    all_tokens, all_tags = [], []
    for filename in files_to_download:
        print("processing " + filename)

        object = client.get_object(
            Bucket=source_bucket,
            Key=filename
        )
        if object["ContentLength"] > 0:
            df = pandas.read_csv(
                object["Body"],
                dtype=str,
                keep_default_na=False,
                error_bad_lines=False
            )

        for _, row in df.iterrows():
            if row["country_code"] in components.keys():
                tokens, tags = [], []
                for key in components[row["country_code"]]:
                    if row.get(key):
                        filtered_field = remove_control_chars(row[key])
                        for token in filtered_field.split():
                            tokens.append(token)
                            tags.append(key)

                all_tokens.append([
                    token2feature(tokens[i - 1] if i > 0 else None, tokens[i], tokens[i + 1] if i < len(tokens) - 1 else None) for i in range(len(tokens))
                ])
                all_tags.append(tags)

    return all_tokens, all_tags



if __name__ == "__main__":
    print(f"feature generation started at {time.asctime()}")
    features, tags = get_training_data()

    print(f"train/test split started at {time.asctime()}")
    X_train, X_test, y_train, y_test = train_test_split(features, tags, test_size=0.2, random_state=623)

    with open("X_train_dump", "wb") as f:
        pickle.dump(X_train, f)
    with open("X_test_dump", "wb") as f:
        pickle.dump(X_test, f)
    with open("y_train_dump", "wb") as f:
        pickle.dump(y_train, f)
    with open("y_test_dump", "wb") as f:
        pickle.dump(y_test, f)

    print(f"data generation finished at {time.asctime()}")