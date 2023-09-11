FROM python:3.9.6-bullseye

WORKDIR /usr/src/app

RUN mkdir service
COPY ./src .
COPY ./src/reqs.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r reqs.txt


CMD ["py", "run_backend.py"]

EXPOSE 80