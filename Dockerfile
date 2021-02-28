FROM python:3.7.7-slim-buster

MAINTAINER <sventestcodes@gmail.com>

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 8050

ENTRYPOINT [ "python3" ]

CMD [ "dashboard.py" ]