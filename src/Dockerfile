FROM python:3.12

SHELL ["/bin/bash", "-c"]

COPY . /src
COPY ./requirements.txt /

RUN pip install -r /requirements.txt && \
    python3 /src/fillBase.py

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["/src/bot.py"]