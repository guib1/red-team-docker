FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask docker flask-cors

COPY app.py .

EXPOSE 8082

CMD ["python", "app.py"]
