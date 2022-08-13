FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]