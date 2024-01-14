# Dockerfile
FROM python:3.9

WORKDIR /api

COPY api/requirements.txt .

RUN pip install -r requirements.txt

COPY api .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]