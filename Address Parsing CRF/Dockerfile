FROM python:3.7

WORKDIR /home/aps-crf-service
COPY . .
RUN pip3 install -r requirements.txt

# S3 secrets from k8s secrets
ENV S3_URL=https://s3.wtg.ws:443
# ENV S3_ACCESS_KEY_ID=
# ENV S3_SECRET_ACCESS_KEY=

# start service
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=service.py
CMD ["flask", "run", "--host=0.0.0.0"]
