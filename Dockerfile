FROM python:3.8
COPY . /usr/app
EXPOSE 3000
WORKDIR /usr/app
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
CMD python flask_api.py