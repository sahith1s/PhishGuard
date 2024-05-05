FROM python:3.8-slim-buster



WORKDIR /PhishGuard

COPY requirements.txt requirements.txt
COPY ./templates ./templates
COPY ./static ./static
COPY ./db ./db
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]
