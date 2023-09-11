FROM python:3.9.6-bullseye

WORKDIR /usr/src/app

RUN mkdir service
COPY ./src/backend ./backend
COPY ./src/run_backend.py .
COPY ./reqs.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r reqs.txt


CMD ["python", "run_backend.py"]

EXPOSE 80