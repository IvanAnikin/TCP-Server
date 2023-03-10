FROM python:3.9-slim

WORKDIR /app

COPY server.py /app

RUN pip install numpy

EXPOSE 8080

CMD ["python", "server.py"]