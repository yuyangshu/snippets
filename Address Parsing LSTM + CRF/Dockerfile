FROM nvidia/cuda:11.1-base
# can use GPU but not on k8s

WORKDIR /home/aps-lstm-crf-service
COPY . .
RUN mv .flair /root

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y cmake pkg-config git software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt install -y python3.7-dev python3-pip

RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m spacy download en_core_web_sm
RUN python3.7 -m spacy download ja_core_news_sm

# S3 secrets from k8s secrets
ENV S3_URL=https://s3.wtg.ws:443
# ENV S3_ACCESS_KEY_ID=
# ENV S3_SECRET_ACCESS_KEY=

# start service
ENV FLASK_APP=service.py
CMD ["flask", "run", "--host=0.0.0.0"]
