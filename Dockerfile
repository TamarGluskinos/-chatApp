# set base image (host OS)
FROM python:3.8-slim
# set the working directory in the container
WORKDIR /code
# copy the dependencies file to the working directory
COPY requirements.txt .

ENV CHAT_ROOM_PATH='rooms/'

ENV FLASK_ENV development

# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
COPY src/ .

RUN apt-get -y update; apt-get -y install curl

HEALTHCHECK --interval=10s --timeout=3s CMD curl --fail http://localhost:5000/health || exit 1 

# command to run on container start
CMD [ "python", "./chatApp.py" ]