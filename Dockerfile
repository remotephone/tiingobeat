FROM python:3.8

WORKDIR /code

COPY tiingobeat/requirements.txt .

RUN pip install -r requirements.txt

COPY tiingobeat/src/ .

# command to run on container start
CMD [ "python", "./tiingobeat.py" ]