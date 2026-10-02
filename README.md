# Tip Calculator API

A small FastAPI service that calculates a bill total with optional tax, tip, rounding, and per-person sharing.

## Description

This project exposes a lightweight API for tip calculations. It supports:

- pre-tax or post-tax tip calculation
- tax percentages
- optional rounding modes
- total or per-person rounding targets
- even split calculation across people

## Features

- REST API built with FastAPI
- Decimal-based financial calculations
- Request validation using Pydantic
- Built-in health check endpoint
- JSON response model for totals and per-person shares

## Local setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the environment:
   ```bash
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API:
   ```bash
   python main.py
   ```

The app will be available at:

- http://localhost:8000/health
- http://localhost:8000/docs

## Example request

```json
{
  "bill": "100.00",
  "tip_percent": 20,
  "tax_percent": 8,
  "people": 2,
  "tip_base": "pre_tax",
  "rounding": "none",
  "round_target": "total"
}
```

## Example response

```json
{
  "subtotal": "100.00",
  "tax": "8.00",
  "tip": "20.00",
  "rounding_adjustment": "0.00",
  "total": "128.00",
  "people": 2,
  "shares": ["64.00", "64.00"]
}
```

## Notes

- Decimal arithmetic is used to help keep currency values precise.
- The repository is intended to be publicly shareable and easy to deploy.
- The API is designed for local development and simple financial calculations.
