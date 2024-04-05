FROM python:3.9-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

COPY . .

FROM python:3.9-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .
EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
