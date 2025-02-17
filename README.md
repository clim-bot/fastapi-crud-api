# FastAPI CRUD API with SQLite

## Overview
This is a FastAPI-based CRUD API that uses SQLite as the database. The API supports the following operations:
- **GET**: Retrieve all items or a specific item
- **POST**: Create a new item
- **PUT**: Update an existing item
- **DELETE**: Remove an item from the database

The project also includes:
- **Swagger documentation** for API testing
- **Unit tests using Pytest**
- **Newman for API testing**
- **GitHub Actions for CI/CD automation**

## Installation
### 1. Clone the repository:
```sh
git clone https://github.com/clim-bot/fastapi-crud-api.git
cd fastapi-crud-api
```

### 2. Create a virtual environment:
```sh
python -m venv venv
```

### 3. Activate the virtual environment:
- **Windows (Command Prompt)**:
  ```sh
  venv\Scripts\activate
  ```
- **Windows (PowerShell)**:
  ```sh
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux**:
  ```sh
  source venv/bin/activate
  ```

### 4. Install dependencies:
```sh
pip install -r requirements.txt
```

## Running the Application
Start the FastAPI server with:
```sh
uvicorn app.main:app --reload
```

The API documentation will be available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running Tests
To run the unit tests using Pytest:
```sh
pytest tests
```

To run the Postman tests with Newman:
```sh
newman run postman/collection.json
```

## GitHub Actions CI/CD
This project includes a **GitHub Actions** workflow for automated testing. The workflow runs unit tests with Pytest upon every push or pull request.

### Workflow File:
Located in `.github/workflows/ci.yml`, this file sets up Python, installs dependencies, and runs tests automatically.

## License
This project is licensed under the MIT License.