FROM python:3.13.1

WORKDIR /app

COPY ./base /app
COPY ./Endpoint /app
COPY ./Models /app
COPY ./main.py /app
COPY ./requirments.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirments.txt

CMD ["faststream", "run", "main:app"]