FROM python:3.7.3-stretch
ADD requirements.txt /app/
RUN apt-get update
RUN apt-get install ffmpeg
RUN pip install -U -r /app/requirements.txt
