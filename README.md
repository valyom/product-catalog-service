# Product Catalog API

A REST API for managing a product catalog with hierarchical categories.

The project provides product and category management, product search and filtering, pagination, OpenAPI documentation, transaction handling, and concurrency protection.

## Features

- Product CRUD operations
- Hierarchical categories
- Category CRUD operations
- Product search by:
  - title
  - SKU
  - category
  - minimum price
  - maximum price
- Category search including descendant categories
- Pagination
- PostgreSQL persistence
- OpenAPI documentation
- Automated tests
- Optimistic locking for concurrent category updates
- Pessimistic locking for concurrent product modifications
- Docker-based environment
- Gunicorn with multiple workers

---

## Technology Stack

- Python 3.12
- Django 6
- Django REST Framework
- PostgreSQL 17
- Gunicorn
- Docker / Docker Compose
- drf-spectacular
- WhiteNoise

---

## Running the Project

The recommended way to run the application is with Docker Compose.

This works on:

- Linux
- WSL
- macOS
- Windows with Docker Desktop

### Prerequisites

Install:

- Docker
- Docker Compose

Verify the installation:

```bash
docker --version
docker compose version
```

---

## Configuration

Copy the example environment file.

### Linux / macOS / WSL

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Update the values in `.env` if necessary.

The `.env` file is intentionally excluded from version control.

---

## Start the Application

Build and start the services:

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000
```

The Django application runs with Gunicorn using multiple worker processes.

To stop the application:

```bash
docker compose down
```

---

## Database Migrations

Database migrations are executed automatically when the container starts.

To run migrations manually:

```bash
docker compose exec web python manage.py migrate
```

To create a new migration:

```bash
docker compose exec web python manage.py makemigrations
```
---

## Accessing PostgreSQL

To open a PostgreSQL shell for running direct SQL queries:

```bash
docker compose exec -it db psql -U ebag -d product_catalog
```
Some useful commands to try in psql:

```text
\dt

\d inventory_category

\d inventory_product

\q
```

---

## Seed Sample Data

The project includes a management command that creates sample categories and products.

The sample data includes:

- hierarchical product categories
- example products
- additional products for pagination testing

Run:

```bash
docker compose exec web python manage.py seed_data
```

---

## API Documentation

OpenAPI documentation is available while the application is running.

Swagger UI:

```text
http://localhost:8000/api/docs/
```

OpenAPI schema:

```text
http://localhost:8000/api/schema/
```

---

## API Endpoints

### Products

```text
GET    /api/v1/products/
POST   /api/v1/products/

GET    /api/v1/products/{id}/
PUT    /api/v1/products/{id}/
PATCH  /api/v1/products/{id}/
DELETE /api/v1/products/{id}/
```

### Categories

```text
GET    /api/v1/categories/
POST   /api/v1/categories/

GET    /api/v1/categories/{id}/
PUT    /api/v1/categories/{id}/
PATCH  /api/v1/categories/{id}/
DELETE /api/v1/categories/{id}/
```

---

## Product Search

Products can be filtered using query parameters.

Example:

```text
GET /api/v1/products/?title=apple
```

Supported filters:

```text
title
sku
category_id
price_min
price_max
```

Example:

```text
GET /api/v1/products/?category_id=3&price_min=2.00&price_max=10.00
```

When a category is used for filtering, products from its descendant categories are also included.

---

## Pagination

Product list results are paginated.

Example:

```text
GET /api/v1/products/?page=1
```

The sample dataset contains enough products to demonstrate pagination.

---

## Concurrency Handling

The application includes protection against concurrent modifications.

### Products

Product update and delete operations use database row locking with:

```python
select_for_update()
```

This prevents concurrent requests from modifying the same product simultaneously.

### Categories

Category updates use optimistic locking.

Each category contains a version field.

Example:

```json
{
    "name": "Electronics",
    "parent": null,
    "version": 1
}
```

The client must provide the current version when updating a category.

A successful update increments the version.

If another request has already modified the category, the update is rejected with:

```text
HTTP 409 Conflict
```

The client can then reload the category and retry with the latest version.

---

## Running Tests

Run all tests:

```bash
docker compose exec web python manage.py test
```

Run product search tests:

```bash
docker compose exec web python manage.py test \
    inventory.tests.test_product_search
```

Run category concurrency tests:

```bash
docker compose exec web python manage.py test \
    inventory.tests.test_category_concurrency
```

---

## Production Considerations

This project is implemented with production-oriented concerns in mind.

The application includes:

- database constraints
- database migrations
- transaction handling
- concurrency protection
- application logging
- multiple Gunicorn workers
- environment-based configuration
- static file handling
- automated tests

Sensitive configuration is provided through environment variables and is not committed to the repository.

---

## Clean Database Restart

To remove the current database volume and start with a clean database:

```bash
docker compose down -v
docker compose up --build
```

After the application starts, sample data can be loaded with:

```bash
docker compose exec web python manage.py seed_data
```
