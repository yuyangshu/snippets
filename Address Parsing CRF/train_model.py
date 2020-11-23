import os
import time
import boto3
import pickle
import pycrfsuite

from itertools import chain
from sklearn import metrics
from sklearn.preprocessing import LabelBinarizer



if __name__ == "__main__":
    print(f"training started at {time.asctime()}")
    with open("X_train_dump", "rb") as f:
        X_train = pickle.load(f)
    with open("y_train_dump", "rb") as f:
        y_train = pickle.load(f)

    print(f"appending training data to trainer: {time.asctime()}")
    trainer = pycrfsuite.Trainer(verbose=True)
    for x, y in zip(X_train, y_train):
        trainer.append(x, y)

    trainer.set_params({
        "c1": 0.1,
        "c2": 1e-3,
        "max_iterations": 100,
        "feature.possible_transitions": True
    })
    
    print(f"model training started at {time.asctime()}")
    trainer.train("model_dump")

    print(f"evaluation started at {time.asctime()}")
    # evaluate model
    tagger = pycrfsuite.Tagger()
    tagger.open("model_dump")

    lb = LabelBinarizer()
    with open("X_test_dump", "rb") as f:
        X_test = pickle.load(f)
    with open("y_test_dump", "rb") as f:
        y_test = lb.fit_transform(list(chain.from_iterable(pickle.load(f))))

    y_pred = lb.transform(list(chain.from_iterable([tagger.tag(x) for x in X_test])))

    tag_set = sorted(lb.classes_)
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}

    print(metrics.classification_report(
        y_test,
        y_pred,
        labels = [class_indices[cls] for cls in tag_set],
        target_names = tag_set,
        digits=3
    ))
    print(f"evaluation finished at {time.asctime()}")

    client = boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get("S3_URL"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
    )

    client.upload_file("model_dump", "aps-crf-model", "model_dump")
