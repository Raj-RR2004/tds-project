TDS PROJECT 2
# TDS Project

This project is a FastAPI-based backend for processing uploaded datasets.

## Features
- Health check (`/healthz`)
- Upload and process files (`/api/`)
- Supports CSV, JSON, Parquet, TXT
- Generates correlation matrix, regression, and plots

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 10000

