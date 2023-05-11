FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    mkdir -p /app/img

# ENTRYPOINT [ "python", "stream_capture.py" ]

CMD [ "python", "stream_capture.py" ]
