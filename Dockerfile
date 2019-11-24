FROM python:3.7.3-stretch
ADD requirements.txt /app/
RUN pip install --upgrade pip && \
    apt-get update -y && \
    pip install -U -r /app/requirements.txt && \
    apt-get install -y ffmpeg
