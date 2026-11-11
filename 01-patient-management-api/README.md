# Patient Management API

A simple REST API built with **FastAPI** and **Pydantic** to practice CRUD operations, request validation, and API development in Python.

## Features

- Create, view, update, and delete patient records
- Sort patients by weight, height, or BMI
- Validate patient data using Pydantic
- Automatically calculate BMI and weight category
- Store patient records in a JSON file
- Interactive API documentation using Swagger UI

## Tech Stack

- Python
- FastAPI
- Pydantic
- JSON (file-based storage)

## Getting Started

**1. Install dependencies**


pip install "fastapi[standard]"


**2. Run the application**


python -m fastapi dev main.py


**3. Open the API documentation**

Visit: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | Get patient by ID |
| GET | `/sort` | Sort patient records |
| POST | `/create` | Add a patient |
| PATCH | `/update/{patient_id}` | Update patient information |
| DELETE | `/delete/{patient_id}` | Delete a patient |

## API Preview

This is a learning project. Patient records are stored locally in a JSON file rather than a database. The project helped me practice building REST APIs, handling HTTP requests, and validating data with Pydantic.