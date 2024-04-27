FROM python:3.12

SHELL ["/bin/bash", "-c"]

COPY ./src /src
COPY ./requirements.txt /

RUN pip install -r /requirements.txt

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["/src/main.py"]