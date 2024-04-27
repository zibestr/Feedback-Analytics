FROM python:3.10

SHELL ["/bin/bash", "-c"]

COPY . /src
COPY ./requirements.txt /

RUN pip install -r /requirements.txt
ENTRYPOINT ["python3"]
CMD ["/src/main.py"]