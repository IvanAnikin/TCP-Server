FROM python:3.9-slim

WORKDIR /app

COPY ./* /app

RUN pip install numpy

EXPOSE 8080

CMD ["python", "server full clean.py"]