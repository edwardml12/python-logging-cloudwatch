
# Python Logging with CloudWatch, Serverless, and Elastic Stack

## Overview

This project demonstrates a complete logging solution that integrates:
- **FastAPI** for building HTTP APIs
- **AWS CloudWatch** for centralized log management
- **Serverless Framework** for deploying to AWS Lambda
- **Elastic Stack** (Elasticsearch, Logstash, Kibana) for advanced log analysis and visualization

## Features

- Structured logging formatted for CloudWatch
- FastAPI application deployed via Serverless
- Automatic log aggregation to Elasticsearch
- Kibana dashboards for monitoring and analysis
- Lambda integration with CloudWatch Logs

## Prerequisites

- Python 3.9+
- Node.js and npm (for Serverless)
- AWS credentials configured
- Elasticsearch and Kibana (local or cloud)
- Mysql

## Installation

```bash
npm install -g serverless
pip install -r requirements.txt
```

## Project Structure

```
python-logging/
├── app/
│   ├── main.py           # FastAPI application
│   └── logger.py         # Logging configuration
├── serverless.yml        # Serverless configuration
├── requirements.txt
└── README.md
```

## Configuration

Configure CloudWatch and Elasticsearch endpoints in environment variables or `serverless.yml`.

## Deployment

```bash
serverless deploy
```

## Run Locally

### Option 1 — Uvicorn (local FastAPI)
```bash
pip install -r requirements.txt
# start the app (adjust module path if needed)
uvicorn app.main:app --reload --port 3000
```
Visit: http://localhost:3000

### Option 2 — Serverless Offline
```bash
npm install -g serverless
# ensure serverless-offline is in serverless.yml/plugins
sls offline
# or
sls offline start
```
Default offline endpoints are available at http://localhost:3000

