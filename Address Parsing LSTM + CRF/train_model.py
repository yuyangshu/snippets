import os
import time
import boto3

from itertools import chain
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

from common import *



if __name__ == "__main__":
    print(f"loading corpus: {time.asctime()}")
    working_directory = "/home/yuyang/data_science/experimental_address_parsing/output"

    # corpus = ColumnCorpus(
    #     data_folder=working_directory,
    #     column_format={0: "text", 1: "address_part"},
    #     train_file="train.txt",
    #     dev_file="dev.txt",
    #     test_file="test.txt",
    #     in_memory=False     # dataset too large to fit into 128G RAM
    # )

    corpus = ColumnCorpus(
        data_folder=working_directory,
        column_format={0: "text", 1: "address_part"},
        train_file="train-reduced.txt",
        dev_file="dev-reduced.txt",
        test_file="test-reduced.txt"
    )

    print(f"creating model and trainer: {time.asctime()}")
    tag_type = "address_part"
    tagger = SequenceTagger(
        hidden_size=256,
        embeddings=embeddings,
        tag_dictionary=corpus.make_tag_dictionary(tag_type=tag_type),
        tag_type=tag_type,
        use_crf=True
    )
    trainer = ModelTrainer(tagger, corpus)

    print(f"model training started at {time.asctime()}")
    trainer.train(
        working_directory,
        learning_rate=0.1,
        mini_batch_size=32,
        max_epochs=150
    )

    client = boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get("S3_URL"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
    )

    client.upload_file("final-model.pt", "aps-lstm-crf-model", "final-model.pt")
